import json
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import base64 as b64

LARGURA = 500
ALTURA = 400


class Tela_publicacao(tk.Toplevel):
    def __init__(self, parent, handle):
        super().__init__(parent)

        self.handle = handle

        self.imagem = None
        self.arquivo_selecionado = None
        self.title("Nova Publicação")
        #self.iconbitmap("View/imagens/icone_icook.ico")

        # dimensões
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        # posicionamento da janela
        pos_x = (largura_tela // 2) - (LARGURA // 2)
        pos_y = (altura_tela // 2) - (ALTURA // 2)
        self.geometry(f"{LARGURA}x{ALTURA}+{pos_x}+{pos_y}")

        # labels
        label_publicacao = tk.Label(self, text="Nova Publicação", font=("Arial", 20, "bold"))
        label_publicacao.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        label_titulo = tk.Label(self, text="Titulo:")
        label_titulo.place(relx=0.125, rely=0.2, anchor=tk.E)

        label_imagem = tk.Label(self, text="Imagem:")
        label_imagem.place(relx=0.3, rely=0.30, anchor=tk.E)

        label_passos = tk.Label(self, text="Passos:")
        label_passos.place(relx=0.8, rely=0.30, anchor=tk.E)

        label_tags = tk.Label(self, text="Tags:")
        label_tags.place(relx=0.125, rely=0.80, anchor=tk.E)

        # entradas
        self.campo_titulo = tk.Entry(self, width=50)
        self.campo_titulo.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.campo_passos = tk.Text(self, height=8, width=20)
        self.campo_passos.place(relx=0.75, rely=0.5, anchor=tk.CENTER)

        self.campo_tags = tk.Entry(self, width=50)
        self.campo_tags.place(relx=0.5, rely=0.80, anchor=tk.CENTER)

        # Botão
        self.bt_publicar = tk.Button(self, text='Publicar', command=self.publica_receita)
        self.bt_publicar.place(relx=0.4, rely=0.9, anchor=tk.CENTER)

        self.bt_voltar = tk.Button(self, text="Voltar", command=self.voltar)
        self.bt_voltar.place(relx=0.6, rely=0.9, anchor=tk.CENTER)

        self.bt_selecionar = tk.Button(self, text="Selecionar Imagem", command=self.selecionar_imagem)
        self.bt_selecionar.place(relx=0.275, rely=0.70, anchor=tk.CENTER)

    #publica receita
    def publica_receita(self):
        # tira dos campos e armazena em variaveis
        titulo = self.campo_titulo.get()
        imagem = self.imagem
        passos = self.campo_passos.get("1.0", tk.END)
        tags = self.campo_tags.get()

        #aqui publica a receita e teoricamente associa ao usuario

        self.handle.publicar(titulo, imagem.hex(), passos, tags)

        messagebox.showinfo('Aviso', "Receita Publicada")

        self.destroy()

    #fecha a janela
    def voltar(self):
        self.destroy()

    #seleciona uma imagem do computador e armazena na variavel "arquivo_selecionado"
    #só pra mostrar um preview na tela
    def selecionar_imagem(self):
        # Abre uma janela de diálogo para selecionar um arquivo de imagem
        arquivo = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg")])

        if arquivo:
            self.imagem = open(arquivo, "rb").read()

            # Carrega a imagem selecionada
            imagem = Image.open(arquivo)

            # Redimensiona a imagem para ajustar na janela
            imagem = imagem.resize((125, 125))

            # Atualiza a imagem exibida na janela
            imagem_tk = ImageTk.PhotoImage(imagem)
            # print(imagem)
            label_imagem_inserida = tk.Label(self)
            label_imagem_inserida.place(relx=0.4, rely=0.5, anchor=tk.E)
            label_imagem_inserida.configure(image=imagem_tk)
            label_imagem_inserida.image = imagem_tk
