import tkinter as tk
from tkinter import ttk
import sqlite3

DB_NAME = "oficina.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def buscar_manutencoes():
    nome_cliente = entry_cliente.get()
    nome_veiculo = entry_veiculo.get()
    data = entry_data.get()
    tipo = entry_tipo.get()

    query = """
        SELECT c.nome, v.modelo, m.servicos, m.data
        FROM manutencoes m
        JOIN veiculos v ON m.veiculo_id = v.id
        JOIN clientes c ON v.cliente_id = c.id
        WHERE 1=1
    """
    params = []

    if nome_cliente:
        query += " AND c.nome LIKE ?"
        params.append(f"%{nome_cliente}%")
    if nome_veiculo:
        query += " AND v.modelo LIKE ?"
        params.append(f"%{nome_veiculo}%")
    if data:
        query += " AND m.data = ?"
        params.append(data)
    if tipo:
        query += " AND m.servicos LIKE ?"
        params.append(f"%{tipo}%")

    con = conectar()
    cur = con.cursor()
    cur.execute(query, params)
    resultados = cur.fetchall()
    con.close()

    # Limpar tabela
    for item in tree.get_children():
        tree.delete(item)

    # Inserir resultados
    for row in resultados:
        tree.insert("", tk.END, values=row)

# ==== Interface Tkinter ====
root = tk.Tk()
root.title("Histórico de Manutenções")
root.geometry("950x550")
root.configure(bg="#f5f5f5")

tk.Label(root, text="Histórico", font=("Arial Black", 18), bg="#f5f5f5").pack(pady=10)

frame_filtros = tk.Frame(root, bg="#f5f5f5")
frame_filtros.pack(pady=5)

tk.Label(frame_filtros, text="Nome do Cliente:", bg="#f5f5f5").grid(row=0, column=0, padx=5)
entry_cliente = tk.Entry(frame_filtros)
entry_cliente.grid(row=1, column=0, padx=5)

tk.Label(frame_filtros, text="Nome do Veículo:", bg="#f5f5f5").grid(row=0, column=1, padx=5)
entry_veiculo = tk.Entry(frame_filtros)
entry_veiculo.grid(row=1, column=1, padx=5)

tk.Label(frame_filtros, text="Data (dd/mm/yyyy):", bg="#f5f5f5").grid(row=0, column=2, padx=5)
entry_data = tk.Entry(frame_filtros)
entry_data.grid(row=1, column=2, padx=5)

tk.Label(frame_filtros, text="Tipo de Manutenção:", bg="#f5f5f5").grid(row=0, column=3, padx=5)
entry_tipo = tk.Entry(frame_filtros)
entry_tipo.grid(row=1, column=3, padx=5)

btn_buscar = tk.Button(frame_filtros, text="Buscar", bg="black", fg="white", command=buscar_manutencoes)
btn_buscar.grid(row=1, column=4, padx=10)

# ==== Tabela ====
frame_tabela = tk.Frame(root)
frame_tabela.pack(pady=10, fill="both", expand=True)

colunas = ("Cliente", "Carro", "Manutenções", "Data do Serviço")
tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, width=200)

tree.pack(fill="both", expand=True)

root.mainloop()
