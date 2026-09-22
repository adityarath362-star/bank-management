"""Custom exception classes for the Bank Account Management System."""


class BankError(Exception):
    """Base class for all bank-related exceptions."""
    pass


class InvalidAmountError(BankError):
    """Raised when a deposit/withdrawal/initial amount is invalid (<= 0 or negative)."""
    pass


class InsufficientFundsError(BankError):
    """Raised when a withdrawal would breach available balance or account rules."""
    pass


class AccountNotFoundError(BankError):
    """Raised when an account number does not exist in the bank."""
    pass
