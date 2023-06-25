#-- -----------------------------------------------------
#-- Classe usuario
#-- -----------------------------------------------------


class Usuario:
    def __init__(self, nome: str, user: str, email:str, senha:str):
        self.nome = nome
        self.user = user
        self.email = email
        self.senha = senha
        self.sou_seguidor = []

    def get_user(self):
        return self.user

    def get_sou_seguidor(self):
        return self.sou_seguidor

    def get_nome(self):
        return self.nome

    def get_email(self):
        return self.email

    def get_senha(self):
        return self.senha

    def inserir_seguidores(self, seguidores: list[str]):
        self.sou_seguidor.extend(seguidores)

    def remover_seguidor(self, seguidor):
        self.sou_seguidor.remove(seguidor)

        
    
