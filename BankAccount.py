import os
import random


# Bank account that stores every transaction in a statement file.
class BankAccount(object):
    # IDs already given out in this run, so two accounts cannot share one.
    _used_ids = set()

    # Create an account with a username, type (checking or saving), and balance (0 by default).
    def __init__(self, name, accountType, balance=0):
        if not name or not str(name).strip():
            raise ValueError("Username is required.")

        account_type = str(accountType).strip().lower()
        if account_type not in ("checking", "saving"):
            raise ValueError("Account type must be 'checking' or 'saving'.")

        try:
            opening_balance = float(balance)
        except (TypeError, ValueError):
            raise ValueError("Balance must be a number.")

        if opening_balance < 0:
            raise ValueError("Opening balance cannot be negative.")

        self.name = str(name).strip()
        self.accountType = account_type
        self.balance = opening_balance
        # Generate a new account ID, then name the statement file from ID, type, and username.
        self.accountNumber = self._generate_account_number()
        self.filename = (
            str(self.accountNumber) + "_" + self.accountType + "_" + self.name + ".txt"
        )
        self._create_statement_file()

    # Build a unique account ID and skip any ID whose statement file already exists.
    def _generate_account_number(self):
        while True:
            account_number = random.randint(100000, 999999)
            candidate = str(account_number) + "_" + self.accountType + "_" + self.name + ".txt"
            if account_number not in BankAccount._used_ids and not os.path.exists(candidate):
                BankAccount._used_ids.add(account_number)
                return account_number

    # Create the statement file and write the opening balance.
    def _create_statement_file(self):
        with open(self.filename, "w", encoding="utf-8") as statement:
            statement.write(
                "Account opened | ID: {0} | Type: {1} | Balance: {2}\n".format(
                    self.accountNumber, self.accountType, self._money(self.balance)
                )
            )

    # Append one transaction line to the statement file.
    def _record(self, message):
        with open(self.filename, "a", encoding="utf-8") as statement:
            statement.write(message + "\n")

    # Format a money amount with two decimal places.
    @staticmethod
    def _money(amount):
        return "{0:.2f}".format(float(amount))

    # Deposit money and store the transaction in the statement file.
    def deposit(self, amount):
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            print("Deposit rejected: amount must be a number.")
            return False

        if amount <= 0:
            print("Deposit rejected: amount must be greater than zero.")
            return False

        self.balance += amount
        self._record(
            "Deposit: {0} | Balance: {1}".format(self._money(amount), self._money(self.balance))
        )
        print("Deposited {0}. New balance: {1}".format(self._money(amount), self._money(self.balance)))
        return True

    # Withdraw money and store the transaction. Reject amounts higher than the balance.
    def withdraw(self, amount):
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            print("Withdrawal rejected: amount must be a number.")
            return False

        if amount <= 0:
            print("Withdrawal rejected: amount must be greater than zero.")
            return False

        if amount > self.balance:
            print(
                "Withdrawal rejected: cannot withdraw {0}. Available balance: {1}".format(
                    self._money(amount), self._money(self.balance)
                )
            )
            return False

        self.balance -= amount
        self._record(
            "Withdraw: {0} | Balance: {1}".format(self._money(amount), self._money(self.balance))
        )
        print("Withdrew {0}. New balance: {1}".format(self._money(amount), self._money(self.balance)))
        return True

    # Return the current balance.
    def getBalance(self):
        return self.balance

    # Return the account ID.
    def getID(self):
        return self.accountNumber

    # Return the username.
    def getUsername(self):
        return self.name

    # Return the account type.
    def getAccountType(self):
        return self.accountType

    # Read the statement file and return the transaction history.
    def getTransactionHistory(self):
        with open(self.filename, "r", encoding="utf-8") as statement:
            return statement.read()


# Print one account's details and its statement.
def _show_account(account):
    print("-" * 48)
    print("Username:  {0}".format(account.getUsername()))
    print("ID:        {0}".format(account.getID()))
    print("Type:      {0}".format(account.getAccountType()))
    print("Balance:   {0:.2f}".format(account.getBalance()))
    print("Statement: {0}".format(account.filename))
    print("History:")
    print(account.getTransactionHistory().rstrip())
    print()


# Create several accounts and run different deposits and withdrawals.
if __name__ == "__main__":
    alice = BankAccount("Alice", "checking", 100)
    bob = BankAccount("Bob", "saving")
    carol = BankAccount("Carol", "checking", 250)

    alice.deposit(50)
    alice.withdraw(30)
    alice.withdraw(500)  # rejected because it is higher than the balance

    bob.deposit(200)
    bob.withdraw(75)
    bob.deposit(25)

    carol.withdraw(100)
    carol.deposit(40)
    carol.withdraw(190)

    for account in (alice, bob, carol):
        _show_account(account)
