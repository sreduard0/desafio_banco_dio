import json
import os
import getpass
from datetime import datetime

class BankApp:
    def __init__(self):
        self.logado = False
        self.usuario = []
        self.AGENCIA = 3378
        self.CONTA = 2525

    def screen_clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def deposito(self):
        self.screen_clear()
        print("=============================================")
        print("                  DEPÓSITO                   ")
        print("=============================================")
        valor = float(input("Valor do depósito: "))
        if valor > 0:
            with open("DB_ACCOUNT_BANK.json", "r") as account:
                user_account = json.load(account)
            with open("DB_ACCOUNT_BANK.json", "w") as account:
                user_account[self.usuario[0]]["saldo"] += valor
                user_account[self.usuario[0]]["historico"].append([datetime.now().strftime('%d/%m/%Y'), valor, 'deposito'])
                json.dump(user_account, account)
            self.screen_clear()
            print("=============================================")
            print("              DEPÓSITO BEM SUCEDIDO!         ")
            print("                  R$", valor)
            print("=============================================")
        else:
            self.screen_clear()
            print("Você está tentando depositar um valor incorreto!")
            print("\n")

    def saque(self):
        self.screen_clear()
        print("=============================================")
        print("                  SAQUE                   ")
        print("=============================================")
        with open("DB_ACCOUNT_BANK.json", "r") as account:
            user_account = json.load(account)
        print("SALDO                             :", user_account[self.usuario[0]]["saldo"])
        print("_____________________________________________")
        valor = input("Valor do saque: ")
        if valor == '':
            print("Digite um valor!")
            self.saque()
            return
        valor = float(valor)
        if valor < 0:
            print("Valor de saque inválido!")
            return
        if valor > user_account[self.usuario[0]]["saldo"]:
            print("Saldo insuficiente!")
            return

        if valor > 500:
            print("Valor de saque deve ser menor que R$500!")
            return

        contagem = sum(1 for item in user_account[self.usuario[0]]["historico"] if
                       item[0] == datetime.now().strftime('%d/%m/%Y'))
        if contagem > 3:
            self.screen_clear()
            print("=====================================================")
            print("   VOCÊ ATINGIU A QUANTIDADE MAXÍMA DE SAQUES HOJE   ")
            print("               LIMITE MAXÍMO 3 SAQUES                ")
            print("=====================================================")
            return

        with open("DB_ACCOUNT_BANK.json", "w") as account:
            user_account[self.usuario[0]]["saldo"] -= valor
            user_account[self.usuario[0]]["historico"].append([datetime.now().strftime('%d/%m/%Y'), valor, 'saque   '])
            json.dump(user_account, account)
        self.screen_clear()
        print("=============================================")
        print("              SAQUE BEM SUCEDIDO!            ")
        print("                  R$", valor)
        print("        LIMITE DE SAQUES RESTANTES: ", (3 - contagem))
        print("=============================================")

    def extrato(self):
        self.screen_clear()
        print("=============================================")
        print("                  EXTRATO                    ")
        print("=============================================")
        with open("DB_ACCOUNT_BANK.json", "r") as account:
            user_account = json.load(account)
        print("AÇÃO                VALOR                DATA")
        for historico in user_account[self.usuario[0]]["historico"]:
            print(historico[2], "          ", historico[1], "        ", historico[0])
        print("=============================================")
        print("SALDO____________________:", user_account[self.usuario[0]]["saldo"])
        print("=============================================")

    def form_login(self, option):
        self.screen_clear()
        if option == '1':
            print("\n")
            print("=============================================")
            print("                    LOGIN                    ")
            print("=============================================")
            with open("DB_USERS_BANK.json", "r") as usuarios:
                data = json.load(usuarios)

            login = input("Digite seu login: ")
            senha = getpass.getpass("Digite sua senha: ")

            if login in data.keys() and data[login][1] == senha:
                self.usuario.append(data[login][0])
                self.usuario.append(data[login][2])
                return True

            else:
                self.screen_clear()
                print("=============================================")
                print("     Seu login ou senha estão incorretos.    ")
                print("=============================================")
                print("\n")
                input("Pressione <ENTER> para voltar ao menu inicial")
                return False

        elif option == '2':
            print("\n")
            print("=============================================")
            print("                  CADASTRO                   ")
            print("=============================================")
            with open("DB_USERS_BANK.json", "r") as usuarios:
                data = json.load(usuarios)

            nome = input("Digite seu nome completo: ")

            login = input("Digite seu login: ")
            while len(login) < 3:
                print("Seu login é muito curto.")
                login = input("Digite novamente: ")
            if login in data.keys():
                login_existe = True
                while login_existe == True:
                    if login in data.keys():
                        print("Seu login já está em uso!")
                        login = input("Digite novamente: ")
                        login_existe = True
                    else:
                        login_existe = False

            senha = input("Digite uma senha ( Com no mínimo 4 dígitos ): ")
            while len(senha) < 4:
                print("Sua senha é menor que 4 dígitos.")
                senha = input("Digite novamente: ")

            with open("DB_USERS_BANK.json", "w") as usuarios:
                data[login] = [login, senha, nome.upper()]
                json.dump(data, usuarios)

            with open("DB_ACCOUNT_BANK.json", "r") as accounts:
                new_account = json.load(accounts)

            with open("DB_ACCOUNT_BANK.json", "w") as accounts:
                new_account[login] = {
                    "saldo": 0,
                    "historico": []
                }
                json.dump(new_account, accounts)

            self.screen_clear()
            print("=============================================")
            print("          Obrigado por se cadastrar!         ")
            print("         Você já pode fazer seu login.       ")
            print("=============================================")
            print("\n")
            input("Pressione <enter> para continuar")
            return False

        elif option == '3':
            exit()
        else:
            print("=============================================")
            print("        Ola, seja bem vindo ao PyBank        ")
            print("=============================================")
            print(" 1 - FAZER LOGIN                             ")
            print(" 2 - CADASTRAR-SE                            ")
            print(" 3 - SAIR DO APP                             ")
            print("=============================================")
            option = input("OPÇÃO INVALIDA! DIGITE NOVAMENTE:   ")
            self.form_login(option)

    def login(self):
        while self.logado == False:
            self.screen_clear()
            print("=============================================")
            print("        Ola, seja bem vindo ao PyBank        ")
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
        if action == '1':
            self.saque()
        elif action == '2':
            self.deposito()
        elif action == '3':
            self.extrato()
        elif action == '4':
            self.logout()
        else:
            print("AÇÃO INVALIDA! TENTE NOVAMENTE")

    def run(self):
        close = ''
        while close == "":
            self.login()
            self.screen_clear()
            print("=============================================")
            print("################ Olá, " + self.usuario[1] + " ###############")
            print("# AGENCIA: " + str(self.AGENCIA) + "-9                           #")
            print("# CONTA: " + str(self.CONTA) + "-9                             #")
            print("#############################################")
            print("\n")
            print(" 1 - SACAR                                   ")
            print(" 2 - DEPOSITAR                               ")
            print(" 3 - EXTRATO                                 ")
            print(" 4 - SAIR                                  ")
            print("=============================================")

            action = input("O QUE DESEJA FAZER?: ")
            self.select_action(action)
            print("\n")
            close = input("Precione 'ENTER' para voltar para o menu inicial.")


bank = BankApp()
bank.run()
