import tkinter as tk
from tkinter import messagebox

import Pyro5.api as api
from View.tela_cadastro import Tela_cadastro
from View.tela_principal import Tela_principal
from Model.exceptions.CredenciaisErradasException import CredenciaisErradasException
LARGURA = 400
ALTURA = 300


class Tela_login(tk.Tk):
    def __init__(self, handle):
        super().__init__()

        self.handle = handle
        self.title("Login")

        #dimensões
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        #posicionamento da janela
        pos_x = (largura_tela // 2) - (LARGURA // 2)
        pos_y = (altura_tela // 2) - (ALTURA // 2)
        self.geometry(f"{LARGURA}x{ALTURA}+{pos_x}+{pos_y}")

        #label
        label_icook = tk.Label(self, text="iCook", font=("Arial", 20, "bold"))
        label_icook.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        label_usuario = tk.Label(self, text="Usuário:")
        label_usuario.place(relx=0.27, rely=0.35, anchor=tk.E)

        label_senha = tk.Label(self, text="Senha:")
        label_senha.place(relx=0.27, rely=0.5, anchor=tk.E)

        #entrada de texto
        self.campo_usuario = tk.Entry(self)
        self.campo_usuario.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        self.campo_senha = tk.Entry(self, show="*")
        self.campo_senha.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        #botões
        bt_logar = tk.Button(self, text="Logar", command=self.logar)
        bt_logar.place(relx=0.5, rely=0.70, anchor=tk.CENTER)

        self.bt_cadastrar = tk.Button(self, text="Cadastrar", command=self.cadastrar)
        self.bt_cadastrar.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    #aqui só abre a tela de cadastro
    def cadastrar(self):
        tela_cadastro = Tela_cadastro(self, self.handle)
        tela_cadastro.grab_set()

    #aqui loga no sistema
    #necessário user e senha
    #user.user ou user.senha sla
    def logar(self):
        usuario = self.campo_usuario.get()
        senha = self.campo_senha.get()

        try:
            self.handle.login(usuario, senha)

            user_hadle = api.Proxy("PYRONAME:handle.userhandler")
            user_hadle.bind_user(usuario)

            tela_principal = Tela_principal(self, user_hadle)
            tela_principal.grab_set()
            self.withdraw()
            self.wait_window(tela_principal)  # Aguarda o fechamento da segunda janela
            self.deiconify()  # Mostra novamente a primeira janela
        except Exception as e:
            self.campo_usuario.delete(0, tk.END)
            self.campo_senha.delete(0, tk.END)
            messagebox.showinfo("Erro", str(e))


"""if __name__ == "__main__":
    tela_login = Tela_login()
    tela_login.mainloop()"""
