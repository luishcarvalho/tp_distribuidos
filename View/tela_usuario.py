import io
import tkinter as tk
from PIL import ImageTk, Image
from View.tela_receita import Tela_receita

LARGURA = 500
ALTURA = 400


# aqui passa o usuario
# mesmo esquema la embaixo: user.nome/user.user sla


class Tela_usuario(tk.Toplevel):
    def __init__(self, parent, user_name, handle):
        super().__init__(parent)

        self.title("Usuario")
        #self.iconbitmap("View/imagens/icone_icook.ico")

        self.handle = handle

        # dimensões
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        # posicionamento da janela
        pos_x = (largura_tela // 2) - (LARGURA // 2)
        pos_y = (altura_tela // 2) - (ALTURA // 2)
        self.geometry(f"{LARGURA}x{ALTURA}+{pos_x}+{pos_y}")

        # Frame principal
        self.frame_principal = tk.Frame(self)
        self.frame_principal.place(relx=0.5, rely=0.65, anchor=tk.CENTER, width=450, height=200)

        self.scrollbar = tk.Scrollbar(self.frame_principal)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.frame_principal, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        # aqui abre o frame para mostrar as receitas
        self.mostra_receitas(user_name)

        # labels
        nome_usuario = self.handle.get_nome(user_name)  # PROPÓSITO DE TESTE
        label_nome_usuario = tk.Label(self, text=nome_usuario, font=("Arial", 15, "bold"))
        label_nome_usuario.place(relx=0.60, rely=0.075, anchor=tk.CENTER)

        self.user_usuario = user_name  # PROPÓSITO DE TESTE
        label_user_usuario = tk.Label(self, text=self.user_usuario, font=("Arial", 10, "bold"))
        label_user_usuario.place(relx=0.60, rely=0.15, anchor=tk.CENTER)

        # imagens
        arquivo = "View/imagens/chef.jpg"  # imagem generica de uma silhueta de chef
        imagem = Image.open(arquivo)
        imagem = imagem.resize((100, 100))
        imagem_tk = ImageTk.PhotoImage(imagem)
        label_imagem = tk.Label(self)
        label_imagem.place(relx=0.3, rely=0.15, anchor=tk.E)
        label_imagem.configure(image=imagem_tk)
        label_imagem.image = imagem_tk

        # botões
        '''
        ideia minha: verifica se o usuario x segue o y
        armazena na "estado_atual"
        caso siga estado = 1 else estado = 0
        '''
        self.seguir_var = tk.IntVar()  # variavel pra mudar o checkbox
        self.estado_atual = self.handle.check_seg(user_name)
        if self.estado_atual == 1:
            verifica_ckeck = self.seguir_var.get()
            self.seguir_var.set(not verifica_ckeck)  # aqui é pra marcar a caixa caso siga

        self.bt_seguir = tk.Checkbutton(self, text="Seguir", variable=self.seguir_var, command=self.seguir)
        self.bt_seguir.place(relx=0.6, rely=0.225, anchor=tk.CENTER)

        self.bt_voltar = tk.Button(self, text="Voltar", command=self.voltar)
        self.bt_voltar.place(relx=0.85, rely=0.15, anchor=tk.CENTER)

    # fecha a janela
    def voltar(self):
        self.destroy()

    # aqui nesse caso eu coloquei uma checkbox
    # entao teoricamente teria que fazer uma verificação pra ver se segue
    #
    def seguir(self):
        self.handle.seguir(self.user_usuario)
        # aqui ele pega o valor da variavel pra fazer um if
        if self.seguir_var.get() == 1:  # se ja segue, muda a variavel pra 0
            self.estado_atual = 0
        else:  # se não segue muda pra 1
            self.estado_atual = 1

    def mostra_receitas(self, user):
        # teoricamente limpa o canvas antes de mostrar as imagens
        self.canvas.delete("all")

        # Posição inicial das imagens
        x, y = 10, 10

        # Lista de imagens
        # aqui ele itera sobre as imagens pra gerar os botões e os títulos
        # true ou false dependendo do objetivo da função
        termo = user

        imagens, nomes, autores = self.handle.get_posts(termo)

        for x in range(len(imagens)):
            # Carrega a imagem

            imagem_bytes = io.BytesIO(bytes.fromhex(imagens[x]))
            nome_prato = nomes[x]

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

            label_nome_receita = tk.Label(self, text=str(nome_prato), font=("Arial", 10, "bold"))
            label_nome_receita.pack(pady=5)

            # Adiciona a imagem ao canvas
            self.canvas.create_window(x, y, anchor=tk.NW, window=label_imagem)
            self.canvas.create_window(140, y + 40, anchor=tk.NW, window=botao_exibir)
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


