import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class pessoa_fisica(cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n### Operação falhou! Você não tem saldo suficiente. ###")

        elif valor > 0:
            self._saldo -= valor
            numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")

            return True

        else:
            print("\n### Operação falhou! O valor informado é inválido. ###")

        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            
        else:
            print("\n### Operação falhou! O valor informado é inválido. ###")

            return False 
        
        return True


class conta_corrente(conta):
    def __init__(self, numero, cliente, limite_valor=1500, limite_saque=3):
        super().__init__(numero, cliente)
        self._limite_valor = limite_valor
        self._limite_saque = limite_saque

    def sacar(self, valor):
        numeros_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == saque. __name__]
        )

        excedeu_limite = valor > self._limite_valor
        excedeu_saque = numeros_saques >= self._limite_saque

        if excedeu_limite:
            print("\n### Operação falhou! O valor do saque excedeu o limite. ###")

        elif excedeu_saque:
            print("\n### Operação falhou! Número máximo de saques excedido. ###")

        else:
            return super().sacar(valor)
        
        return False
    def __str__(self):
        return f"""\
        Agência:\t{self.agencia}
        C/C:\t\t{self.numero}
        Titular:\t{self.cliente.nome}
        """


class historico:
    def __init__(self):
        self.transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%y %H:%M:%S")
            }
        )


class transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass
    

class saque(transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class deposito(transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [7]\tSair

    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n### Cliente não possui conta! ###")
        return
    #Não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)


    if not cliente:
        print("\n### Cliente não encontrado! ###")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_trasancao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n### Cliente não encontrado! ###")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n### Cliente não encontrado! ###")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadoas movimentações."
    
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n### Já existe cliente com esse CPF! ###")
        return
        

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nº - bairro - cidade/sigla estado): ")

    cliente = pessoa_fisica({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    clientes.append(cliente)

    print("=== Cadastro criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n### Cliente não encontrado, fluxo de criação de conta encerrado! ###")
        return
    
    conta = conta_corrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
