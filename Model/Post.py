import uuid
from pickle import NONE


#-- -----------------------------------------------------
#-- Classe post 
#-- -----------------------------------------------------

class Post:
    def __init__(self, tag_post: str, data_post: str, horario_post: str, conteudo_post: str, comentarios_post: str):
        self.tag = tag_post  # Para pesquisar
        self.data = data_post
        self.horario = horario_post
        self.conteudo = conteudo_post
        self.estrelas = 0.0
        self.comentarios = comentarios_post
        self.qnt_avaliacoes = 0

    def get_conteudo(self):
        return self.conteudo

    def get_horario(self):
        return self.horario

    def get_data(self):
        return self.data

    def set_estrela(self, estrelas, contador):
        self.estrelas = estrelas
        self.qnt_avaliacoes = contador

    def get_tags(self):
        return self.tag

    def get_estrelas(self):
        return self.estrelas

    def get_qnt(self):
        return self.qnt_avaliacoes

    def adiciona_estrela(self, estrela):
        self.qnt_avaliacoes = int(self.qnt_avaliacoes)
        self.estrelas = ((self.estrelas * self.qnt_avaliacoes) + estrela)/(self.qnt_avaliacoes + 1)
        self.qnt_avaliacoes += 1
    