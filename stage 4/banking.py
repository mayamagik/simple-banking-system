# Simple Banking System Stage 4

import random
import sqlite3
import sys

# Accounts are stored permanently in an SQLite database
# Create DB connection
conn = sqlite3.connect("card.s3db")

# Create cursor object
cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS card (
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
)
""")

conn.commit()


# Create an account
def create_account():
    bank_id = "400000"

    # Generate 9-digit account identifier
    customer_account_number = f"{random.randint(0, 999999999):09d}"

    # First 15 digits
    temporary_account = bank_id + customer_account_number

    # Calculate last/checksum digit
    checksum = create_checksum(temporary_account)

    # Complete 16-digit card number
    card_number = temporary_account + str(checksum)

    # Generate 4-digit PIN
    pin_number = f"{random.randint(0, 9999):04d}"

    # Store account in database
    cur.execute(
        "INSERT INTO card (number, pin) VALUES (?, ?)",
        (card_number, pin_number)
    )
    conn.commit()

    print(
        f"Your card has been created\n"
        f"Your card number:\n"
        f"{card_number}\n"
        f"Your card PIN:\n"
        f"{pin_number}"
    )


# Create checksum / last digit using Luhn algorithm
def create_checksum(temporary_account):
    total = 0

    for index, digit in enumerate(temporary_account):
        digit = int(digit)

        # Odd positions 1, 3, 5... have indexes 0, 2, 4...
        if index % 2 == 0:
            digit *= 2

            if digit > 9:
                digit -= 9

        total += digit

    # total + checksum must be divisible by 10
    checksum = (10 - total % 10) % 10

    return checksum


# Check whether a complete card number passes Luhn
def is_luhn_valid(card_number):
    total = 0

    for index, digit in enumerate(card_number):
        digit = int(digit)

        if index % 2 == 0:
            digit *= 2

            if digit > 9:
                digit -= 9

        total += digit

    return total % 10 == 0


# Log into an account
def login():
    user_card_number = input("Enter your card number:\n")
    user_pin_number = input("Enter your PIN:\n")

    cur.execute(
        "SELECT * FROM card WHERE number = ? AND pin = ?",
        (user_card_number, user_pin_number)
    )

    account = cur.fetchone()

    if account:
        print("You have successfully logged in!")
        account_menu(user_card_number)
    else:
        print("Wrong card number or PIN!")


# Menu after successful login
def account_menu(card_number):
    while True:
        user_action = input(
            "1. Balance\n"
            "2. Add income\n"
            "3. Do transfer\n"
            "4. Close account\n"
            "5. Log out\n"
            "0. Exit\n"
        )

        # Show balance
        if user_action == "1":
            cur.execute(
                "SELECT balance FROM card WHERE number = ?",
                (card_number,)
            )

            balance = cur.fetchone()[0]

            print(f"Balance: {balance}")

        # Add income
        elif user_action == "2":
            added_income = int(input("Enter income:\n"))

            cur.execute(
                "UPDATE card SET balance = balance + ? WHERE number = ?",
                (added_income, card_number)
            )
            conn.commit()

            print("Income was added!")

        # Transfer money
        elif user_action == "3":
            do_transfer(card_number)

        # Close account
        elif user_action == "4":
            cur.execute(
                "DELETE FROM card WHERE number = ?",
                (card_number,)
            )
            conn.commit()

            print("The account has been closed!")
            return

        # Log out
        elif user_action == "5":
            print("You have successfully logged out!")
            return

        # Exit program
        elif user_action == "0":
            print("Bye!")
            conn.close()
            sys.exit()


# Transfer money to another account
def do_transfer(card_number):
    print("Transfer")

    transfer_card_number = input("Enter card number:\n")

    # Check if user entered same card number
    if transfer_card_number == card_number:
        print("You can't transfer money to the same account!")
        return

    # Check Luhn
    if not is_luhn_valid(transfer_card_number):
        print(
            "Probably you made a mistake in the card number. "
            "Please try again!"
        )
        return

    # Check if receiver exists
    cur.execute(
        "SELECT number FROM card WHERE number = ?",
        (transfer_card_number,)
    )

    receiver = cur.fetchone()

    if receiver is None:
        print("Such a card does not exist.")
        return

    # Ask for amount
    transfer_amount = int(
        input("Enter how much money you want to transfer:\n")
    )

    # Get sender's current balance
    cur.execute(
        "SELECT balance FROM card WHERE number = ?",
        (card_number,)
    )

    balance = cur.fetchone()[0]

    # Check if sender has enough money
    if transfer_amount > balance:
        print("Not enough money!")
        return

    # Remove money from sender
    cur.execute(
        "UPDATE card SET balance = balance - ? WHERE number = ?",
        (transfer_amount, card_number)
    )

    # Add money to receiver
    cur.execute(
        "UPDATE card SET balance = balance + ? WHERE number = ?",
        (transfer_amount, transfer_card_number)
    )

    conn.commit()

    print("Success!")


# Main menu
def create_menu():
    while True:
        user_action = input(
            "1. Create an account\n"
            "2. Log into account\n"
            "0. Exit\n"
        )

        if user_action == "1":
            create_account()

        elif user_action == "2":
            login()

        elif user_action == "0":
            print("Bye!")
            conn.close()
            break


create_menu()