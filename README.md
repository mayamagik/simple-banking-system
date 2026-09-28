# Simple Banking System

A Python banking application developed as part of the Hyperskill Python with SQL course.

## Features

- Account creation
- PIN authentication
- Luhn-valid card number generation
- SQLite database storage
- Balance management
- Income deposits
- Card-to-card transfers
- Account deletion

## Project Stages

### Stage 1 — Basic Account System
Implemented account creation, PIN generation, login, balance checking, logout, and exit. Account data is stored temporarily in memory using a list.

### Stage 2 — Luhn Algorithm
Added generation of valid 16-digit card numbers using the Luhn algorithm. Accounts are still stored temporarily while the program is running.

### Stage 3 — SQLite Database
Replaced temporary storage with persistent SQLite storage using `card.s3db`. The database stores card numbers, PINs, and balances.

### Stage 4 — Banking Transactions
Added income deposits, card-to-card transfers, receiver-card validation, insufficient-funds checks, and account deletion.

## Tech

- Python
- SQLite
- SQL
- Luhn algorithm

## How to Run

```bash
python banking.py