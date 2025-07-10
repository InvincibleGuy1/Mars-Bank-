import os
import time
import hashlib


class bankAccount:
    def __init__(self, name, balance, interestRate, accNo, password_hash):
        self.name = name
        self.balance = balance
        self.interestRate = interestRate
        self.accNo = accNo
        self.password_hash = password_hash  # Store the hashed password

    def outputter(self):
        print(f"""Account Name: {self.name}
Account Number: {self.accNo}
Balance: £{self.balance}
Current Interest: {self.interestRate}%""")

    def deposit(self):
        try:
            depositCount = float(input(f"Your current balance is £{self.balance}, how much would you like to deposit? "))
            if depositCount < 0:
                print("Deposit amount cannot be negative.")
                return
            self.balance += depositCount
            print(f"Your new balance is £{self.balance}.")
        except ValueError:
            print("Invalid input for deposit amount.")

    def withdraw(self):
        try:
            withdrawCount = float(input(f"Your current balance is £{self.balance}, how much would you like to withdraw? "))
            if withdrawCount < 0:
                print("Withdrawal amount cannot be negative.")
                return
            if withdrawCount > self.balance:
                print("Insufficient funds.")
                return
            self.balance -= withdrawCount
            print(f"Your new balance is £{self.balance}.")
        except ValueError:
            print("Invalid input for withdrawal amount.")

    def set_interest_rate(self):
        try:
            new_rate = float(input(f"Your current interest rate is {self.interestRate}%, what is the new interest rate (in %)? "))
            self.interestRate = new_rate
            print(f"The new interest rate is {new_rate}%.")
        except ValueError:
            print("Invalid input for interest rate.")

    def calculate_expected_return(self):
        try:
            years = int(input("How many years will the money remain in this account? "))
            expected_balance = self.balance * pow(self.interestRate / 100 + 1, years)
            print(f"Your expected balance after {years} years is: £{round(expected_balance, 2)}")
        except ValueError:
            print("Invalid input for years.")


accounts = {}
logged_in_account = None  # Keeps track of the logged-in user


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_account_number():
    return len(accounts) + 1  # Simple account number generation


def create_account():
    accName = input("What is your name? ").strip()
    accNo = generate_account_number()
    if accNo in accounts:
        print("Account with this name already exists. Please use a different name.")
        return None
    try:
        balance = float(input("How much do you want to initially deposit? "))
        if balance < 0:
            print("Initial deposit cannot be negative.")
            return None
        interestRate = (float(input("What is the current interest rate (in %)? ")) / 100) + 1
        password = input("Choose a password: ").strip()
        password_hash = hash_password(password)
    except ValueError:
        print("Invalid input.")
        return None
    accounts[accNo] = bankAccount(accName, balance, interestRate, accNo, password_hash)
    print(f"Account created! Your account number is {accNo}. Please remember it.")
    return accNo


def load_accounts():
    if os.path.exists('accounts.csv'):
        with open('accounts.csv', 'r') as f:
            lines = f.readlines()
            for line in lines:
                fields = line.strip().split(",")
                if len(fields) == 5:
                    name, balance, interestRate, accNo, password_hash = fields
                    balance = float(balance)
                    interestRate = float(interestRate)
                    accNo = int(accNo)
                    accounts[accNo] = bankAccount(name, balance, interestRate, accNo, password_hash)


def save():
    with open('accounts.csv', 'w') as f:
        for account in accounts.values():
            f.write(f"{account.name},{account.balance},{account.interestRate},{account.accNo},{account.password_hash}\n")


def login():
    global logged_in_account
    acc_identifier = input("Enter your account number or name: ").strip()
    password = input("Enter your password: ").strip()

    if acc_identifier.isdigit():
        accNo = int(acc_identifier)
        if accNo not in accounts:
            print("Account not found.")
            return None
        account = accounts[accNo]
    else:
        account = None
        for acc in accounts.values():
            if acc.name.lower() == acc_identifier.lower():
                account = acc
                break
        if account is None:
            print("Account not found.")
            return None

    if account.password_hash == hash_password(password):
        logged_in_account = account
        print(f"Welcome back, {account.name}!")
        return account
    else:
        print("Incorrect password.")
        return None


def logged_in_menu():
    global logged_in_account
    while True:
        try:
            menuResponse = int(input(f"""
You are logged in as {logged_in_account.name}.
1. Deposit
2. Withdraw
3. Set interest rate
4. Calculate return
5. Show account info
6. Transfer to another account
7. Logout
8. Exit
Select an option (1-8): """))

        except ValueError:
            print("Invalid input. Please enter a number between 1 and 8.")
            continue

        if menuResponse == 1:
            logged_in_account.deposit()
        elif menuResponse == 2:
            logged_in_account.withdraw()
        elif menuResponse == 3:
            logged_in_account.set_interest_rate()
        elif menuResponse == 4:
            logged_in_account.calculate_expected_return()
        elif menuResponse == 5:
            logged_in_account.outputter()
        elif menuResponse == 6:
            senderNo = int(input("Enter your account number: "))
            recipientNo = int(input("Enter recipient account number: "))
            sender = accounts.get(senderNo)
            recipient = accounts.get(recipientNo)

            if sender and recipient:
                amount = float(input("How much would you like to transfer? "))
                if sender.balance >= amount:
                    sender.balance -= amount
                    recipient.balance += amount
                    print(f"Transfer successful. Your new balance is £{sender.balance}.")
                else:
                    print("Insufficient funds for transfer.")
            else:
                print("Account not found.")
        elif menuResponse == 7:
            logged_in_account = None
            print("You have logged out.")
            break
        elif menuResponse == 8:
            save()
            print("Goodbye!")
            break
        else:
            print("Please select a valid option (1-8).")


def pre_login_menu():
    global logged_in_account
    while True:
        if logged_in_account:
            logged_in_menu()
            break
        try:
            menuResponse = int(input("""
Welcome to Mars Bank!
1. Login
2. Create account
3. Exit
Select an option (1-3): """))

        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
            continue

        if menuResponse == 1:
            login()
        elif menuResponse == 2:
            create_account()
        elif menuResponse == 3:
            save()
            print("Goodbye!")
            break
        else:
            print("Please select a valid option (1-3).")


def main():
    load_accounts()  # Load stored accounts on start
    pre_login_menu()  # Start the pre-login menu

main()
