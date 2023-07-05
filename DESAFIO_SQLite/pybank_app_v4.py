import sqlite3
import getpass


class Bank:
    def __init__(self):
        self.db_connection = sqlite3.connect("bank.db")
        self.create_tables()
        self.logado = False
        self.usuario = []

    def create_tables(self):
        cursor = self.db_connection.cursor()

        # Tabela de usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                login TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)

        # Tabela de contas bancárias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                balance REAL NOT NULL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Tabela de histórico de transações
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                amount REAL NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            )
        """)

        self.db_connection.commit()

    def screen_clear(self):
        print("\033[H\033[J")

    def saque(self):
        self.screen_clear()
        cursor = self.db_connection.cursor()
        account_id = self.get_account_id()

        if account_id is None:
            return

        amount = float(input("Digite o valor do saque: "))
        if amount <= 0:
            print("Valor inválido!")
            return

        balance = self.get_account_balance(account_id)
        if balance < amount:
            print("Saldo insuficiente!")
            return

        new_balance = balance - amount

        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
        cursor.execute("INSERT INTO transactions (account_id, action, amount) VALUES (?, 'SAQUE', ?)", (account_id, amount))
        self.db_connection.commit()

        print("Saque realizado com sucesso!")
        print("Novo saldo: R$", new_balance)

    def deposito(self):
        self.screen_clear()
        cursor = self.db_connection.cursor()
        account_id = self.get_account_id()

        if account_id is None:
            return

        amount = float(input("Digite o valor do depósito: "))
        if amount <= 0:
            print("Valor inválido!")
            return

        balance = self.get_account_balance(account_id)
        new_balance = balance + amount

        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
        cursor.execute("INSERT INTO transactions (account_id, action, amount) VALUES (?, 'DEPÓSITO', ?)", (account_id, amount))
        self.db_connection.commit()

        print("Depósito realizado com sucesso!")
        print("Novo saldo: R$", new_balance)

    def extrato(self):
        self.screen_clear()
        cursor = self.db_connection.cursor()
        account_id = self.get_account_id()

        if account_id is None:
            return

        cursor.execute("SELECT * FROM transactions WHERE account_id = ?", (account_id,))
        transactions = cursor.fetchall()

        print("=============================================")
        print("                  EXTRATO                    ")
        print("=============================================")
        print("AÇÃO                VALOR                DATA")

        for transaction in transactions:
            action = transaction[2]
            amount = transaction[3]
            date = transaction[4]
            print(f"{action:12} {amount:20} {date}")

        print("=============================================")

    def get_account_id(self):
        cursor = self.db_connection.cursor()
        login = input("Digite seu login: ")

        cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
        user_id = cursor.fetchone()

        if user_id is None:
            print("Usuário não encontrado!")
            return None

        cursor.execute("SELECT id FROM accounts WHERE user_id = ?", (user_id[0],))
        account_id = cursor.fetchone()

        if account_id is None:
            print("Conta bancária não encontrada!")
            return None

        return account_id[0]

    def get_account_balance(self, account_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
        balance = cursor.fetchone()

        if balance is None:
            return None

        return balance[0]

    def form_login(self, option):
        cursor = self.db_connection.cursor()

        if option == "1":
            login = input("Digite seu login: ")
            password = getpass.getpass("Digite sua senha: ")

            cursor.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password))
            user = cursor.fetchone()

            if user is not None:
                self.usuario = user
                self.logado = True
                return True
            else:
                print("Login ou senha incorretos!")
                return False

        elif option == "2":
            name = input("Digite seu nome: ")
            login = input("Digite um login: ")
            password = getpass.getpass("Digite uma senha: ")

            cursor.execute("INSERT INTO users (name, login, password) VALUES (?, ?, ?)", (name, login, password))
            self.db_connection.commit()

            print("Usuário cadastrado com sucesso!")
            return False

        elif option == "3":
            self.logout()
            return False

        else:
            print("Opção inválida!")
            return False

    def login(self):
        while not self.logado:
            self.screen_clear()
            print("=============================================")
            print("        Ola, seja bem-vindo ao PyBank        ")
            print("=============================================")
            print(" 1 - FAZER LOGIN                             ")
            print(" 2 - CADASTRAR-SE                            ")
            print(" 3 - SAIR DO APP                             ")
            print("=============================================")
            option = input("DIGITE SUA OPÇÃO: ")
            self.logado = self.form_login(option)

    def logout(self):
        self.logado = False
        self.usuario.clear()

    def select_action(self, action):
        if action == "1":
            self.saque()
        elif action == "2":
            self.deposito()
        elif action == "3":
            self.extrato()
        elif action == "4":
            self.logout()
        else:
            print("AÇÃO INVÁLIDA! TENTE NOVAMENTE")

    def run(self):
        close = ""
        while close == "":
            self.login()
            self.screen_clear()
            print("=============================================")
            print("################ Olá, " + self.usuario[1] + " ###############")
            print("# AGENCIA: 2525-9                           #")
            print("# CONTA: 8547-9                             #")
            print("#############################################")
            print("\n")
            print(" 1 - SACAR                                   ")
            print(" 2 - DEPOSITAR                               ")
            print(" 3 - EXTRATO                                 ")
            print(" 4 - LOGOUT                                  ")
            print("\n")
            action = input("DIGITE SUA OPÇÃO: ")
            self.select_action(action)
            print("=============================================")
            close = input("Pressione <ENTER> para continuar ou digite qualquer tecla para sair.")


if __name__ == "__main__":
    bank = Bank()
    bank.run()
