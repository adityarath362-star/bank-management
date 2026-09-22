"""
Domain models for the Bank Account Management System.

Classes:
    Transaction      - a single deposit/withdrawal record
    Account (ABC)     - abstract base class for all account types
    SavingsAccount    - concrete account with interest + minimum balance rule
    CurrentAccount    - concrete account with overdraft facility
"""

from abc import ABC, abstractmethod
from datetime import datetime

from exceptions import InvalidAmountError, InsufficientFundsError


class Transaction:
    """Represents a single transaction on an account (encapsulated record)."""

    def __init__(self, ttype, amount, balance_after, timestamp=None):
        self.ttype = ttype
        self.amount = amount
        self.balance_after = balance_after
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"[{self.timestamp}] {self.ttype:<10} {self.amount:>10.2f} | Balance after: {self.balance_after:.2f}"

    def to_csv_row(self, account_number):
        return [account_number, self.ttype, f"{self.amount:.2f}", f"{self.balance_after:.2f}", self.timestamp]


class Account(ABC):
    """
    Abstract base class representing a generic bank account.

    Demonstrates:
        - Abstraction (ABC + abstractmethod)
        - Encapsulation (private __balance, protected _account_number/_holder_name)
    """

    def __init__(self, account_number, holder_name, balance=0.0):
        if balance < 0:
            raise InvalidAmountError("Initial balance cannot be negative")
        self._account_number = account_number
        self._holder_name = holder_name
        self.__balance = float(balance)          # private attribute (name-mangled)
        self._transactions = []                  # protected attribute

    # ---------- Encapsulated access (getters / property) ----------
    @property
    def balance(self):
        return self.__balance

    def get_account_number(self):
        return self._account_number

    def get_holder_name(self):
        return self._holder_name

    def get_transaction_history(self):
        return list(self._transactions)

    # ---------- Shared behaviour ----------
    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")
        self.__balance += amount
        self._record_transaction("DEPOSIT", amount)

    def withdraw(self, amount):
        """Generic rule: cannot withdraw more than the current balance.
        Subclasses override this to apply their own rule (min balance / overdraft)."""
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        if amount > self.__balance:
            raise InsufficientFundsError(
                f"Insufficient funds. Available balance: {self.__balance:.2f}"
            )
        self._apply_withdrawal(amount)

    def _apply_withdrawal(self, amount):
        """Protected helper that actually mutates the private balance.
        Defined here so subclasses can reuse it after their own checks,
        while __balance name-mangling still resolves correctly (mangled to Account)."""
        self.__balance -= amount
        self._record_transaction("WITHDRAW", amount)

    def _record_transaction(self, ttype, amount):
        self._transactions.append(Transaction(ttype, amount, self.__balance))

    # ---------- Abstraction: must be implemented by every subclass ----------
    @abstractmethod
    def account_type(self):
        """Return a human readable account type string."""
        raise NotImplementedError

    @abstractmethod
    def apply_monthly_update(self):
        """Apply the account's monthly rule (interest or maintenance fee)."""
        raise NotImplementedError

    def __str__(self):
        return (f"{self._account_number} | {self._holder_name:<20} | "
                f"{self.account_type():<8} | Balance: {self.__balance:.2f}")


class SavingsAccount(Account):
    """Concrete account: earns monthly interest, enforces a minimum balance."""

    INTEREST_RATE = 0.04     # 4% annual
    MIN_BALANCE = 500.0

    def account_type(self):
        return "Savings"

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        if self.balance - amount < self.MIN_BALANCE:
            raise InsufficientFundsError(
                f"Withdrawal denied: minimum balance of {self.MIN_BALANCE:.2f} must be maintained"
            )
        self._apply_withdrawal(amount)

    def apply_monthly_update(self):
        interest = round(self.balance * self.INTEREST_RATE / 12, 2)
        if interest > 0:
            self.deposit(interest)
        return interest


class CurrentAccount(Account):
    """Concrete account: allows overdraft up to a limit, charges a maintenance fee."""

    OVERDRAFT_LIMIT = 1000.0
    MAINTENANCE_FEE = 25.0

    def account_type(self):
        return "Current"

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        if self.balance - amount < -self.OVERDRAFT_LIMIT:
            raise InsufficientFundsError(
                f"Withdrawal denied: overdraft limit of {self.OVERDRAFT_LIMIT:.2f} exceeded"
            )
        self._apply_withdrawal(amount)

    def apply_monthly_update(self):
        fee = self.MAINTENANCE_FEE
        # Charge fee directly (bypasses withdraw rule since it's a bank-side deduction)
        self._apply_withdrawal(fee)
        return fee
