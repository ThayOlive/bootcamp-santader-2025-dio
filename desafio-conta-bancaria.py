
menu = """
    ########## MENU ##########

    [1] - Depositar
    [2] - Sacar 
    [3] - Extrato
    [0] - Sair

"""

saldo = 0
numero_saques = 0
extrato = ""
limite = 500
LIMIT_SAQUE = 3

while True:
    opcao = input(menu)

    if opcao == '1':
        deposito = float(input("Digite o valor do depósito:"))
        if deposito < 0:
            print("Valor inválido. Apenas valores positivos.")
        else:
            saldo += deposito
            extrato += f'Deposito: R$ {deposito:.2f}\n'

    elif opcao == '2':
        if numero_saques == LIMIT_SAQUE:
             print("Você ultrapassou o limite de saques.")
        else:
            valor = float(input("Digite o valor do saque:"))
            if valor > limite:
                    print("Você ultrapassou o limite de saque diário. Tente outro valor.")
                    
            elif saldo < valor:
                print("Valor insuficiente para saque. ")
            else:
                saldo -= valor
                numero_saques += 1  
                extrato += f'Saque: R$ {valor:.2f}\n'

    elif opcao == "3":
        print(" =========== EXTRATO =========== ")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f'SALDO TOTAL R$: {saldo:.2f}')
        print("================================")

    elif opcao =="0":
        break

    else: 
        print("Operação inválida, por favor selecione novamente a operação desejada.")
