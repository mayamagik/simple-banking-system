# Simple Banking System Stage 1
import random
import sys


# Store created accounts in a list
accounts = []


# Create an account
def create_account():
    bank_id = "400000"                                  # 6 digits
    account_number = random.randint(10000000, 99999999)  # 8 digits
    customer_account_number = random.randint(0, 9)       # 1 digit
    checksum = random.randint(0, 9)                       # 1 digit

    # 16 digits in total
    card_number = (
        bank_id
        + str(account_number)
        + str(customer_account_number)
        + str(checksum)
    )

    # Keep PIN as a string and always make it 4 digits
    pin_number = f"{random.randint(0, 9999):04d}"

    # Store the new account
    account = {
        "card_number": card_number,
        "pin": pin_number,
        "balance": 0
    }

    accounts.append(account)
    print(
        f"Your card has been created\n"
        f"Your card number:\n"
        f"{card_number}\n"
        f"Your card PIN:\n"
        f"{pin_number}"
    )


# Log into an account
def login():
    user_card_number = input("Enter your card number:\n")
    user_pin_number = input("Enter your PIN:\n")

    for account in accounts:
        if (
            user_card_number == account["card_number"]
            and user_pin_number == account["pin"]
        ):
            print("You have successfully logged in!")
            account_menu(account)
            return

    print("Wrong card number or PIN!")


# Menu after successful login
def account_menu(account):
    while True:
        user_action = input(
            "1. Balance\n"
            "2. Log out\n"
            "0. Exit\n"
        )

        if user_action == "1":
            print(f'Balance: {account["balance"]}')

        elif user_action == "2":
            print("You have successfully logged out!")
            return

        elif user_action == "0":
            print("Bye!")
            sys.exit()

# Main menu
def create_menu():
    while True:
        user_action = input("1. Create an account\n"
                            "2. Log into account\n"
                            "0. Exit\n")

        if user_action == "1":
            create_account()

        elif user_action == "2":
            login()

        elif user_action == "0":
            print("Bye!")
            break


create_menu()