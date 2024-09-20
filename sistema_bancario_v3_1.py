from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty

class Cliente:
    def __init__(self, endereco) -> None:
        self.endereco = endereco
        self.contas = []

    def realizar_trasacao(self, conta, transacao):
        transacao.realizar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco) -> None:
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente) -> None:
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._clente = cliente
        self._historico = Historico()

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
        return self._clente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        saldo_induficiente = valor > saldo

        if saldo_induficiente:
            print(f"Você não tem saldo suficiente para esse saque. Saldo: R$ {saldo:.2f}")
        elif valor > 0:
            self._saldo -= valor
            print(f"Saque realizado com sucesso. Saldo: R$ {saldo:.2f}")
            return True
        else:
            print("O valor informado para saque não pode ser negativo!")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Saque realizado com sucesso. Saldo: R$ {saldo:.2f}")
            return True
        else:
            print("O valor informado para depósito não pode ser negativo!")

        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3) -> None:
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"]  == Saque.__name__])

        limite_excedido = valor > self.limite
        numero_saques_excedido = numero_saques >= self.limite_saque

        if limite_excedido:
            print(f"O valor do saque é maior que o limite diário. Limite: {limite}")
        elif numero_saques_excedido:
            print(f"Você alcançou o número máximo de saques. Limite: {limite_saques}")
        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self) -> None:
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

#interface
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self): pass

    @abstractclassmethod
    def registrar(self, conta): pass


class Saque(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)