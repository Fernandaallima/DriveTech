import tkinter as tk
from tkinter import messagebox
import re

# Dados simulados da oficina (credencial fixa para o exemplo)
USUARIO_EMAIL = "oficina@drivetech.com"
USUARIO_SENHA = "admin123"

# Função para validar o email com regex
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
        # Aqui você pode abrir a próxima tela (dashboard do sistema)
    else:
        messagebox.showerror("Erro", "Email ou senha incorretos")

# Mostrar ou esconder senha
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
root.configure(bg="#d3d3d3")

# Mensagem de boas-vindas
welcome = tk.Label(root, text="Seja Bem-Vindo(a)!", font=("Arial", 12, "bold"), bg="#d3d3d3")
welcome.place(x=20, y=20)

# Logo 
try:
    logo_img = tk.PhotoImage(file="logo.png")  
    logo_label = tk.Label(root, image=logo_img, bg="#d3d3d3")
    logo_label.pack(pady=20)
except:
    # fallback se não tiver a imagem
    logo_label = tk.Label(root, text="DRIVE TECH", font=("Arial Black", 24), bg="#d3d3d3")
    logo_label.pack(pady=20)

# Frame do login
frame = tk.Frame(root, bg="#2c2c2c", padx=20, pady=20)
frame.pack()

# Campo de email
tk.Label(frame, text="Email", fg="white", bg="#2c2c2c").grid(row=0, column=0, sticky="w")
email_entry = tk.Entry(frame, width=30)
email_entry.grid(row=1, column=0, columnspan=2)
email_entry.insert(0, "your@email.com")

# Mensagem de erro
msg_erro = tk.Label(frame, text="", bg="#2c2c2c")
msg_erro.grid(row=2, column=0, columnspan=2, sticky="w")

# Campo de senha
tk.Label(frame, text="Password", fg="white", bg="#2c2c2c").grid(row=3, column=0, sticky="w")
senha_entry = tk.Entry(frame, width=30, show='*')
senha_entry.grid(row=4, column=0)

# Botão de mostrar senha
show_btn = tk.Button(frame, text="Show", command=toggle_senha, width=6)
show_btn.grid(row=4, column=1, padx=5)

# Botões
btn_cancelar = tk.Button(frame, text="Cancel", command=root.destroy, bg="white")
btn_cancelar.grid(row=5, column=0, pady=10, sticky="w")

btn_login = tk.Button(frame, text="Login", command=fazer_login, bg="black", fg="white")
btn_login.grid(row=5, column=1, pady=10, sticky="e")

root.mainloop()
