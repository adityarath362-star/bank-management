"""
Non-interactive demo that exercises every key operation of the Bank system
and prints the results — useful for generating sample console output
without needing to type into main.py's interactive menu.
"""

from bank import Bank
from exceptions import BankError

bank = Bank(data_file="accounts.csv", transactions_file="transactions.csv")

print("=== Creating accounts ===")
a1 = bank.create_account("Aditya Sharma", "savings", 1000)
a2 = bank.create_account("Priya Verma", "current", 500)
a3 = bank.create_account("Rohit Singh", "savings", 2000)
for acc in bank.list_accounts():
    print(" ", acc)

print("\n=== Deposits & Withdrawals ===")
bank.deposit(a1.get_account_number(), 500)
bank.withdraw(a2.get_account_number(), 300)
print(f"  {a1.get_account_number()} balance: {bank.check_balance(a1.get_account_number()):.2f}")
print(f"  {a2.get_account_number()} balance: {bank.check_balance(a2.get_account_number()):.2f}")

print("\n=== Testing overdraft on Current account (allowed up to limit) ===")
bank.withdraw(a2.get_account_number(), 1000)   # goes negative but within overdraft
print(f"  {a2.get_account_number()} balance after overdraft withdrawal: "
      f"{bank.check_balance(a2.get_account_number()):.2f}")

print("\n=== Testing minimum balance rule on Savings account (should fail) ===")
try:
    bank.withdraw(a1.get_account_number(), 2000)
except BankError as e:
    print(f"  Expected error: {e}")

print("\n=== Testing invalid input handling (should fail) ===")
try:
    bank.deposit(a1.get_account_number(), -50)
except BankError as e:
    print(f"  Expected error: {e}")

try:
    bank.get_account("9999")
except BankError as e:
    print(f"  Expected error: {e}")

print("\n=== Search by name ===")
for acc in bank.search_by_name("ri"):
    print(" ", acc)

print("\n=== Transaction history for", a1.get_account_number(), "===")
for t in bank.transaction_history(a1.get_account_number()):
    print(" ", t)

print("\n=== Month-end interest / fees ===")
for acc_num, acc_type, amount in bank.run_month_end():
    label = "Interest credited" if acc_type == "Savings" else "Maintenance fee charged"
    print(f"  {acc_num} ({acc_type}): {label} = {amount:.2f}")

print("\n=== Final account list ===")
for acc in bank.list_accounts():
    print(" ", acc)

bank.save_data()
print("\nData saved to accounts.csv and transactions.csv")
