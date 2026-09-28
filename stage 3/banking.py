#Simple Banking System Stage 3
import random
import sqlite3

# Accounts are stored permanently in an SQLite database
# Create DB connection
conn = sqlite3.connect("card.s3db")

# Create cursor object
cur = conn.cursor()

# Create table if it does not exist
cur.execute("""
CREATE TABLE IF NOT EXISTS card (
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
)
""")

conn.commit()


## Create checksum / last digit using Luhn algorithm
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

# Create a new account
def create_account():
    bank_id = "400000"

    customer_account_number = f"{random.randint(0, 999999999):09d}"

    temporary_account = bank_id + customer_account_number

    checksum = create_checksum(temporary_account)

    card_number = temporary_account + str(checksum)

    pin_number = f"{random.randint(0, 9999):04d}"

    # Store account in database
    cur.execute(
        "INSERT INTO card (number, pin) VALUES (?, ?)",
        (card_number, pin_number)
    )

    conn.commit()

    print(
        "\nYour card has been created\n"
        "Your card number:\n"
        f"{card_number}\n"
        "Your card PIN:\n"
        f"{pin_number}\n"
    )


# Menu after successful login
def account_menu(card_number):
    while True:
        print(
            "1. Balance\n"
            "2. Log out\n"
            "0. Exit"
        )

        choice = input()

        if choice == "1":
            cur.execute(
                "SELECT balance FROM card WHERE number = ?",
                (card_number,)
            )

            result = cur.fetchone()

            print(f"\nBalance: {result[0]}\n")

        elif choice == "2":
            print("\nYou have successfully logged out!\n")
            return

        elif choice == "0":
            print("\nBye!")
            conn.close()
            exit()


# Log into an existing account
def login():
    card_number = input("\nEnter your card number:\n")
    pin_number = input("Enter your PIN:\n")

    cur.execute(
        "SELECT number, pin FROM card WHERE number = ? AND pin = ?",
        (card_number, pin_number)
    )

    account = cur.fetchone()

    if account:
        print("\nYou have successfully logged in!\n")
        account_menu(card_number)

    else:
        print("\nWrong card number or PIN!\n")


# Main menu
def main():
    while True:
        print(
            "1. Create an account\n"
            "2. Log into account\n"
            "0. Exit"
        )

        choice = input()

        if choice == "1":
            create_account()

        elif choice == "2":
            login()

        elif choice == "0":
            print("\nBye!")
            break

    conn.close()


main()