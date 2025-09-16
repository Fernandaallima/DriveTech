# models.py
import sqlite3
from database import conectar

# Classe base: Pessoa
class Pessoa:
    def __init__(self, nome, telefone=None, email=None, cpf=None):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.cpf = cpf


# Subclasse: Cliente
class Cliente(Pessoa):
    def __init__(self, nome, telefone=None, email=None, cpf=None):
        super().__init__(nome, telefone, email, cpf)

    def adicionar(self):
        con = conectar()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO clientes (nome, telefone, email, cpf) VALUES (?, ?, ?, ?)",
            (self.nome, self.telefone, self.email, self.cpf)
        )
        con.commit()
        con.close()

    @staticmethod
    def listar():
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM clientes")
        dados = cur.fetchall()
        con.close()
        return dados

    @staticmethod
    def atualizar(cliente_id, nome=None, telefone=None, email=None):
        con = conectar()
        cur = con.cursor()
        if nome:
            cur.execute("UPDATE clientes SET nome=? WHERE id=?", (nome, cliente_id))
        if telefone:
            cur.execute("UPDATE clientes SET telefone=? WHERE id=?", (telefone, cliente_id))
        if email:
            cur.execute("UPDATE clientes SET email=? WHERE id=?", (email, cliente_id))
        con.commit()
        con.close()

    @staticmethod
    def deletar(cliente_id):
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
        con.commit()
        con.close()

# Classe: Veiculo
class Veiculo:
    def __init__(self, cliente_id, marca, modelo, ano, placa, km_atual=0):
        self.cliente_id = cliente_id
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.placa = placa
        self.km_atual = km_atual

    def adicionar(self):
        con = conectar()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO veiculos (cliente_id, marca, modelo, ano, placa, km_atual) VALUES (?, ?, ?, ?, ?, ?)",
            (self.cliente_id, self.marca, self.modelo, self.ano, self.placa, self.km_atual)
        )
        con.commit()
        con.close()

    @staticmethod
    def listar():
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM veiculos")
        dados = cur.fetchall()
        con.close()
        return dados

# Classe: Manutencao
class Manutencao:
    def __init__(self, veiculo_id, descricao, data, km_realizada, km_proxima=None, data_proxima=None):
        self.veiculo_id = veiculo_id
        self.descricao = descricao
        self.data = data
        self.km_realizada = km_realizada
        self.km_proxima = km_proxima
        self.data_proxima = data_proxima

    def adicionar(self):
        con = conectar()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO manutencoes (veiculo_id, descricao, data, km_realizada, km_proxima, data_proxima) VALUES (?, ?, ?, ?, ?, ?)",
            (self.veiculo_id, self.descricao, self.data, self.km_realizada, self.km_proxima, self.data_proxima)
        )
        con.commit()
        con.close()

    @staticmethod
    def listar():
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM manutencoes")
        dados = cur.fetchall()
        con.close()
        return dados


# Classes de Usuário e Admin
class Usuario:
    def __init__(self, nome, email, senha, nivel="usuario"):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.nivel = nivel

    def adicionar(self):
        con = conectar()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO usuarios (nome, email, senha, nivel) VALUES (?, ?, ?, ?)",
            (self.nome, self.email, self.senha, self.nivel)
        )
        con.commit()
        con.close()

    @staticmethod
    def listar():
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id, nome, email, nivel FROM usuarios")
        dados = cur.fetchall()
        con.close()
        return dados

class Administrador(Usuario):
    def __init__(self, nome, email, senha):
        super().__init__(nome, email, senha, nivel="admin")
