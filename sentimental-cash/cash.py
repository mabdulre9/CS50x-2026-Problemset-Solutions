while True:
    change = input("Change: ")
    try:
        change = float(change)
        break
    except ValueError:
        continue

change = int(change*100)

quarter = 25
dime = 10
nickel = 5
penny = 1
coins = 0

while change!=0:

    if change >= quarter:
        change -= quarter
        coins+=1
    elif change >= dime:
        change -= dime
        coins+=1
    elif change >= nickel:
        change -= nickel
        coins+=1
    else:
        change -= penny
        coins+=1

print(coins)
