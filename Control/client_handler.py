from Model.Usuario import Usuario
import Model.Banco as Bd
from Pyro5 import api
from Model.exceptions.CredenciaisErradasException import CredenciaisErradasException

from Model.exceptions.UserExisteException import UserExisteException
from Model.exceptions.SenhasNaoConferemException import SenhasNaoConferemException


@api.expose
class ClientHandler(object):
    def __init__(self):
        self.bd = Bd.Banco()

    def login(self, user_name, senha):
        r = self.bd.buscarUsuario(user_name, senha)
        if r is None:
            raise Exception(str(CredenciaisErradasException()))

    def cadastro(self, nome, user_name, email, senha, confirmar_senha):
        if senha == confirmar_senha:
            user = Usuario(nome, user_name, email, senha)
            try:
                self.bd.inserirUsuario(user)
            except UserExisteException as e:
                raise Exception(str(e))
        else:
            e = SenhasNaoConferemException()
            raise Exception(str(e))

