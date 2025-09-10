import tkinter as tk
from tkinter import messagebox

# Funções para cada botão
def abrir_cadastro_cliente():
    messagebox.showinfo("Ação", "Abrir tela de cadastro de cliente")

def abrir_cadastro_veiculo():
    messagebox.showinfo("Ação", "Abrir tela de cadastro de veículo")

def abrir_registro_manutencao():
    messagebox.showinfo("Ação", "Abrir tela de manutenção")

def abrir_historico():
    messagebox.showinfo("Ação", "Abrir histórico de manutenções")

def abrir_notificacoes():
    messagebox.showinfo("Ação", "Abrir notificações preventivas")

# Criando a janela principal
root = tk.Tk()
root.title("Drive Tech - Sistema de Manutenção")
root.geometry("900x600")
root.configure(bg="#F5F5F5")

# Barra superior
top_bar = tk.Frame(root, bg="#DDDDDD", height=60)
top_bar.pack(side="top", fill="x")

logo = tk.Label(top_bar, text="DRIVE TECH", font=("Arial Black", 20), bg="#DDDDDD")
logo.pack(side="left", padx=20, pady=10)

usuario = tk.Label(top_bar, text="Olá, Fulano 👤", font=("Arial", 12), bg="#DDDDDD")
usuario.pack(side="right", padx=20)

# Menu lateral
menu = tk.Frame(root, bg="#2C2C2C", width=200)
menu.pack(side="left", fill="y")

def add_menu_button(text, command):
    btn = tk.Button(menu, text=text, command=command, fg="white", bg="#2C2C2C", anchor="w", padx=10)
    btn.pack(fill="x", pady=2)

# Adicionando botões ao menu
add_menu_button("Cadastrar Cliente", abrir_cadastro_cliente)
add_menu_button("Cadastrar Veículo", abrir_cadastro_veiculo)
add_menu_button("Registrar Manutenção", abrir_registro_manutencao)
add_menu_button("Consultar Histórico", abrir_historico)
add_menu_button("Notificações Preventivas", abrir_notificacoes)
add_menu_button("Gerenciar Estoque", lambda: None)
add_menu_button("Relatórios", lambda: None)
add_menu_button("Usuários e Permissões", lambda: None)
add_menu_button("Backup", lambda: None)

# Área de ações principais
main_panel = tk.Frame(root, bg="white")
main_panel.pack(side="right", expand=True, fill="both", padx=10, pady=10)

# Botões principais no painel
def add_main_button(text, command, row, col):
    btn = tk.Button(main_panel, text=text, font=("Arial", 12), width=20, height=3, command=command)
    btn.grid(row=row, column=col, padx=20, pady=20)

add_main_button("Novo Cliente", abrir_cadastro_cliente, 0, 0)
add_main_button("Novo Veículo", abrir_cadastro_veiculo, 0, 1)
add_main_button("Registrar Manutenção", abrir_registro_manutencao, 1, 0)
add_main_button("Histórico", abrir_historico, 1, 1)
add_main_button("Notificações", abrir_notificacoes, 2, 0)

root.mainloop()
