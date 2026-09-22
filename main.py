"""Console interface for the Bank Account Management System."""

from bank import Bank
from exceptions import BankError


MENU = """
========== BANK ACCOUNT MANAGEMENT SYSTEM ==========
1. Create Account
2. Deposit
3. Withdraw
4. Check Balance
5. Transaction History
6. Search Accounts by Name
7. Display All Accounts
8. Run Month-End (apply interest / fees)
9. Save & Exit
======================================================
"""


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number. Please enter a numeric value.")


def main():
    bank = Bank(data_file="accounts.csv", transactions_file="transactions.csv")
    try:
        bank.load_data()
        print(f"Loaded {len(bank.list_accounts())} existing account(s) from accounts.csv")
    except OSError as e:
        print(f"Warning: could not load existing data ({e}). Starting fresh.")

    while True:
        print(MENU)
        choice = input("Choose an option (1-9): ").strip()

        try:
            if choice == "1":
                name = input("Holder name: ")
                acc_type = input("Account type (savings/current): ")
                initial = get_float("Initial deposit: ")
                acc = bank.create_account(name, acc_type, initial)
                print(f"Account created successfully -> {acc}")

            elif choice == "2":
                acc_num = input("Account number: ")
                amount = get_float("Deposit amount: ")
                bank.deposit(acc_num, amount)
                print(f"Deposited {amount:.2f}. New balance: {bank.check_balance(acc_num):.2f}")

            elif choice == "3":
                acc_num = input("Account number: ")
                amount = get_float("Withdrawal amount: ")
                bank.withdraw(acc_num, amount)
                print(f"Withdrew {amount:.2f}. New balance: {bank.check_balance(acc_num):.2f}")

            elif choice == "4":
                acc_num = input("Account number: ")
                print(f"Balance: {bank.check_balance(acc_num):.2f}")

            elif choice == "5":
                acc_num = input("Account number: ")
                history = bank.transaction_history(acc_num)
                if not history:
                    print("No transactions yet.")
                for t in history:
                    print(" ", t)

            elif choice == "6":
                name = input("Search by name: ")
                results = bank.search_by_name(name)
                if not results:
                    print("No matching accounts.")
                for acc in results:
                    print(" ", acc)

            elif choice == "7":
                accounts = bank.list_accounts()
                if not accounts:
                    print("No accounts yet.")
                for acc in accounts:
                    print(" ", acc)

            elif choice == "8":
                summary = bank.run_month_end()
                for acc_num, acc_type, amount in summary:
                    label = "Interest credited" if acc_type == "Savings" else "Maintenance fee charged"
                    print(f"  {acc_num} ({acc_type}): {label} = {amount:.2f}")

            elif choice == "9":
                bank.save_data()
                print("Data saved to accounts.csv and transactions.csv. Goodbye!")
                break

            else:
                print("Invalid option, please choose between 1 and 9.")

        except BankError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except OSError as e:
            print(f"File error: {e}")


if __name__ == "__main__":
    main()
