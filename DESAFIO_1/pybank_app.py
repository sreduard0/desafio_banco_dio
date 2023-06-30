import json
import os
import getpass
import sys
from datetime import datetime
logado = False
close = ''
usuario = []
def screen_clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def deposito():
    screen_clear()
    print("=============================================")
    print("                  DEPÓSITO                   ")
    print("=============================================")
    valor = float(input("Valor do depósito: "))
    if valor > 0:    
        with open("DB_ACCOUNT_BANK.json","r") as account:
            user_account = json.load(account)
        with open("DB_ACCOUNT_BANK.json","w") as account:
            user_account[usuario[0]]["saldo"] = user_account[usuario[0]]["saldo"]+valor
            user_account[usuario[0]]["historico"] += [[datetime.now().strftime('%d/%m/%Y'), valor,'deposito']]
            json.dump(user_account,account)
        screen_clear()
        print("=============================================")
        print("              DEPÓSITO BEM SUCEDIDO!         ")
        print("                  R$",valor)
        print("=============================================")
    else:
        screen_clear()
        print("Você está tentando depositar um valor incorreto!")
        print("\n")

def saque():
    screen_clear()
    print("=============================================")
    print("                  SAQUE                   ")
    print("=============================================")
    with open("DB_ACCOUNT_BANK.json","r") as account:
        user_account = json.load(account)
    print("SALDO                             :",user_account[usuario[0]]["saldo"])
    print("_____________________________________________")
    valor = input("Valor do saque: ")
    if valor == '':
        print("Digite um valor!")
        saque()
        return
    valor = float(valor)
    if valor < 0:
        print("Valor de saque inválido!")
        return
    if valor > user_account[usuario[0]]["saldo"]:
        print("Saldo insuficiente!")
        return
    
    if valor > 500:
        print("Valor de saque deve ser menor que R$500!")
        return
    
    
    contagem = sum(1 for item in user_account[usuario[0]]["historico"] if item[0] == datetime.now().strftime('%d/%m/%Y'))
    if contagem  > 3:
        screen_clear()
        print("=====================================================")
        print("   VOCÊ ATINGIU A QUANTIDADE MAXÍMA DE SAQUES HOJE   ")
        print("               LIMITE MAXÍMO 3 SAQUES                ")
        print("=====================================================")
        return
        
    with open("DB_ACCOUNT_BANK.json","w") as account:
        user_account[usuario[0]]["saldo"] = user_account[usuario[0]]["saldo"]-valor
        user_account[usuario[0]]["historico"] += [[datetime.now().strftime('%d/%m/%Y'), valor,'saque   ']]
        json.dump(user_account,account)
    screen_clear()
    print("=============================================")
    print("              SAQUE BEM SUCEDIDO!            ")
    print("                  R$",valor)
    print("        LIMITE DE SAQUES RESTANTES: ",(3-contagem))
    print("=============================================")
   

def extrato():
    screen_clear()
    print("=============================================")
    print("                  EXTRATO                    ")
    print("=============================================")
    with open("DB_ACCOUNT_BANK.json","r") as account:
        user_account = json.load(account)
    print("AÇÃO                VALOR                DATA")
    for historico in user_account[usuario[0]]["historico"]: 
        print(historico[2],"          ",historico[1],"        ",historico[0])
    print("=============================================")
    print("SALDO____________________:",user_account[usuario[0]]["saldo"])
    print("=============================================")
    
def form_login(option):
    screen_clear()    
    match (option):
        case '1': 
            print("\n")
            print("=============================================")
            print("                    LOGIN                    ")
            print("=============================================")
            with open("DB_USERS_BANK.json","r") as usuarios:
                data = json.load(usuarios)
                
            login = input("Digite seu login: ")
            senha = getpass.getpass("Digite sua senha: ")
            
            if login in data.keys() and data[login][1] == senha:
                usuario.append(data[login][0])
                usuario.append(data[login][2])
                return True
                
            else:
                screen_clear()
                print("=============================================")
                print("     Seu login ou senha estão incorretos.    ")
                print("=============================================")
                print("\n")
                input("Pressione <ENTER> para voltar ao menu inicial")
                return False
            
        case '2':  
            print("\n")
            print("=============================================")
            print("                  CADASTRO                   ")
            print("=============================================")
            with open("DB_USERS_BANK.json","r") as usuarios:
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
                        
                    
            senha = input("Digite uma senha ( Com no minimo 4 dígitos ): ")
            while len(senha) < 4:
                print("Sua senha é menor que 4 dígitos.")
                senha = input("Digite novamente: ")
           
            with open("DB_USERS_BANK.json","w") as usuarios:
                data[login] = [login,senha,nome.upper()]
                json.dump(data,usuarios)
                
            with open("DB_ACCOUNT_BANK.json","r") as accounts:
                new_account = json.load(accounts)
    
            with open("DB_ACCOUNT_BANK.json","w") as accounts:
                new_account[login] = {
                    "saldo": 0,
                    "historico":[]
                }
                json.dump(new_account,accounts)
                
            screen_clear()
            print("=============================================")
            print("          Obrigado por se cadastrar!         ")
            print("         Você já pode fazer seu login.       ")
            print("=============================================")
            print("\n")
            input("Pressione <enter> para continuar")
            return False

        case '3':
            sys.exit()
        case _:
            print("=============================================")
            print("        Ola, seja bem vindo ao PyBank        ")
            print("=============================================")
            print(" 1 - FAZER LOGIN                             ")
            print(" 2 - CADASTRAR-SE                            ")
            print(" 3 - SAIR DO APP                             ")
            print("=============================================")
            option = input("OPÇÃO INVALIDA! DIGITE NOVAMENTE:   ")
            form_login(option) 
            
def login():
    global logado
    while logado == False:
        screen_clear()
        print("=============================================")
        print("        Ola, seja bem vindo ao PyBank        ")
        print("=============================================")
        print(" 1 - FAZER LOGIN                             ")
        print(" 2 - CADASTRAR-SE                            ")
        print(" 3 - SAIR DO APP                             ")
        print("=============================================")
        option = input("DIGITE SUA OPÇÃO: ")
        logado = form_login(option)
        
def logout():
    global logado
    logado = False 
    usuario.clear()
    
                
def select_action(action):    
    match (action):
        case '1':  
            saque()    
        case '2': 
            deposito()
        case '3': 
            extrato()    
        case '4': 
            logout()
        case _:
            print("AÇÃO INVALIDA! TENTE NOVAMENTE")
    
while close == "":
    login()
    screen_clear()
    print("=============================================")
    print("############ Olá, "+usuario[1] +" ###########")
    print(" 1 - SACAR                                   ")
    print(" 2 - DEPOSITAR                               ")
    print(" 3 - EXTRATO                                 ")
    print(" 4 - SAIR                                  ")
    print("=============================================")
    
    action = input("O QUE DESEJA FAZER?: ")
    select_action(action)  
    print("\n")
    close = input("Precione 'ENTER' para voltar para o menu inicial.")

# DATA: 28/06/23
# CRIADO POR EDUARDO MARTINS
# DESAFIO DIO/ CERTIFICAÇÃO DE PYTHON
