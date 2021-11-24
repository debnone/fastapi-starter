import pytest
from app.calc import add, subtract, multiply, divide, BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [(3, 2, 5), (7, 1, 8), (12, 4, 16)])
def test_add(num1, num2, expected):
    print("Testing add function")
    assert add(num1, num2) == expected


def test_subtract():
    print("Testing subtract function")
    assert subtract(9, 4) == 5


def test_multiply():
    print("Testing multiply function")
    assert multiply(5, 3) == 15


def test_divide():
    print("Testing divide function")
    assert divide(10, 2) == 5


def test_bank_set_initial_amount():
    print("Testing BankAccount class")
    bank_account = BankAccount(50)
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    bank_account = BankAccount(50)
    bank_account.deposit(20)
    assert bank_account.balance == 70


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize(
    "deposited, withdrewed, expected",
    [(200, 100, 300), (50, 10, 90), (1200, 200, 2200)],
)
def test_bank_transaction(zero_bank_account, deposited, withdrewed, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrewed)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
