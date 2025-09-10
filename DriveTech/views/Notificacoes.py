import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

DB_NAME = "oficina.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def buscar_notificacoes():
    cliente = cb_cliente.get()
    veiculo = cb_veiculo.get()
    tipo = cb_tipo.get()
    data_limite = cb_data.get()

    query = """
        SELECT c.nome, v.modelo, v.placa, m.servicos, m.data
        FROM manutencoes m
        JOIN veiculos v ON m.veiculo_id = v.id
        JOIN clientes c ON v.cliente_id = c.id
        WHERE 1=1
    """
    params = []  

    if cliente:
        query += " AND c.nome LIKE ?"
        params.append(f"%{cliente}%")
    if veiculo:
        query += " AND v.modelo LIKE ?"
        params.append(f"%{veiculo}%")
    if tipo:
        query += " AND m.servicos LIKE ?"
        params.append(f"%{tipo}%")
    if data_limite:
        try:
            data_limite_dt = datetime.strptime(data_limite, "%d/%m/%Y")
            query += " AND date(m.data) <= ?"
            params.append(data_limite_dt.date())
        except ValueError:
            return

    con = conectar()
    cur = con.cursor()
    cur.execute(query, params)
    notificacoes = cur.fetchall()
    con.close()

    for widget in frame_notificacoes.winfo_children():
        widget.destroy()

    for nome, modelo, placa, servico, data in notificacoes:
        bloco = tk.Frame(frame_notificacoes, bd=1, relief="solid", bg="white", padx=10, pady=10)
        bloco.pack(pady=5, fill="x")

        lbl_servico = tk.Label(bloco, text=servico, font=("Arial", 14, "bold"), fg="red", bg="white")
        lbl_servico.pack(anchor="w")

        info = f"Modelo: {modelo}   |   Placa: {placa}   |   Cliente: {nome}\nData da última manutenção: {data}"
        tk.Label(bloco, text=info, bg="white", anchor="w", justify="left").pack(anchor="w")

# ==== Interface Tkinter ====
root = tk.Tk()
root.title("Notificações Preventivas")
root.geometry("900x600")
root.configure(bg="white")

tk.Label(root, text="Notificações Preventivas", font=("Arial Black", 18), bg="white").pack(pady=10)

frame_filtros = tk.Frame(root, bg="white")
frame_filtros.pack(pady=5)

tk.Label(frame_filtros, text="Cliente:", bg="white").grid(row=0, column=0, padx=5)
cb_cliente = ttk.Combobox(frame_filtros, width=15)
cb_cliente.grid(row=1, column=0, padx=5)

tk.Label(frame_filtros, text="Veículo:", bg="white").grid(row=0, column=1, padx=5)
cb_veiculo = ttk.Combobox(frame_filtros, width=15)
cb_veiculo.grid(row=1, column=1, padx=5)

tk.Label(frame_filtros, text="Tipo de Manutenção:", bg="white").grid(row=0, column=2, padx=5)
cb_tipo = ttk.Combobox(frame_filtros, width=20)
cb_tipo.grid(row=1, column=2, padx=5)

tk.Label(frame_filtros, text="Data Limite (dd/mm/yyyy):", bg="white").grid(row=0, column=3, padx=5)
cb_data = tk.Entry(frame_filtros, width=15)
cb_data.grid(row=1, column=3, padx=5)

btn_buscar = tk.Button(frame_filtros, text="Buscar", bg="black", fg="white", command=buscar_notificacoes)
btn_buscar.grid(row=1, column=4, padx=10)

frame_notificacoes = tk.Frame(root, bg="white")
frame_notificacoes.pack(fill="both", expand=True, padx=20, pady=10)

root.mainloop()
