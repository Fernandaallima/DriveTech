import tkinter as tk
from tkinter import messagebox
import re

# Dados simulados da oficina
USUARIO_EMAIL = "oficina@drivetech.com"
USUARIO_SENHA = "admin123"

# Função para validar email
def email_valido(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email)

# Função de login
def fazer_login():
    email = email_entry.get()
    senha = senha_entry.get()

    if not email_valido(email):
        msg_erro.config(text="Digite um e-mail válido", fg="red")
        return

    if email == USUARIO_EMAIL and senha == USUARIO_SENHA:
        messagebox.showinfo("Login", "Login realizado com sucesso!")
        root.destroy()
    else:
        messagebox.showerror("Erro", "Email ou senha incorretos")

# Mostrar/esconder senha
def toggle_senha():
    if senha_entry.cget('show') == '':
        senha_entry.config(show='*')
        show_btn.config(text='Show')
    else:
        senha_entry.config(show='')
        show_btn.config(text='Hide')

# Janela principal
root = tk.Tk()
root.title("Login - Drive Tech")
root.geometry("800x500")
root.configure(bg="#e6e6e6")  # cinza mais claro

# Container principal
container = tk.Frame(root, bg="#e6e6e6")
container.pack(expand=True)

# Mensagem de boas-vindas
welcome = tk.Label(container, text="Seja Bem-Vindo(a)!", font=("Helvetica", 20, "bold"), bg="#e6e6e6", fg="#333")
welcome.pack(pady=10)

# Logo
try:
    root.logo_img = tk.PhotoImage(file="DriveTech/views/logo.png")
    root.logo_img = root.logo_img.subsample(4, 4)  
    logo_label = tk.Label(container, image=root.logo_img, bg="#e6e6e6")
    logo_label.pack(pady=10)
except:
    logo_label = tk.Label(container, text="DRIVE TECH", font=("Arial Black", 24), bg="#e6e6e6", fg="#222")
    logo_label.pack(pady=10)

# Frame do login (caixa central)
frame = tk.Frame(container, bg="#2c2c2c", padx=20, pady=20, bd=0, relief="flat")
frame.pack(pady=20)

# Campo de email
tk.Label(frame, text="Email", fg="white", bg="#2c2c2c", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w")
email_entry = tk.Entry(frame, width=30, font=("Helvetica", 10))
email_entry.grid(row=1, column=0, columnspan=1, pady=(0,10))
email_entry.insert(0, "your@email.com")

# Mensagem de erro
msg_erro = tk.Label(frame, text="", bg="#2c2c2c", fg="red", font=("Helvetica", 9))
msg_erro.grid(row=2, column=0, columnspan=2, sticky="w")

# Campo de senha
tk.Label(frame, text="Password", fg="white", bg="#2c2c2c", font=("Helvetica", 10)).grid(row=3, column=0, sticky="w")
senha_entry = tk.Entry(frame, width=30, show='*', font=("Helvetica", 10))
senha_entry.grid(row=4, column=0, pady=(0,10))

# Botão mostrar senha
show_btn = tk.Button(frame, text="Show", command=toggle_senha, width=6, font=("Helvetica", 9))
show_btn.grid(row=4, column=1, padx=5)

# Linha de botões
btn_frame = tk.Frame(frame, bg="#2c2c2c")
btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

btn_cancelar = tk.Button(btn_frame, text="Cancel", command=root.destroy, bg="white", width=12, font=("Helvetica", 10))
btn_cancelar.pack(side="left", padx=5)

btn_login = tk.Button(btn_frame, text="Login", command=fazer_login, bg="black", fg="white", width=12, font=("Helvetica", 10))
btn_login.pack(side="left", padx=5)

root.mainloop()
