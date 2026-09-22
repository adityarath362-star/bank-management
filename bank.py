"""Bank class: the main manager object that holds all accounts and handles file I/O."""

import csv
import os

from models import SavingsAccount, CurrentAccount
from exceptions import AccountNotFoundError, InvalidAmountError


class Bank:
    """Manages a collection of Account objects (composition, not inheritance)."""

    def __init__(self, data_file="accounts.csv", transactions_file="transactions.csv"):
        self._accounts = {}          # account_number -> Account
        self.data_file = data_file
        self.transactions_file = transactions_file
        self._next_id = 1001

    # ---------- Core operations ----------
    def create_account(self, holder_name, account_type="savings", initial_deposit=0.0):
        if not holder_name or not holder_name.strip():
            raise ValueError("Holder name cannot be empty")
        if initial_deposit < 0:
            raise InvalidAmountError("Initial deposit cannot be negative")

        acc_num = str(self._next_id)
        self._next_id += 1

        account_type = account_type.strip().lower()
        if account_type == "savings":
            acc = SavingsAccount(acc_num, holder_name.strip(), initial_deposit)
        elif account_type == "current":
            acc = CurrentAccount(acc_num, holder_name.strip(), initial_deposit)
        else:
            raise ValueError("Account type must be 'savings' or 'current'")

        self._accounts[acc_num] = acc
        return acc

    def get_account(self, acc_num):
        acc_num = str(acc_num).strip()
        if acc_num not in self._accounts:
            raise AccountNotFoundError(f"No account found with number '{acc_num}'")
        return self._accounts[acc_num]

    def deposit(self, acc_num, amount):
        self.get_account(acc_num).deposit(amount)

    def withdraw(self, acc_num, amount):
        self.get_account(acc_num).withdraw(amount)

    def check_balance(self, acc_num):
        return self.get_account(acc_num).balance

    def transaction_history(self, acc_num):
        return self.get_account(acc_num).get_transaction_history()

    def search_by_name(self, name):
        name = name.lower().strip()
        return [a for a in self._accounts.values() if name in a.get_holder_name().lower()]

    def list_accounts(self):
        return list(self._accounts.values())

    def close_account(self, acc_num):
        acc = self.get_account(acc_num)
        del self._accounts[acc.get_account_number()]

    def run_month_end(self):
        """Apply monthly interest/fees to every account. Returns a summary list."""
        summary = []
        for acc in self._accounts.values():
            amount = acc.apply_monthly_update()
            summary.append((acc.get_account_number(), acc.account_type(), amount))
        return summary

    # ---------- File handling ----------
    def save_data(self):
        try:
            with open(self.data_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["account_number", "holder_name", "account_type", "balance"])
                for acc in self._accounts.values():
                    writer.writerow([
                        acc.get_account_number(),
                        acc.get_holder_name(),
                        acc.account_type(),
                        f"{acc.balance:.2f}",
                    ])

            with open(self.transactions_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["account_number", "type", "amount", "balance_after", "timestamp"])
                for acc in self._accounts.values():
                    for t in acc.get_transaction_history():
                        writer.writerow(t.to_csv_row(acc.get_account_number()))
        except OSError as e:
            raise OSError(f"Failed to save bank data: {e}")

    def load_data(self):
        if not os.path.exists(self.data_file):
            return
        try:
            with open(self.data_file, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    acc_num = row["account_number"]
                    acc_type = row["account_type"]
                    balance = float(row["balance"])
                    if acc_type == "Savings":
                        acc = SavingsAccount(acc_num, row["holder_name"], balance)
                    else:
                        acc = CurrentAccount(acc_num, row["holder_name"], balance)
                    self._accounts[acc_num] = acc
                    if acc_num.isdigit() and int(acc_num) >= self._next_id:
                        self._next_id = int(acc_num) + 1
        except (OSError, csv.Error, KeyError, ValueError) as e:
            raise OSError(f"Failed to load bank data: {e}")
