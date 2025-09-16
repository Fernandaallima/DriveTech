import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import shutil
import os
from datetime import datetime

DB_NAME = "oficina.db"
BACKUP_DIR = "backups"
HISTORICO_FILE = "historico_backups.txt"

# Cria diretório se não existir
os.makedirs(BACKUP_DIR, exist_ok=True)

# === Funções ===
def registrar_backup(status, tamanho):
    with open(HISTORICO_FILE, "a") as f:
        data = datetime.now().strftime("%d/%m/%Y - %H:%M")
        f.write(f"{data}|{tamanho} MB|{status}\n")

def carregar_historico():
    if not os.path.exists(HISTORICO_FILE):
        return
    tree.delete(*tree.get_children())
    with open(HISTORICO_FILE, "r") as f:
        for linha in f:
            partes = linha.strip().split("|")
            if len(partes) == 3:
                tree.insert("", "end", values=partes)

def criar_backup():
    try:
        data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_backup = f"backup_{data_hora}.db"
        caminho_destino = os.path.join(BACKUP_DIR, nome_backup)

        shutil.copy(DB_NAME, caminho_destino)
        tamanho = round(os.path.getsize(caminho_destino) / (1024 * 1024), 2)

        registrar_backup("Concluído", tamanho)
        messagebox.showinfo("Backup", "Backup criado com sucesso!")
        carregar_historico()
    except Exception as e:
        registrar_backup("Falhou", 0)
        messagebox.showerror("Erro", f"Erro ao criar backup:\n{e}")

def restaurar_backup():
    arquivo = filedialog.askopenfilename(title="Selecionar backup", filetypes=[("Banco de Dados", "*.db")])
    if not arquivo:
        return
    try:
        shutil.copy(arquivo, DB_NAME)
        messagebox.showinfo("Restaurar", "Backup restaurado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao restaurar backup:\n{e}")

# === GUI ===
root = tk.Tk()
root.title("Gerenciamento de Backups")
root.geometry("700x450")

tk.Label(root, text="Gerenciamento de Backups", font=("Arial Black", 18)).pack(pady=10)

frame_btns = tk.Frame(root)
frame_btns.pack(pady=20)

btn_backup = tk.Button(frame_btns, text="Criar Backup", font=("Arial", 12), width=15, command=criar_backup)
btn_backup.grid(row=0, column=0, padx=20)

btn_restaurar = tk.Button(frame_btns, text="Restaurar Backup", font=("Arial", 12), width=15, command=restaurar_backup)
btn_restaurar.grid(row=0, column=1, padx=20)

tk.Label(root, text="Histórico de Backups", font=("Arial", 14, "bold")).pack(pady=10)

tree = ttk.Treeview(root, columns=("Data", "Tamanho", "Status"), show="headings")
tree.heading("Data", text="Data/Hora")
tree.hea
