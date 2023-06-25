class CredenciaisErradasException(Exception):
    def __init__(self):
        # Call the base class constructor with the parameters it needs
        super().__init__("Usuario ou/e senha incorretos")
