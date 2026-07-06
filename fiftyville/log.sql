-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Viewing crime scene report to get id and information about crime
SELECT id,description FROM crime_scene_reports WHERE year = 2025 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Crime id found = 295. Theft took place at 10:15 am at 'Humphrey Street bakery'; Three interviews of witnesses are conducted today;
-- We found a lead and now lets the interviews of these three witnesses


SELECT id, name, transcript from interviews WHERE year = 2025 AND month = 7 AND day = 28;

-- within 10 minutes of theft the thief got into car i.e between (10:15 - 10:25) check footage said RUTH 161
-- Thief withdraw money from atm on leggett street on the same day but before 10:15 am said Eugene 162
-- Thief called someone during leaving the bakery
-- theif took tomorrow first flight out of fiftyville. the other person purchased ticket today (163 raymond)

-- check security footage
-- check atm
-- check phone calls
-- check flights

SELECT id, caller, receiver FROM phone_calls WHERE year = 2025 AND month = 7 AND day = 28 AND duration <= 60;

-- The thief phone number and receiver helper is among these below
--+-----+----------------+----------------+
--| id  |     caller     |    receiver    |
--+-----+----------------+----------------+
--| 221 | (130) 555-0289 | (996) 555-8899 |
--| 224 | (499) 555-9472 | (892) 555-8872 |
--| 233 | (367) 555-5533 | (375) 555-8161 |
--| 234 | (609) 555-5876 | (389) 555-5198 |
--| 251 | (499) 555-9472 | (717) 555-1342 |
--| 254 | (286) 555-6063 | (676) 555-6554 |
--| 255 | (770) 555-1861 | (725) 555-3243 |
--| 261 | (031) 555-6622 | (910) 555-3251 |
--| 279 | (826) 555-1652 | (066) 555-9701 |
--| 281 | (338) 555-6650 | (704) 555-2131 |
--+-----+----------------+----------------+

-- Now checking footage for exit vehicles
SELECT id, activity, license_plate FROM bakery_security_logs WHERE year = 2025 AND month = 7 AND day = 28 AND hour = 10 AND (minute >= 15 AND minute <= 25) AND activity = 'exit';

-- id  | activity | license_plate |
--+-----+----------+---------------+
--| 260 | exit     | 5P2BI95       |
--| 261 | exit     | 94KL13X       |
--| 262 | exit     | 6P58WS2       |
--| 263 | exit     | 4328GD8       |
--| 264 | exit     | G412CB7       |
--| 265 | exit     | L93JTIZ       |
--| 266 | exit     | 322W7JE       |
--| 267 | exit     | 0NTHK55       |
--+-----+----------+---------------+

-- now checking atm transactions

SELECT id, account_number, transaction_type FROM atm_transactions WHERE year = 2025 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

--+-----+----------------+------------------+
--| id  | account_number | transaction_type |
--+-----+----------------+------------------+
--| 246 | 28500762       | withdraw         |
--| 264 | 28296815       | withdraw         |
--| 266 | 76054385       | withdraw         |
--| 267 | 49610011       | withdraw         |
--| 269 | 16153065       | withdraw         |
--| 288 | 25506511       | withdraw         |
--| 313 | 81061156       | withdraw         |
--| 336 | 26013199       | withdraw         |
-----+----------------+------------------+


--+---------+
--|  name   |
--+---------+
--| Kenny   |
--| Iman    |
--| Benista |
--| Taylor  |
--| Brooke  |
--| Luca    |
--| Diana   |
--| Bruce   |
--+---------+

SELECT name, phone_number, license_plate, passport_number FROM people WHERE people.id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2025 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw')) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2025 AND month = 7 AND day = 28 AND hour = 10 AND (minute >= 15 OR minute <= 25) AND activity = 'exit') AND phone_number IN (SELECT caller FROM phone_calls WHERE year = 2025 AND month = 7 AND day = 28 AND duration <= 60);


-- My 3 main theif suspects
SELECT name, phone_number, license_plate, passport_number FROM people WHERE people.id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2025 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw')) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2025 AND month = 7 AND day = 28 AND hour = 10 AND (minute >= 15 OR minute <= 25) AND activity = 'exit') AND phone_number IN (SELECT caller FROM phone_calls WHERE year = 2025 AND month = 7 AND day = 28 AND duration <= 60);

--+--------+----------------+---------------+-----------------+
--|  name  |  phone_number  | license_plate | passport_number |
--+--------+----------------+---------------+-----------------+
--| Taylor | (286) 555-6063 | 1106N58       | 1988161715      |
--| Diana  | (770) 555-1861 | 322W7JE       | 3592750733      |
--| Bruce  | (367) 555-5533 | 94KL13X       | 5773159633      |
--+--------+----------------+---------------+-----------------+

-- Now i want to check flights

SELECT flights.id, full_name, city, origin_airport_id, destination_airport_id, day, hour, minute FROM airports JOIN flights ON flights.origin_airport_id = airports.id WHERE year = 2025 AND month = 7 AND day = 29;

--- theif fled to destination_airport_id = 4 from origin_airport_id = 8

--- Theif is in New York City flight id 36

SELECT passport_number, seat FROM passengers WHERE flight_id = 36;

--+--------+----------------+---------------+-----------------+
--|  name  |  phone_number  | license_plate | passport_number |
--+--------+----------------+---------------+-----------------+
--| Taylor | (286) 555-6063 | 1106N58       | 1988161715      |
--| Bruce  | (367) 555-5533 | 94KL13X       | 5773159633      |
--+--------+----------------+---------------+-----------------+

-- Now check atm which one from taylor or bruce withdrew money from atm on 28th


SELECT name FROM people WHERE people.id IN (SELECT bank_accounts.person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2025 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'));

-- Again Bruce and Taylor they both withdrew money

-- CHECK WHICH LICENSE PLATE IS UNDER TAYLOR AND BRUCE NAME

SELECT license_plate FROM people WHERE name = 'Taylor' OR name = 'Bruce';

-- Only Bruce car was is the footage at the time of theft hence bruce is the culprit

SELECT name, phone_number FROM people WHERE phone_number = '(375) 555-8161';
-- Robin is the accomplice
