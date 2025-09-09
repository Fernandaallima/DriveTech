import sqlite3

DB_NAME = "oficina.db"  # Nome do banco adaptado

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabelas():
    con = conectar()
    cur = con.cursor()

    # Tabela de clientes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            email TEXT,
            cpf TEXT UNIQUE
        )
    """)

    # Tabela de veículos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            marca TEXT,
            modelo TEXT,
            ano INTEGER,
            placa TEXT UNIQUE,
            km_atual INTEGER,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id)
        )
    """)

    # Tabela de manutenções
    cur.execute("""
        CREATE TABLE IF NOT EXISTS manutencoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veiculo_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            data TEXT NOT NULL,
            km_realizada INTEGER,
            km_proxima INTEGER,
            data_proxima TEXT,
            FOREIGN KEY(veiculo_id) REFERENCES veiculos(id)
        )
    """)

    con.commit()
    con.close()
