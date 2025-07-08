
class bankAccount:
    def __init__(self, name, balance, interestRate, accNo):
        self.name = name
        self.balance = balance
        self.interestRate = interestRate
        self.accNo = accNo

    def outputter(self):
        try:
            print(f"""Account Name: {self.name}
Account Number: {self.accNo}
Balance: £{self.balance}
Current Interest: {int(round((self.interestRate - 1) * 100, 5))}%""")
        except:
            print(f"""Account Name: {self.name}
Account Number: {self.accNo}
Balance: £{self.balance}
Current Interest: {round((self.interestRate - 1) * 100, 4)}%""")

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
            new_rate = float(input(f"Your current interest rate is {round((self.interestRate-1)*100,5)}%, what is the new interest rate (in %)? "))
            self.interestRate = (new_rate / 100) + 1
            print(f"The new interest rate is {new_rate}%.")
        except ValueError:
            print("Invalid input for interest rate.")

    def calculate_expected_return(self):
        try:
            years = int(input("How many years will the money remain in this account? "))
            if years < 0:
                print("Years cannot be negative.")
                return
            expected_balance = self.balance * pow(self.interestRate, years)
            print(f"Your expected balance after {years} years is: £{expected_balance}")
        except ValueError:
            print("Invalid input for years.")


accounts = {}

def create_account():
    accName = input("What is your name? ").strip()
    accNo = abs(hash(accName)) % (10**10)
    if accNo in accounts:
        print("Account with this name already exists. Please use a different name.")
        return None
    try:
        balance = float(input("How much do you want to initially deposit? "))
        if balance < 0:
            print("Initial deposit cannot be negative.")
            return None
        interestRate = (float(input("What is the current interest rate (in %)? ")) / 100) + 1
    except ValueError:
        print("Invalid input.")
        return None
    accounts[accNo] = bankAccount(accName, balance, interestRate, accNo)
    print(f"Account created! Your account number is {accNo}. Please remember it.")
    return accNo

def auto_account(name,balanced,interest,number):
    accName = name
    accNo = number
    balance = balanced
    interestRate = interest
    accounts[accNo] = bankAccount(accName, balance, interestRate, accNo)

def select_account(version):
    if version == "normal":
        try:
            accNo = int(input("Enter your account number: "))
            if accNo not in accounts:
                print("Account not found.")
                return None
            return accNo
        except ValueError:
            print("Invalid account number input.")
            return None
    else:
        try:
            accNo = int(input("Enter recipients number: "))
            if accNo not in accounts:
                print("Account not found.")
                return None
            return accNo
        except ValueError:
            print("Invalid account number input.")
            return None

def menu():
    while True:
        try:
            menuResponse = int(input("""
Welcome to Mars Bank!
1. Create account
2. Deposit
3. Withdraw
4. Set interest rate
5. Calculate return
6. Show account info
7. Transfer to another account
8. Exit
Select an option (1-8): """))

        except ValueError:
            print("Invalid input. Please enter a number between 1 and 7.")
            continue

        if menuResponse == 1:
            create_account()
        elif menuResponse in [2,3,4,5,6]:
            accNo = select_account("normal")
            if accNo is None:
                continue
            account = accounts[accNo]

            if menuResponse == 2:
                account.deposit()
            elif menuResponse == 3:
                account.withdraw()
            elif menuResponse == 4:
                account.set_interest_rate()
            elif menuResponse == 5:
                account.calculate_expected_return()
            elif menuResponse == 6:
                account.outputter()
        elif menuResponse == 7:
            senderNo = select_account("normal")
            recipientNo = select_account("recipient")
            sender = accounts[senderNo]
            recipient = accounts[recipientNo]
            exchange = int(input("How much would you like to transfer? "))
            sender.balance -= exchange
            recipient.balance += exchange
            print(f"The transfer was successful, your new balance is {sender.balance}")

        elif menuResponse == 8:
            print("goodbye")
            break
        else:
            print("Please select a valid option (1-8).")

with open("accounts") as f:
    storedAccounts = (f.read()).split(",")

for x in range(len(storedAccounts)):
    try:
        storedAccounts[x] = int(storedAccounts[x])
    except:
        storedAccounts[x] = str(storedAccounts[x])


for i in range(len(storedAccounts)):
    if type(storedAccounts[i]) == str:
        auto_account(storedAccounts[i],storedAccounts[i+1],storedAccounts[i+2],storedAccounts[i+3])

menu()



