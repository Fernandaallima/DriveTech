import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "oficina.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabela_usuarios():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            perfil TEXT
        )
    """)
    con.commit()
    con.close()

def carregar_usuarios():
    for item in tree.get_children():
        tree.delete(item)

    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nome, email, perfil FROM usuarios")
    for row in cur.fetchall():
        tree.insert("", "end", iid=row[0], values=(row[1], row[2], row[3]))
    con.close()

def adicionar_usuario():
    nome = entry_nome.get()
    email = entry_email.get()
    perfil = cb_perfil.get()

    if not nome or not email or not perfil:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
        return

    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO usuarios (nome, email, perfil) VALUES (?, ?, ?)", (nome, email, perfil))
    con.commit()
    con.close()

    carregar_usuarios()
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    cb_perfil.set("")

def deletar_usuario():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Selecione", "Selecione um usuário.")
        return
    user_id = selecionado[0]
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM usuarios WHERE id=?", (user_id,))
    con.commit()
    con.close()
    carregar_usuarios()

def editar_usuario():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Selecione", "Selecione um usuário.")
        return
    user_id = selecionado[0]
    nome = entry_nome.get()
    email = entry_email.get()
    perfil = cb_perfil.get()

    if not nome or not email or not perfil:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
        return

    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE usuarios SET nome=?, email=?, perfil=? WHERE id=?", (nome, email, perfil, user_id))
    con.commit()
    con.close()
    carregar_usuarios()

def preencher_campos(event):
    selecionado = tree.selection()
    if not selecionado:
        return
    item = tree.item(selecionado)
    valores = item["values"]
    entry_nome.delete(0, tk.END)
    entry_nome.insert(0, valores[0])
    entry_email.delete(0, tk.END)
    entry_email.insert(0, valores[1])
    cb_perfil.set(valores[2])

# === GUI ===
root = tk.Tk()
root.title("Usuários e Permissões")
root.geometry("700x450")

tk.Label(root, text="Usuários e Permissões", font=("Arial Black", 18)).pack(pady=10)

frame_form = tk.Frame(root)
frame_form.pack(pady=5)

tk.Label(frame_form, text="Nome:").grid(row=0, column=0, padx=5)
entry_nome = tk.Entry(frame_form)
entry_nome.grid(row=0, column=1, padx=5)

tk.Label(frame_form, text="Email:").grid(row=0, column=2, padx=5)
entry_email = tk.Entry(frame_form)
entry_email.grid(row=0, column=3, padx=5)

tk.Label(frame_form, text="Perfil:").grid(row=0, column=4, padx=5)
cb_perfil = ttk.Combobox(frame_form, values=["Usuário", "Administrador"])
cb_perfil.grid(row=0, column=5, padx=5)

frame_btns = tk.Frame(root)
frame_btns.pack(pady=10)

tk.Button(frame_btns, text="Adicionar", bg="black", fg="white", command=adicionar_usuario).grid(row=0, column=0, padx=10)
tk.Button(frame_btns, text="Editar", bg="black", fg="white", command=editar_usuario).grid(row=0, column=1, padx=10)
tk.Button(frame_btns, text="Excluir", bg="black", fg="white", command=deletar_usuario).grid(row=0, column=2, padx=10)

tree = ttk.Treeview(root, columns=("Nome", "Email", "Perfil"), show="headings")
tree.heading("Nome", text="Nome")
tree.heading("Email", text="Email")
tree.heading("Perfil", text="Perfil de Acesso")
tree.bind("<<TreeviewSelect>>", preencher_campos)
tree.pack(fill="both", expand=True, padx=20, pady=10)

criar_tabela_usuarios()
carregar_usuarios()
root.mainloop()
