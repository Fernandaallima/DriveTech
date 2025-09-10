import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Banco
DB_NAME = "oficina.db"

def conectar():
    return sqlite3.connect(DB_NAME)

# Obter lista de veículos (placa + modelo)
def obter_veiculos():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, placa, modelo FROM veiculos")
    veiculos = cur.fetchall()
    con.close()
    return veiculos

def registrar_manutencao():
    veiculo_selecionado = combo_veiculo.get()
    data = entry_data.get()
    servicos = txt_servicos.get("1.0", tk.END).strip()
    pecas = combo_pecas.get()
    observacoes = txt_obs.get("1.0", tk.END).strip()

    if not veiculo_selecionado or not data or not servicos:
        messagebox.showwarning("Atenção", "Preencha os campos obrigatórios.")
        return

    try:
        # Obter ID do veículo
        veiculo_id = veiculo_map.get(veiculo_selecionado)

        con = conectar()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO manutencoes (veiculo_id, data, servicos, pecas, observacoes)
            VALUES (?, ?, ?, ?, ?)
        """, (veiculo_id, data, servicos, pecas, observacoes))

        con.commit()
        con.close()

        messagebox.showinfo("Sucesso", "Manutenção registrada com sucesso.")
        limpar_campos()

    except Exception as e:
        messagebox.showerror("Erro", str(e))

def limpar_campos():
    combo_veiculo.set("")
    entry_data.delete(0, tk.END)
    combo_pecas.set("")
    txt_servicos.delete("1.0", tk.END)
    txt_obs.delete("1.0", tk.END)

# Interface
root = tk.Tk()
root.title("Registrar Manutenção - Drive Tech")
root.geometry("850x500")
root.configure(bg="#F5F5F5")

# Título
tk.Label(root, text="Registrar Manutenções", font=("Arial Black", 18), bg="#F5F5F5").pack(pady=10)

form = tk.Frame(root, bg="#F5F5F5")
form.pack(pady=10)

# Selecionar veículo
tk.Label(form, text="Selecionar Veículo:", bg="#F5F5F5").grid(row=0, column=0, sticky="w")
combo_veiculo = ttk.Combobox(form, width=35, state="readonly")
combo_veiculo.grid(row=1, column=0, padx=10)

# Data
tk.Label(form, text="Data:", bg="#F5F5F5").grid(row=0, column=1, sticky="w")
entry_data = tk.Entry(form, width=30)
entry_data.grid(row=1, column=1, padx=10)
entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))

# Serviços
tk.Label(form, text="Serviços realizados:", bg="#F5F5F5").grid(row=2, column=0, sticky="w", pady=(10, 0))
txt_servicos = tk.Text(form, width=40, height=5)
txt_servicos.grid(row=3, column=0, padx=10)

# Peças
tk.Label(form, text="Peças utilizadas:", bg="#F5F5F5").grid(row=2, column=1, sticky="w", pady=(10, 0))
combo_pecas = ttk.Combobox(form, width=35, state="readonly")
combo_pecas.grid(row=3, column=1, padx=10)

# Observações
tk.Label(form, text="Observações:", bg="#F5F5F5").grid(row=4, column=0, sticky="w", pady=(10, 0))
txt_obs = tk.Text(form, width=40, height=4)
txt_obs.grid(row=5, column=0, padx=10)

# Botão
btn_registrar = tk.Button(root, text="Registrar", command=registrar_manutencao, bg="black", fg="white", width=15, height=2)
btn_registrar.pack(pady=20)

# Carregar dados no ComboBox
veiculos = obter_veiculos()
veiculo_map = {f"{v[1]} - {v[2]}": v[0] for v in veiculos}
combo_veiculo['values'] = list(veiculo_map.keys())

# Placeholder para peças (exemplo fixo, pode vir do estoque futuramente)
combo_pecas['values'] = ["Óleo", "Filtro de ar", "Pneu", "Pastilha de freio"]

root.mainloop()
