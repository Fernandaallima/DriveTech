import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

DB_NAME = "oficina.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabela_manutencao():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS manutencao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            carro TEXT,
            placa TEXT,
            data TEXT,
            servico TEXT
        )
    """)
    con.commit()
    con.close()

# Para teste: dados fictícios
def popular_dados_ficticios():
    con = conectar()
    cur = con.cursor()
    cur.executemany("""
        INSERT INTO manutencao (cliente, carro, placa, data, servico)
        VALUES (?, ?, ?, ?, ?)
    """, [
        ("Jorge Almeida", "Prisma", "FGT456", "2025-05-12", "Troca de Óleo"),
        ("Marcia Souza", "Uno", "UTS985", "2025-05-09", "Cambagem"),
        ("Luis Matos", "C3", "JSE684", "2025-05-04", "Alinhamento")
    ])
    con.commit()
    con.close()

def gerar_relatorio():
    tipo_servico = cb_servico.get()
    data = entrada_data.get()

    query = "SELECT * FROM manutencao WHERE 1=1"
    params = []

    if tipo_servico:
        query += " AND servico LIKE ?"
        params.append(f"%{tipo_servico}%")
    if data:
        query += " AND data = ?"
        params.append(data)

    con = conectar()
    cur = con.cursor()
    cur.execute(query, params)
    resultados = cur.fetchall()
    con.close()

    for item in tree.get_children():
        tree.delete(item)

    for row in resultados:
        texto = f"Relatório - {row[2]}/{row[3]} - {row[4]}_{row[1].replace(' ', '_')}"
        tree.insert("", "end", values=(texto,))

    if not resultados:
        messagebox.showinfo("Relatório", "Nenhum resultado encontrado.")

def exportar_relatorio():
    itens = tree.get_children()
    if not itens:
        messagebox.showwarning("Exportar", "Nenhum relatório para exportar.")
        return

    with open("relatorios_gerados.txt", "w", encoding="utf-8") as f:
        for item in itens:
            texto = tree.item(item, "values")[0]
            f.write(texto + "\n")

    messagebox.showinfo("Exportado", "Relatório exportado para relatorios_gerados.txt")

# ==== Interface ====
root = tk.Tk()
root.title("Relatórios")
root.geometry("700x400")

tk.Label(root, text="Relatórios", font=("Arial Black", 18)).pack(pady=10)

frame_filtros = tk.Frame(root)
frame_filtros.pack(pady=5)

tk.Label(frame_filtros, text="Serviços realizados:").grid(row=0, column=0, padx=5)
cb_servico = ttk.Combobox(frame_filtros, values=["", "Troca de Óleo", "Cambagem", "Alinhamento", "Suspensão"])
cb_servico.grid(row=0, column=1, padx=5)

tk.Label(frame_filtros, text="Data (AAAA-MM-DD):").grid(row=0, column=2, padx=5)
entrada_data = tk.Entry(frame_filtros)
entrada_data.grid(row=0, column=3, padx=5)

tk.Button(frame_filtros, text="Gerar relatório", bg="black", fg="white", command=gerar_relatorio).grid(row=0, column=4, padx=10)

tree = ttk.Treeview(root, columns=("Relatório",), show="headings")
tree.heading("Relatório", text="Relatórios Gerados")
tree.pack(expand=True, fill="both", padx=20, pady=10)

tk.Button(root, text="Exportar Relatório", bg="black", fg="white", command=exportar_relatorio).pack(pady=5)

criar_tabela_manutencao()
popular_dados_ficticios()
root.mainloop()
