import tkinter as tk
from tkinter import messagebox
import sqlite3

# Conexão com o banco
DB_NAME = "oficina.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def salvar_dados():
    # Captura os dados do formulário
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    telefone = entry_telefone.get()
    email = entry_email.get()
    endereco = entry_endereco.get()

    marca = entry_marca.get()
    modelo = entry_modelo.get()
    placa = entry_placa.get()
    ano = entry_ano.get()
    cor = entry_cor.get()

    if not nome or not cpf or not placa:
        messagebox.showerror("Erro", "Nome, CPF/CNPJ e Placa são obrigatórios.")
        return

    try:
        con = conectar()
        cur = con.cursor()

        # Inserir cliente
        cur.execute("""
            INSERT INTO clientes (nome, telefone, email, cpf, endereco)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, telefone, email, cpf, endereco))

        cliente_id = cur.lastrowid

        # Inserir veículo
        cur.execute("""
            INSERT INTO veiculos (cliente_id, marca, modelo, placa, ano, cor)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (cliente_id, marca, modelo, placa, ano, cor))

        con.commit()
        con.close()

        messagebox.showinfo("Sucesso", "Cliente e veículo cadastrados com sucesso!")
        limpar_campos()

    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "CPF ou Placa já cadastrados.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def limpar_campos():
    for entry in entries:
        entry.delete(0, tk.END)

# Interface gráfica
root = tk.Tk()
root.title("Cadastro de Veículo e Cliente - Drive Tech")
root.geometry("800x500")
root.configure(bg="#F5F5F5")

# Título
titulo = tk.Label(root, text="Cadastro", font=("Arial Black", 20), bg="#F5F5F5")
titulo.pack(pady=10)

form_frame = tk.Frame(root, bg="#F5F5F5")
form_frame.pack(pady=10)

# ---------------- DADOS DO CLIENTE ----------------
cliente_frame = tk.LabelFrame(form_frame, text="Dados do cliente", padx=10, pady=10, bg="white")
cliente_frame.grid(row=0, column=0, padx=20)

tk.Label(cliente_frame, text="Nome:", bg="white").grid(row=0, column=0, sticky="e")
entry_nome = tk.Entry(cliente_frame, width=30)
entry_nome.grid(row=0, column=1)

tk.Label(cliente_frame, text="CPF/CNPJ:", bg="white").grid(row=1, column=0, sticky="e")
entry_cpf = tk.Entry(cliente_frame, width=30)
entry_cpf.grid(row=1, column=1)

tk.Label(cliente_frame, text="Telefone:", bg="white").grid(row=2, column=0, sticky="e")
entry_telefone = tk.Entry(cliente_frame, width=30)
entry_telefone.grid(row=2, column=1)

tk.Label(cliente_frame, text="Email:", bg="white").grid(row=3, column=0, sticky="e")
entry_email = tk.Entry(cliente_frame, width=30)
entry_email.grid(row=3, column=1)

tk.Label(cliente_frame, text="Endereço:", bg="white").grid(row=4, column=0, sticky="e")
entry_endereco = tk.Entry(cliente_frame, width=30)
entry_endereco.grid(row=4, column=1)

# ---------------- DADOS DO VEÍCULO ----------------
veiculo_frame = tk.LabelFrame(form_frame, text="Dados do veículo", padx=10, pady=10, bg="white")
veiculo_frame.grid(row=0, column=1, padx=20)

tk.Label(veiculo_frame, text="Marca:", bg="white").grid(row=0, column=0, sticky="e")
entry_marca = tk.Entry(veiculo_frame, width=30)
entry_marca.grid(row=0, column=1)

tk.Label(veiculo_frame, text="Modelo:", bg="white").grid(row=1, column=0, sticky="e")
entry_modelo = tk.Entry(veiculo_frame, width=30)
entry_modelo.grid(row=1, column=1)

tk.Label(veiculo_frame, text="Placa:", bg="white").grid(row=2, column=0, sticky="e")
entry_placa = tk.Entry(veiculo_frame, width=30)
entry_placa.grid(row=2, column=1)

tk.Label(veiculo_frame, text="Ano:", bg="white").grid(row=3, column=0, sticky="e")
entry_ano = tk.Entry(veiculo_frame, width=30)
entry_ano.grid(row=3, column=1)

tk.Label(veiculo_frame, text="Cor:", bg="white").grid(row=4, column=0, sticky="e")
entry_cor = tk.Entry(veiculo_frame, width=30)
entry_cor.grid(row=4, column=1)

# Lista de entradas para limpar depois
entries = [
    entry_nome, entry_cpf, entry_telefone, entry_email, entry_endereco,
    entry_marca, entry_modelo, entry_placa, entry_ano, entry_cor
]

# Botão de cadastro
btn_cadastrar = tk.Button(root, text="Cadastrar", command=salvar_dados, bg="black", fg="white", width=15, height=2)
btn_cadastrar.pack(pady=20)

root.mainloop()
