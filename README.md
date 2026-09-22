# Bank Account Management System

A console-based bank account management system in Python demonstrating core
Object-Oriented Programming concepts.

## Files

| File | Purpose |
|---|---|
| `exceptions.py` | Custom exception hierarchy (`BankError`, `InvalidAmountError`, `InsufficientFundsError`, `AccountNotFoundError`) |
| `models.py` | `Transaction`, abstract `Account` base class, `SavingsAccount`, `CurrentAccount` |
| `bank.py` | `Bank` class — manages all accounts, search, and CSV file persistence |
| `main.py` | Interactive console menu (run this) |
| `demo.py` | Non-interactive script that exercises every feature end-to-end and prints results (used to generate `demo_output.txt`) |
| `accounts.csv` | Sample/persisted account data |
| `transactions.csv` | Sample/persisted transaction history |
| `demo_output.txt` | Captured console output from `demo.py` |

## How to run

```bash
python3 main.py
```

Menu options let you create accounts, deposit, withdraw, check balance, view
transaction history, search by name, list all accounts, run month-end
interest/fee processing, and save data before exiting.

To see a full automated walkthrough instead of typing into the menu:

```bash
python3 demo.py
```

## OOP concepts demonstrated

- **Classes & Objects (3+):** `Account` (abstract), `SavingsAccount`,
  `CurrentAccount`, `Transaction`, `Bank`.
- **Encapsulation:** `Account.__balance` is a private attribute accessed only
  through the `balance` property and the `deposit`/`withdraw` methods;
  `_account_number`/`_holder_name` are protected with getter methods.
- **Inheritance:** `SavingsAccount` and `CurrentAccount` both inherit from
  `Account` and reuse its `deposit`, `_apply_withdrawal`, and transaction
  logic.
- **Abstraction:** `Account` is an `abc.ABC` with abstract methods
  `account_type()` and `apply_monthly_update()` — it can never be
  instantiated directly, only through its subclasses.
- **File Handling:** `Bank.save_data()` / `load_data()` read and write
  `accounts.csv` and `transactions.csv` using the `csv` module.
- **Exception Handling:** Custom exceptions (`InvalidAmountError`,
  `InsufficientFundsError`, `AccountNotFoundError`) are raised for bad input
  and account-rule violations, and caught in `main.py`; file I/O errors are
  wrapped and caught as `OSError`.

## Business rules

- **SavingsAccount:** earns 4% annual interest (applied monthly, pro-rated);
  must keep a minimum balance of 500.00 — withdrawals that would breach this
  are rejected.
- **CurrentAccount:** allows overdraft up to 1000.00 below zero; a flat
  25.00 monthly maintenance fee is deducted on month-end processing.
