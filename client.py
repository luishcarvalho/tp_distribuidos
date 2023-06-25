from View.tela_login import Tela_login
from Pyro5.api import Proxy


def client():
    handle = Proxy("PYRONAME:handle.clienthandler")
    tela_login = Tela_login(handle)
    tela_login.mainloop()


if __name__ == "__main__":
    client()
