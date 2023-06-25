import json
from datetime import datetime
from Pyro5 import api
from Model.Banco import Banco as Bd
from Model.Usuario import Usuario
from Model.Post import Post


@api.expose
class UserHandler:
    def __init__(self):
        self.i_sorted = []
        self.usuario = None
        self.bd = Bd()
        self.pubs = {}

    def bind_user(self, usuario):
        self.usuario = self.bd.buscarUsuarioBancoUser(usuario)

    def get_nick(self):
        return self.usuario.get_user()

    def get_nome(self, user_name):
        return self.bd.buscarUsuarioBancoUser(user_name).get_nome()

    def check_seg(self, user_name):
        return 1 if user_name in self.usuario.get_sou_seguidor() else 0

    def seguir(self, user_name):
        if user_name in self.usuario.get_sou_seguidor():
            self.usuario.remover_seguidor(user_name)
            self.bd.atualizaBanco(self.usuario)
        else:
            self.usuario.inserir_seguidores([user_name])
            self.bd.atualizaBanco(self.usuario)

    def get_posts(self, pesquisa):
        if pesquisa == "":
            usuarios = self.usuario.get_sou_seguidor()
        else:
            usuarios = [pesquisa]

        imagens = []
        nomes = []
        autores = []

        self.pubs = {}
        for seg in usuarios:
            for pub in self.bd.buscarPost(seg):
                self.pubs[int(pub.get_horario()
                         .replace(":", "").replace(" ", "").replace(".", "").replace("-", "")
                         )] = (pub.get_data(), pub.get_conteudo().split('/////')[0], seg, pub)

        self.i_sorted = sorted(self.pubs.keys(), reverse=True)

        for x in self.i_sorted:
            imagem = open(self.pubs[x][0], "rb").read()
            imagens.append(imagem.hex())
            autores.append(self.pubs[x][2])
            nomes.append(self.pubs[x][1])

        return imagens, nomes, autores

    def publicar(self, titulo, imagem, passos, tags):
        imagem = bytes.fromhex(imagem)
        self.bd.inserirPost(self.usuario.get_user(), Post(tags, '', str(datetime.now()),
                                                          f"{titulo}" + r"/////" + passos, ""), imagem)

    def get_titulo(self, index):
        dict_index = self.i_sorted[index]
        return self.pubs[dict_index][3].get_conteudo().split('/////')[0]

    def get_passos(self, index):
        dict_index = self.i_sorted[index]
        return self.pubs[dict_index][3].get_conteudo().split('/////')[1]

    def get_tags(self, index):
        dict_index = self.i_sorted[index]
        return self.pubs[dict_index][3].get_tags()

    def get_estrelas(self, index):
        dict_index = self.i_sorted[index]
        return self.pubs[dict_index][3].get_estrelas()

    def avaliar(self, index, estrelas):
        dict_index = self.i_sorted[index]
        self.pubs[dict_index][3].adiciona_estrela(estrelas)

        self.bd.atualizaBancoPost(post=self.pubs[dict_index][3])