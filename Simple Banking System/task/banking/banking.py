import random, sys, sqlite3


class Bank:
    def __init__(self):
        self.seed = random.seed()

    def menu1(self):
        print("1. Create an account", "2. Log into account", "0. Exit", sep="\n")
        return input()

    def create_acc(self):
        self.number = (400000000000000 + (random.randint(0000000000, 999999999)))
        self.number = self.append(str(self.number))
        self.number = int(self.number)
        self.pin = random.randint(1000, 9999)
        self.sql_insert(self.number, self.pin)
        return print('Your card has been created', f"Your card number:\n{self.number}", f"Your card PIN:\n{self.pin}", sep="\n")

    def validation(self,num, pin):
        self.conn = sqlite3.connect("card.s3db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            'SELECT number FROM card WHERE number = ? AND pin = ?', (num, pin)
        )
        self.result = self.cur.fetchone()
        self.conn.commit()
        self.conn.close()
        return True if self.result else False

    def insimenu(self):
        print("1. Balance", "2. Add income", "3. Do transfer", "4. Close account", "5. Log out", "0. Exit", sep="\n")
        self.choice = input()
        return self.choice

    def checksum(self, string):
        self.digits = list(map(int, string))
        self.odd_sum = sum(self.digits[-1::-2])
        self.even_sum = sum([sum(divmod(2 * d, 10)) for d in self.digits[-2::-2]])
        return (self.odd_sum + self.even_sum) % 10

    def verify(self, string):
        return (self.checksum(string) == 0)

    def generate(self, string):
        self.cksum = self.checksum(string + '0')
        return (10 - self.cksum) % 10

    def append(self, string):
        return string + str(self.generate(string))

    @staticmethod
    def createconn():
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS card(id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
        conn.commit()
        conn.close()

    @staticmethod
    def checkbalance(num, passw):
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("SELECT balance FROM card WHERE number =? AND pin=?", (num, passw))
        res = cur.fetchone()
        return res

    @staticmethod
    def addincome(num):
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        income = int(input("Enter income:\n"))
        cur.execute("UPDATE card SET balance = (balance + ?) WHERE number=?", (income, num))
        conn.commit()
        conn.close()
        return print("Income was added!")

    def transfer(self, num, card):
        self.sender = num
        self.receiver = card
        self.balance = boa.sql_balance(self.sender)
        if not boa.verify(self.receiver):
            return print("Probably you made a mistake in the card number. Please try again!")
        if self.sender == self.receiver:
            return print("You can't transfer money to the same account!")
        self.conn = sqlite3.connect("card.s3db")
        self.cur = self.conn.cursor()
        self.cur.execute("Select * FROM card WHERE number =?", (self.receiver,))
        self.res = self.cur.fetchone()
        if not self.res:
            return print("Such a card does not exist.")
        self.amount = int(input("Enter how much money you want to transfer:\n"))
        self.cur.execute("SELECT balance FROM card WHERE number = ?", (self.sender,))
        self.sender_cash = self.cur.fetchone()
        if self.sender_cash[0] - self.amount < 0:
            return print("Not enough money!")
        self.cur.execute("UPDATE card SET balance = (balance - ?) WHERE number =?", (self.amount, self.sender,))
        self.conn.commit()
        self.cur.execute("UPDATE card SET balance = (balance + ?) WHERE number =?", (self.amount, self.receiver,))
        self.conn.commit()
        self.cur.execute("SELECT balance FROM card WHERE number = ?", (self.receiver,))
        self.sender_cash = self.cur.fetchone()
        return print("Success!")

    @staticmethod
    def delet(num):
        conn = sqlite3.connect("card.s3db")
        cur = conn.cursor()
        cur.execute("DELETE FROM card WHERE number=?", (num,))
        conn.commit()

    @staticmethod
    def sql_insert(card, pin):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        cur.execute(
            f'INSERT INTO'
            f'  card(number, pin)'
            f'VALUES'
            f'  ({card}, {pin})'
        )
        conn.commit()
        conn.close()

    @staticmethod
    def sql_balance(num):
        value = (num,)
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        cur.execute(
            'SELECT balance FROM card WHERE number = ?', value
        )
        balance = cur.fetchone()
        conn.commit()
        conn.close()
        return balance[0]


if __name__ == "__main__":
    Bank.createconn()
    while True:
        boa = Bank()
        user_choice = boa.menu1()
        if user_choice == "1":
            boa.create_acc()
            continue
        elif user_choice == "2":
            num = input("Enter your card number:\n")
            passw = input("Enter your PIN:\n")
            check = boa.validation(num, passw)
            print(check)
            if check is False :
                print("Wrong card number or PIN!")
                continue
            else:
                print("You have successfully logged in!")
                while True:
                    choice = boa.insimenu()
                    if choice == "1":
                        res = boa.checkbalance(num, passw)
                        if res:
                            print(f"Balance: {res}")
                            continue
                        else:
                            continue
                    elif choice == "2":
                        boa.addincome(num)
                        continue
                    elif choice == "3":
                        card = input("Enter card number:\n")
                        boa.transfer(num, card)
                        continue
                    elif choice == "4":
                        boa.delet(num)
                        break
                    elif choice == "5":
                        print("You have successfully logged out!")
                        break
                    else:
                        print("Bye!")
                        sys.exit(0)
        elif user_choice == "0":
            print("Bye!")
            sys.exit(0)

