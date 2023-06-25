import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

LARGURA = 400
ALTURA = 300


class Tela_cadastro(tk.Toplevel):
    def __init__(self, parent, handle):
        super().__init__(parent)

        self.handle = handle

        self.title("Cadastro")
        #self.iconbitmap("View/imagens/icone_icook.ico")

        # dimensões
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        # posicionamento da tela
        pos_x = (largura_tela // 2) - (LARGURA // 2)
        pos_y = (altura_tela // 2) - (ALTURA // 2)
        self.geometry(f"{LARGURA}x{ALTURA}+{pos_x}+{pos_y}")

        # labels
        label_cadastro = tk.Label(self, text="Cadastro", font=("Arial", 20, "bold"))
        label_cadastro.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        label_nome = tk.Label(self, text="Nome:")
        label_nome.place(relx=0.27, rely=0.25, anchor=tk.E)

        label_usuario = tk.Label(self, text="Usuário:")
        label_usuario.place(relx=0.27, rely=0.35, anchor=tk.E)

        label_email = tk.Label(self, text="E-mail:")
        label_email.place(relx=0.27, rely=0.45, anchor=tk.E)

        label_senha = tk.Label(self, text="Senha:")
        label_senha.place(relx=0.27, rely=0.55, anchor=tk.E)

        label_conf_senha = tk.Label(self, text="Confirme a senha:")
        label_conf_senha.place(relx=0.27, rely=0.65, anchor=tk.E)

        # entradas
        self.campo_nome = ttk.Entry(self)
        self.campo_nome.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

        self.campo_usuario = ttk.Entry(self)
        self.campo_usuario.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        self.campo_email = ttk.Entry(self)
        self.campo_email.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        self.campo_senha = ttk.Entry(self)
        self.campo_senha.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.campo_senha_conf = ttk.Entry(self)
        self.campo_senha_conf.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        # Botão
        self.bt_reg_cadastro = ttk.Button(self, text='Cadastrar', command=self.realiza_cadastro)
        self.bt_reg_cadastro.place(relx=0.5, rely=0.7625, anchor=tk.CENTER)

        self.bt_voltar = tk.Button(self, text="Voltar", command=self.voltar)
        self.bt_voltar.place(relx=0.5, rely=0.875, anchor=tk.CENTER)

    #realiza cadastro
    def realiza_cadastro(self):
        # tira dos campos e armazena em variaveis
        nome = self.campo_nome.get()
        usuario = self.campo_usuario.get()
        email = self.campo_email.get()
        senha = self.campo_senha.get()
        senha_conf = self.campo_senha_conf.get()

        try:
            self.handle.cadastro(nome, usuario, email, senha, senha_conf)
            messagebox.showinfo('Aviso', "Cadastro Realizado!")
            self.destroy()
        except Exception as e:
            messagebox.showinfo('Aviso', str(e))

    #fecha a janela
    def voltar(self):
        self.destroy()
