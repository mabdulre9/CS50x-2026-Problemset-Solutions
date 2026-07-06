import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Get all unique symbols owned by the user
    rows = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", user_id)

    stocks = []
    total_value = 0

    for row in rows:
        symbol = row["symbol"]
        shares = row["total_shares"]

        # Look up current price
        quote = lookup(symbol)
        if quote is None:
            continue # Skip if lookup fails

        price = quote["price"]
        total_stock_value = shares * price

        stocks.append({
            "symbol": symbol,
            "name": quote["name"],
            "shares": shares,
            "price": price,
            "total": total_stock_value
        })

        total_value += total_stock_value

    # Get user's cash
    user_rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = user_rows[0]["cash"]

    grand_total = cash + total_value

    return render_template("index.html", stocks=stocks, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure shares was submitted and is a positive integer
        shares_str = request.form.get("shares")
        if not shares_str or not shares_str.isdigit() or int(shares_str) <= 0:
            return apology("must provide a positive integer number of shares", 400)

        shares = int(shares_str)

        # Lookup the stock
        quote = lookup(request.form.get("symbol"))
        if quote is None:
            return apology("invalid symbol", 400)

        # Calculate total cost
        price = quote["price"]
        total_cost = price * shares

        # Check user's cash balance
        user_id = session["user_id"]
        rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = rows[0]["cash"]

        if cash < total_cost:
            return apology("not enough cash",400)

        # Update user's cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total_cost, user_id)

        # Record the transaction
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)",
                   user_id, quote["symbol"], shares, price, "BUY")

        # Redirect to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    # Get all transactions for the user, ordered by time
    rows = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", user_id)

    return render_template("history.html", transactions=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Lookup the stock
        quote = lookup(request.form.get("symbol"))

        # Ensure valid symbol
        if quote is None:
            return apology("invalid symbol", 400)

        # Render quoted template
        return render_template("quoted.html", name=quote["name"], price=quote["price"], symbol=quote["symbol"])

    # User reached route via GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])

def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation matches password
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Hash the password
        hash = generate_password_hash(request.form.get("password"))

        # Insert the new user into the database
        try:
            result = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hash)
        except ValueError:
            return apology("username already exists", 400)

        # Remember which user has logged in
        session["user_id"] = result

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    # User reached route via GET
    if request.method == "GET":
        # Get all unique symbols owned by the user with positive shares
        rows = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", stocks=rows)

    # User reached route via POST
    else:
        # Ensure symbol was selected
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        # Ensure shares was submitted and is a positive integer
        shares_str = request.form.get("shares")
        if not shares_str or not shares_str.isdigit() or int(shares_str) <= 0:
            return apology("must provide a positive integer number of shares", 400)

        shares = int(shares_str)

        # Check if user owns enough shares
        rows = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)
        total_shares_owned = rows[0]["total_shares"]

        if total_shares_owned is None or total_shares_owned < shares:
            return apology("not enough shares", 400)

        # Lookup current price
        quote = lookup(symbol)
        if quote is None:
            return apology("invalid symbol", 400)

        price = quote["price"]
        total_sale_value = price * shares

        # Update user's cash
        user_rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        current_cash = user_rows[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash + total_sale_value, user_id)

        # Record the transaction (negative shares to indicate sell)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)",
                   user_id, symbol, -shares, price, "SELL")

        return redirect("/")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to user's account"""
    # User reached route via GET
    if request.method == "GET":
        return render_template("add_cash.html")

    # User reached route via POST
    else:
        # Ensure amount was submitted
        amount_str = request.form.get("amount")
        if not amount_str or not amount_str.replace('.', '', 1).isdigit() or float(amount_str) <= 0:
            return apology("must provide a positive amount", 403)

        amount = float(amount_str)

        # Update user's cash
        user_id = session["user_id"]
        rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        current_cash = rows[0]["cash"]

        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash + amount, user_id)

        # Flash a message to confirm
        flash(f"Added ${amount:,.2f} to your account!")

        return redirect("/")
