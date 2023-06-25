import tkinter as tk
from PIL import ImageTk, Image
import emoji

LARGURA = 500
ALTURA = 400

#passar como referência "o objeto receita"(?)
#ai depois faz um receita.foto / receita.titulo sla?


class Tela_receita(tk.Toplevel):
    def __init__(self, parent, index, imagem_path, handle):
        super().__init__(parent)

        self.handle = handle

        self.index = index

        self.title("Receita")
        #self.iconbitmap("View/imagens/icone_icook.ico")

        # dimensões
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        # posicionamento da janela
        pos_x = (largura_tela // 2) - (LARGURA // 2)
        pos_y = (altura_tela // 2) - (ALTURA // 2)
        self.geometry(f"{LARGURA}x{ALTURA}+{pos_x}+{pos_y}")

        # labels
        titulo_receita = self.handle.get_titulo(index)  # PROPÓSITO DE TESTE
        label_titulo = tk.Label(self, text=titulo_receita, font=("Arial", 15, "bold"))
        label_titulo.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # imagens
        imagem = Image.open(imagem_path)
        imagem = imagem.resize((200, 200))
        imagem_tk = ImageTk.PhotoImage(imagem)
        label_imagem = tk.Label(self)
        label_imagem.place(relx=0.45, rely=0.425, anchor=tk.E)
        label_imagem.configure(image=imagem_tk)
        label_imagem.image = imagem_tk

        passos = self.handle.get_passos(index)
        label_passos = tk.Label(self, text=passos)
        label_passos.place(relx=0.8, rely=0.30, anchor=tk.E)

        tags = self.handle.get_tags(index)
        label_tags = tk.Label(self, text=tags)
        label_tags.place(relx=0.5, rely=0.80, anchor=tk.E)

        self.estrelas_reload(self.handle.get_estrelas(index))

        # botões
        emoji_1estrela = emoji.emojize(":star:")
        emoji_2estrela = emoji.emojize(":star: :star:")
        emoji_3estrela = emoji.emojize(":star: :star: :star:")
        self.estrelas = tk.IntVar()
        self.bt_avaliar = tk.Button(self, text="Avaliar", command=self.avaliar)
        self.bt_avaliar.place(relx=0.6, rely=0.9, anchor=tk.CENTER)

        estrela_1 = tk.Radiobutton(self, text=emoji_1estrela, variable=self.estrelas, value=1)
        estrela_1.place(relx=0.1, rely=0.9, anchor=tk.CENTER)
        estrela_2 = tk.Radiobutton(self, text=emoji_2estrela, variable=self.estrelas, value=2)
        estrela_2.place(relx=0.25, rely=0.9, anchor=tk.CENTER)
        estrela_3 = tk.Radiobutton(self, text=emoji_3estrela, variable=self.estrelas, value=3)
        estrela_3.place(relx=0.40, rely=0.9, anchor=tk.CENTER)

        self.bt_voltar = tk.Button(self, text="Voltar", command=self.voltar)
        self.bt_voltar.place(relx=0.8, rely=0.9, anchor=tk.CENTER)

    # fecha a janela
    def voltar(self):
        self.destroy()

    # aqui adiciona uma nota a receita
    def avaliar(self):
        opcao_selecionada = self.estrelas.get()

        self.handle.avaliar(self.index, opcao_selecionada)

        self.estrelas_reload(self.handle.get_estrelas(self.index))

    def estrelas_reload(self, estrelas):
        label_tags = tk.Label(self, text=f'Estrelas: {estrelas:.2f}')
        label_tags.place(relx=0.9, rely=0.80, anchor=tk.E)

