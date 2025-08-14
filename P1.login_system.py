
class AccountData:
    def __init__(self):
        self.__accounts = {}

    def create_account(self, username: str, password: str):
        self.__accounts[username] = [password, 0]

    def view_all_accounts(self):
        return self.__accounts
    
    def view_account(self, username: str, password: str):
        if self.__accounts[username][0] == password:
            print("Signed in!")
            self.account_options(username)
        else:
            print("Invalid password.")

    def account_options(self, username):
        while True:
            print("")
            print("  1 - Add to balance \n  2 - View balance \n  0 - Log out")
            action = input("  Action: ")
            if action == "0":
                break
            elif action == "1":
                deposit = int(input("  Deposit: "))
                if deposit > 0:
                    self.__accounts[username][1] += deposit
                else:
                    print("  Deposit must be larger than 0.")
            elif action == "2":
                print(f"  You have {self.__accounts[username][1]}$")
            else:
                print("  1 - Add to balance \n  2 - View balance \n  0 - Log out")
            


class Application:
    def __init__(self):
        self.data = AccountData()

    def create_account(self):
        print("Create an account")
        username = input("Username: ")
        password = input("Password: ")
        pass_check = input("Enter password again: ")
        if password == pass_check:
            print("Account created successfully!")
            self.data.create_account(username, password)
        else:
            print("Passwords do not match.")

    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        self.data.view_account(username, password)


    def help(self):
        print("1 - Create Account \n2 - Login \n0 - exit")

    def execute(self):
        self.help()
        while True:
            print("")
            command = input("Command: ")
            if command == "0":
                break
            elif command == "1":  
                self.create_account()
            elif command == "2":
                self.login()
            elif command == "5":
                print(self.data.view_all_accounts())
            else: 
                self.help()

Application().execute()
        