import glob
import io
import json
import os
import tkinter as tk
from PIL import ImageTk, Image
from View.tela_receita import Tela_receita
from View.tela_usuario import Tela_usuario
from View.tela_publicacao import Tela_publicacao
import base64 as b64

LARGURA = 500
ALTURA = 400


class Tela_principal(tk.Toplevel):
    def __init__(self, parent, handle):
        super().__init__(parent)

        self.handle = handle

        self.title("iCook")
        #self.iconbitmap("View/imagens/icone_icook.ico")

        # dimensões
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        # posicionamento da janela
        pos_x = (largura_tela // 2) - (LARGURA // 2)
        pos_y = (altura_tela // 2) - (ALTURA // 2)
        self.geometry(f"{LARGURA}x{ALTURA}+{pos_x}+{pos_y}")

        # Frame principal
        self.frame_principal = tk.Frame(self)
        self.frame_principal.place(relx=0.5, rely=0.55, anchor=tk.CENTER, width=450, height=300)

        self.scrollbar = tk.Scrollbar(self.frame_principal)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.frame_principal, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        self.mostra_receitas(False)

        # labels
        label_feed = tk.Label(self, text="Feed", font=("Arial", 15, "bold"))
        label_feed.place(relx=0.15, rely=0.075, anchor=tk.CENTER)

        nick = self.handle.get_nick()

        self.user_usuario = nick  # PROPÓSITO DE TESTE
        label_user_usuario = tk.Label(self, text=self.user_usuario, font=("Arial", 10, "bold"))
        label_user_usuario.place(relx=0.4, rely=0.075, anchor=tk.CENTER)

        # campos
        self.campo_pesquisa = tk.Entry(self, width=45)
        self.campo_pesquisa.place(relx=0.35, rely=0.178, anchor=tk.CENTER)

        # botões
        self.bt_perfil = tk.Button(
            self,            # PROPÓSITO DE TESTE
            text="Perfil",   # passar o user.nome(?) como arg para a função pra abrir o perfil
            command=lambda usuario=nick: self.abre_perfil(usuario)
        )

        #self.bt_perfil = tk.Button(self, text="Perfil", command=self.abre_perfil)
        self.bt_perfil.place(relx=0.65, rely=0.075, anchor=tk.CENTER)

        self.bt_postar = tk.Button(self, text="Postar", command=self.posta_receita)
        self.bt_postar.place(relx=0.75, rely=0.075, anchor=tk.CENTER)

        self.bt_voltar = tk.Button(self, text="Sair", command=self.voltar)
        self.bt_voltar.place(relx=0.85, rely=0.075, anchor=tk.CENTER)

        # aqui o botão chama a função de mostrar receitas dnv
        # mudei a função pra limpar o canvas antes de mostrar imagens dnv
        self.bt_refresh = tk.Button(self, text="Recarregar", command=lambda: self.recarregar())
        self.bt_refresh.place(relx=0.5, rely=0.925, anchor=tk.CENTER)

        # caso seja pesquisa, ele passa true e atualiza o frame de outra maneira
        self.bt_pesquisar = tk.Button(self, text="Pesquisar Receita", command=lambda: self.mostra_receitas(True))
        self.bt_pesquisar.place(relx=0.78, rely=0.175, anchor=tk.CENTER)

    def recarregar(self):
        self.mostra_receitas(False)

    # fecha a janela
    def voltar(self):
        self.destroy()

    def mostra_receitas(self, pesquisa):
        # teoricamente limpa o canvas antes de mostrar as imagens
        self.canvas.delete("all")

        # Posição inicial das imagens
        x, y = 10, 10

        # Lista de imagens
        # aqui ele itera sobre as imagens pra gerar os botões e os títulos
        # true ou false dependendo do objetivo da função
        if pesquisa:
            termo = self.campo_pesquisa.get()
        else:
            termo = ""

        imagens, nomes, autores = self.handle.get_posts(termo)

        for x in range(len(imagens)):
            # Carrega a imagem

            imagem_bytes = io.BytesIO(bytes.fromhex(imagens[x]))
            nome_prato = nomes[x]
            autor = autores[x]

            imagem = Image.open(imagem_bytes)
            imagem = imagem.resize((100, 100))
            imagem_tk = ImageTk.PhotoImage(imagem)

            # Cria um widget Label para exibir a imagem
            label_imagem = tk.Label(self.canvas, image=imagem_tk)
            label_imagem.image = imagem_tk

            # Criar um botão para a imagem
            '''print(imagem_path)
            botao_imagem = tk.Button(self.canvas, text="Exibir", command=self.abre_receita)
            botao_imagem.pack(pady=5)'''

            # eu fiz essa função "exibir nome" só pra testar e ver como que funfa o self com o lambda
            # PROPÓSITO DE TESTE
            botao_exibir = tk.Button(
                self.canvas,
                text="Exibir",  # armazena o receita.nome(?) na variavel e passa como parametro pra "abre_receita"
                command=lambda dados=(x, imagem_bytes): self.abre_receita(dados)
            )
            botao_exibir.pack(pady=5)

            # aqui no caso imagino que seja só passar o receita.user como parâmetro
            # e usar esse parâmetro pra chamar a função de janela de perfildnv
            botao_perfil = tk.Button(
                self.canvas,
                text="Perfil",  # armazena o receita.autor(?) na variavel e passa como parametro pra "abre_perfil"
                command=lambda autor_receita=autor: self.abre_perfil(autor_receita)
            )
            botao_perfil.pack(pady=5)

            label_nome_receita = tk.Label(self, text=str(nome_prato), font=("Arial", 10, "bold"))
            label_nome_receita.pack(pady=5)

            # Adiciona a imagem ao canvas
            self.canvas.create_window(x, y, anchor=tk.NW, window=label_imagem)
            self.canvas.create_window(140, y + 40, anchor=tk.NW, window=botao_exibir)
            self.canvas.create_window(370, y + 40, anchor=tk.NW, window=botao_perfil)
            self.canvas.create_window(200, y + 40, anchor=tk.NW, window=label_nome_receita)

            # Atualiza as posições para a próxima imagem
            y += 120

        # Atualiza a área de visualização do canvas
        self.canvas.update_idletasks()

        # Configura a barra de rolagem
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def abre_receita(self, dados):
        abre_receita = Tela_receita(self, dados[0], dados[1], self.handle)
        abre_receita.grab_set()

    def posta_receita(self):
        posta_receita = Tela_publicacao(self, self.handle)
        posta_receita.grab_set()

    def abre_perfil(self, autor_receita):
        abre_perfil = Tela_usuario(self, autor_receita, self.handle)
        abre_perfil.grab_set()
