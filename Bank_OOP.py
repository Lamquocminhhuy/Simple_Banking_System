from random import randint
import sqlite3


class Bank:
    def __init__(self):
        self.logged_in = False
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.create_table()
        self.menu()

    def create_table(self):
        sql_create_card_table = """CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT,
        pin TEXT, balance INTEGER DEFAULT 0); """
        self.cur.execute(sql_create_card_table)
        self.conn.commit()

    def create_card(self, id_, number, pin, balance):
        sql_insert_card = """INSERT INTO card (id, number, pin, balance) VALUES (?, ?, ?, ?); """
        data_tuple = (id_, number, pin, balance)
        self.cur.execute(sql_insert_card, data_tuple)
        self.conn.commit()

    def gen_id(self):
        query = """SELECT id FROM card ORDER BY id DESC LIMIT 1;"""
        self.cur.execute(query)
        records = self.cur.fetchall()
        try:
            return records[0][0] + 1
        except IndexError:
            return 1

    def read_card(self, card, pin):
        query = """SELECT number, pin FROM card WHERE number = ? AND pin = ?"""
        data_tuple = (card, pin)
        self.cur.execute(query, data_tuple)
        rows = self.cur.fetchone()
        return rows

    def menu(self):
        while not self.logged_in:
            print('1. Create an account\n2. Log into account\n0. Exit')
            choice = input()
            if choice == '1':
                self.create()
            elif choice == '2':
                self.login()
            elif choice == '0':
                print('\nBye!')
                self.cur.close()
                self.conn.close()
                quit()

    def account_menu(self):
        while self.logged_in:
            print('1. Balance\n2. Log out\n0. Exit')
            choice = input()
            if choice == '1':
                print('\nBalance: 0\n')
            elif choice == '2':
                self.logged_in = False
                print('\nYou have successfully logged out!\n')
            elif choice == '0':
                print('\nBye!')
                self.cur.close()
                self.conn.close()
                quit()

    def create(self):
        print()
        id_ = self.gen_id()
        card = self.luhn_alg()
        pin = str.zfill(str(randint(0000, 9999)), 4)
        self.create_card(id_, card, pin, 0)
        print(f'Your card has been created\nYour card number:\n{card}\nYour card PIN:\n{pin}\n')

    def login(self):
        print('\nEnter your card number:')
        card = input()
        print('Enter your PIN:')
        pin = input()
        cards = self.read_card(card, pin)
        if cards:
            print('\nYou have successfully logged in!\n')
            self.logged_in = True
            self.account_menu()
        else:
            print('\nWrong card number or Pin!\n')

    def luhn_alg(self):
        card = '400000' + str.zfill(str(randint(000000000, 999999999)), 9)
        card_check = [int(i) for i in card]
        for index, _ in enumerate(card_check):
            if index % 2 == 0:
                card_check[index] *= 2
            if card_check[index] > 9:
                card_check[index] -= 9
        check_sum = str((10 - sum(card_check) % 10) % 10)
        card += check_sum
        return card


if __name__ == '__main__':
    stage_3 = Bank()
