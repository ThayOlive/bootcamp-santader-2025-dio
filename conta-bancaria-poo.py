from abc import ABC, abstractmethod
from datetime import datetime

#Parte um do desafio (Aplicando conceitos de POO)

class Cliente:
    def __init__(self, endereço):
        self.endereço = endereço
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registar(conta)
    
    def add_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereço):
        super().__init__(endereço)
        self._nome = nome
        self._cpf = cpf 
        self._data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero_conta, cliente):
        self._saldo = 0
        self._numero_conta= numero_conta
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero_conta):
        return cls(numero_conta,cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero_conta(self):
        return self._numero_conta
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
     
    def sacar(self,valor):
        saldo = self._saldo
        valor_insuficiente = saldo < valor
        if valor_insuficiente:
            print("Operação falhou. Saldo insuficiente para saque.")
        elif valor > 0:
            saldo -= valor 
            print("Saldo realizado com sucesso!")
            return True
        else:
            print("Operação falhou. Valor inválido para saque.")
        
        return False

    def depositar(self,valor):
        saldo = self._saldo
        if valor > 0:
            saldo += valor
            print("Deposito realizado com sucesso.")
            
        else:
            print("Operação falhou. Valor inválido.")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numeros_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])
        
        limite_excedido = valor > self.limite
        limite_saques_excedido = numeros_saques >= self.limite_saques

        if limite_excedido:
            print("Operação inválida. Valor acima do limite da conta.")
        elif limite_saques_excedido:
            print("Operação falhou. Limite de saques diários atingido.")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"Agencia: {self.agencia} Conta-corrente: {self.numero} Titular: {self.cliente.nome}"
           
class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes

    def add_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-$m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registar(self,conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor 
    @property
    def valor(self):
        return self._valor
    
    def registar(self, conta):
        transacao = conta.despositar(self.valor)
        if transacao:
            conta.historico.add_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor 
    
    @property
    def valor(self):
        return self._valor
    
    def registar(self, conta):
        transacao = conta.sacar(self.valor)
        if transacao:
            conta.historico.add_transacao(self)

# Parte dois do desafio (DESAFIO EXTRA)

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
    
def buscar_cliente_por_cpf(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def buscar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta")
        return
    
    #Implementar opção de escolha de contas
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente:")
    cliente = buscar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    valor = float(input("Digite um valor para depósito:"))
    transacao = Deposito(valor)

    conta = buscar_conta_cliente(cliente)
    if not conta:
        print("Não há conta registrada")
        return
    
    cliente.realizar_transacao(conta,transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente:")
    cliente = buscar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    valor = float(input("Digite um valor para saque:"))
    transacao = Saque(valor)

    conta = buscar_conta_cliente(cliente)
    if not conta:
        print("Não há conta registrada")
        return
    
    cliente.realizar_transacao(conta,transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente:")
    cliente = buscar_cliente_por_cpf(cpf)
    if not cliente:
        print("Cliente não encontrado")
        return
    
    conta = buscar_conta_cliente(cliente)
    if not conta:
        print("Não há conta registrada")
        return
    
    print("==================== EXTRATO ====================")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Não foram registradas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: R${transacao['valor']:.2f}"

    print(extrato)
    print(f"Saldo total: R$ {conta.saldo:.2f}")
    print('===============================================')

def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente:")
    cliente = buscar_cliente_por_cpf(cpf, clientes)
    if cliente:
        print("Cliente já existe nesse CPF.")
        return
    
    nome = input("Digite o nome do usuário:")
    data_nascimento = input("Digite a data de nascimento:")
    cpf = input("Digite o CPF do usuário:")
    endereço = input("Digite o endereço do usuário(logradouro - nro - bairro - cidade/sigla estado):")
    cliente = PessoaFisica(nome=nome,data_nascimento=data_nascimento,cpf=cpf,endereço=endereço)

    clientes.append(cliente)
    print("Cliente criado com sucesso!")

def criar_conta_corrente(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente:")
    cliente = buscar_cliente_por_cpf(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado")
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero_conta=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("Conta criada com sucesso!")

def exibir_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(str(conta))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == '1':
           depositar(clientes)

        elif opcao == '2':
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
           criar_cliente(clientes)

        elif opcao == "5":
            numero_conta = len(contas)+1
            criar_conta_corrente(numero_conta, clientes, contas)

        elif opcao == "6":
            exibir_contas(contas)
        
        elif opcao =="0":
            break

        else: 
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
