import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "oficina.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabela_estoque():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor REAL NOT NULL
        )
    """)
    con.commit()
    con.close()

def atualizar_tabela():
    for item in tree.get_children():
        tree.delete(item)

    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nome, quantidade, valor FROM estoque")
    for row in cur.fetchall():
        tree.insert("", "end", values=(row[0], row[1], row[2], f"R${row[3]:.2f}"))
    con.close()

def adicionar_item():
    def salvar():
        try:
            nome = entrada_nome.get()
            quantidade = int(entrada_qtd.get())
            valor = float(entrada_valor.get().replace(",", "."))
            if nome == "":
                raise ValueError("Nome não pode ser vazio.")

            con = conectar()
            cur = con.cursor()
            cur.execute("INSERT INTO estoque (nome, quantidade, valor) VALUES (?, ?, ?)", (nome, quantidade, valor))
            con.commit()
            con.close()
            atualizar_tabela()
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    popup = tk.Toplevel(root)
    popup.title("Adicionar Peça")
    popup.geometry("300x200")

    tk.Label(popup, text="Nome da Peça:").pack()
    entrada_nome = tk.Entry(popup)
    entrada_nome.pack()

    tk.Label(popup, text="Quantidade:").pack()
    entrada_qtd = tk.Entry(popup)
    entrada_qtd.pack()

    tk.Label(popup, text="Valor:").pack()
    entrada_valor = tk.Entry(popup)
    entrada_valor.pack()

    tk.Button(popup, text="Salvar", command=salvar).pack(pady=10)

def editar_item():
    item = tree.selection()
    if not item:
        messagebox.showwarning("Aviso", "Selecione um item para editar.")
        return
    valores = tree.item(item, "values")
    id_item, nome_antigo, qtd_antiga, valor_antigo = valores

    def salvar_edicao():
        try:
            novo_nome = entrada_nome.get()
            nova_qtd = int(entrada_qtd.get())
            novo_valor = float(entrada_valor.get().replace(",", "."))

            con = conectar()
            cur = con.cursor()
            cur.execute("UPDATE estoque SET nome=?, quantidade=?, valor=? WHERE id=?", (novo_nome, nova_qtd, novo_valor, id_item))
            con.commit()
            con.close()
            atualizar_tabela()
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    popup = tk.Toplevel(root)
    popup.title("Editar Peça")
    popup.geometry("300x200")

    tk.Label(popup, text="Nome da Peça:").pack()
    entrada_nome = tk.Entry(popup)
    entrada_nome.insert(0, nome_antigo)
    entrada_nome.pack()

    tk.Label(popup, text="Quantidade:").pack()
    entrada_qtd = tk.Entry(popup)
    entrada_qtd.insert(0, qtd_antiga)
    entrada_qtd.pack()

    tk.Label(popup, text="Valor:").pack()
    entrada_valor = tk.Entry(popup)
    entrada_valor.insert(0, valor_antigo.replace("R$", ""))
    entrada_valor.pack()

    tk.Button(popup, text="Salvar Alterações", command=salvar_edicao).pack(pady=10)

def excluir_item():
    item = tree.selection()
    if not item:
        messagebox.showwarning("Aviso", "Selecione um item para excluir.")
        return
    valores = tree.item(item, "values")
    id_item = valores[0]

    confirmacao = messagebox.askyesno("Confirmar", "Deseja realmente excluir essa peça?")
    if confirmacao:
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM estoque WHERE id=?", (id_item,))
        con.commit()
        con.close()
        atualizar_tabela()

# ==== Interface ====
root = tk.Tk()
root.title("Gerenciamento de Estoque")
root.geometry("600x400")

tk.Label(root, text="Gerenciamento de Estoque", font=("Arial Black", 16)).pack(pady=10)

colunas = ("ID", "Peça", "Quantidade", "Valor")
tree = ttk.Treeview(root, columns=colunas, show="headings")
for col in colunas:
    tree.heading(col, text=col)
tree.pack(expand=True, fill="both", padx=20)

# Botões
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text="Adicionar", bg="black", fg="white", width=12, command=adicionar_item).grid(row=0, column=0, padx=10)
tk.Button(frame_botoes, text="Editar", bg="black", fg="white", width=12, command=editar_item).grid(row=0, column=1, padx=10)
tk.Button(frame_botoes, text="Excluir", bg="black", fg="white", width=12, command=excluir_item).grid(row=0, column=2, padx=10)

criar_tabela_estoque()
atualizar_tabela()
root.mainloop()
