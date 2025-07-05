usuarios = []
usuario = {} 
contas = []
conta = {}

def menu():
   return input( """
        ########## MENU ##########

        [1] - Depositar
        [2] - Sacar 
        [3] - Extrato
        [4] - Criar usuario
        [5] - Criar conta corrente
        [6] - Contas
        [0] - Sair
        =>
    """)
    

def fazer_deposito(deposito, saldo, extrato, /):
    if deposito < 0:
        print("Valor inválido. Apenas valores positivos.")
    else:
        saldo += deposito
        extrato += f'Deposito: R$ {deposito:.2f}\n'
    return saldo, extrato

def fazer_saque(*, saldo, valor, extrato, limite, limite_saques, numero_saques):
    if numero_saques == limite_saques:
        print("Você ultrapassou o limite de saques.")
    else:
        if valor > limite:     
            print("Você ultrapassou o limite de saque diário. Tente outro valor.")              
        elif saldo < valor:
            print("Valor insuficiente para saque. ")
        else:
            saldo -= valor
            numero_saques += 1  
            extrato += f'Saque: R$ {valor:.2f}\n'
    return saldo, extrato, numero_saques

def exibir_extrato(saldo,/, *, extrato):
    print(" =========== EXTRATO =========== ")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f'SALDO TOTAL R$: {saldo:.2f}')
    print("================================")
    
def criar_usuario(**kwargs):      
    usuario = kwargs
    usuarios.append(usuario)
    print(usuarios)

def buscar_usuario_por_cpf(cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def criar_conta_corrente(agencia, num_conta, cpf):
    usuario = buscar_usuario_por_cpf(cpf)
    if usuario:
        conta = {"agencia": agencia, "num_conta": num_conta, "usuario": usuario}
        contas.append(conta)
        print("Conta criada com sucesso")
        return conta
    else:
        print("Usuário não encontrado")
        return None

def exibir_contas(contas):
    for conta in contas:
        linha = f"""
Agência:\t{conta['agencia']}
Conta:\t{conta['num_conta']} 
Titular:\t{conta['usuario']['nome']}
"""
        print('=' *100)
        print(linha)

def main():
    saldo = 0
    numero_saques = 0
    extrato = ""
    limite = 500
    LIMIT_SAQUE = 3
    AGENCIA = "0001"

    while True:
        opcao = menu()
        if opcao == '1':
            deposito = float(input("Digite o valor do depósito:"))
            saldo, extrato = fazer_deposito(deposito, saldo, extrato)
        elif opcao == '2':
            valor = float(input("Digite o valor do saque:"))
            saldo, extrato, numero_saques = fazer_saque(
                saldo=saldo, 
                valor=valor, 
                extrato=extrato, 
                limite=limite,
                limite_saques= LIMIT_SAQUE, 
                numero_saques=numero_saques)
            
        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)
        elif opcao =="0":
            break
        elif opcao == "4":
            nome = input("Digite o nome do usuário:")
            data_de_nascimento = input("Digite a data de nascimento:")
            cpf = input("Digite o CPF do usuário:")
            usuario_ja_existe = buscar_usuario_por_cpf(cpf)
            if usuario_ja_existe:
                print("Falha. Usuário já existe.")
            else:
                endereço = input("Digite o endereço do usuário(logradouro - nro - bairro - cidade/sigla estado):")
                criar_usuario(nome=nome,data_de_nascimento=data_de_nascimento,cpf=cpf,endereço=endereço)
        elif opcao == "5":
            cpf= input("Digite o cpf do usuario")
            num_conta = len(contas)+1
            criar_conta_corrente(AGENCIA,num_conta, cpf)
        elif opcao == "6":
            exibir_contas(contas)
        else: 
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()