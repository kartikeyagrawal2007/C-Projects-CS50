-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Looking for the crime scene report
SELECT description
FROM crime_scene_reports
WHERE year = 2025
AND month = 7
AND day = 28
AND street = 'Humphrey Street';

-- Looking at witness interviews
SELECT name, transcript
FROM interviews
WHERE year = 2025
AND month = 7
AND day = 28;

-- Finding vehicles leaving the bakery shortly after the theft
SELECT *
FROM bakery_security_logs
WHERE year = 2025
AND month = 7
AND day = 28
AND hour = 10
AND minute BETWEEN 15 AND 25;

-- Looking for ATM withdrawals at Leggett Street
SELECT *
FROM atm_transactions
WHERE year = 2025
AND month = 7
AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw';

-- Matching ATM accounts to people
SELECT people.name,
       people.phone_number,
       people.passport_number,
       people.license_plate,
       bank_accounts.account_number
FROM people
JOIN bank_accounts
ON people.id = bank_accounts.person_id
WHERE bank_accounts.account_number IN
(
    28500762,
    28296815,
    76054385,
    49610011,
    16153065,
    25506511,
    81061156,
    26013199
);

-- Looking for short phone calls made on the day of the theft
SELECT *
FROM phone_calls
WHERE year = 2025
AND month = 7
AND day = 28
AND duration < 60;

-- Finding the earliest flight out of Fiftyville the next day
SELECT *
FROM flights
WHERE year = 2025
AND month = 7
AND day = 29
ORDER BY hour, minute
LIMIT 5;

-- Checking passengers on the earliest flight
SELECT people.name
FROM passengers
JOIN people
ON passengers.passport_number = people.passport_number
WHERE passengers.flight_id = 36;

-- Finding the destination city
SELECT city
FROM airports
WHERE id = 4;

-- Identifying the accomplice
SELECT name
FROM people
WHERE phone_number = '(375) 555-8161';
