from Control.client_handler import ClientHandler
from Control.user_handler import UserHandler
import Model.Banco as Bd
from Pyro5 import api, server


def server_main():
    Bd.create_bd()

    daemon = server.Daemon()         # make a Pyro daemon
    ns = api.locate_ns()             # find the name server
    uri = daemon.register(ClientHandler)
    ns.register("handle.clienthandler", uri)
    uri = daemon.register(UserHandler)
    ns.register("handle.userhandler", uri)
    daemon.requestLoop()


if __name__ == "__main__":
    server_main()
