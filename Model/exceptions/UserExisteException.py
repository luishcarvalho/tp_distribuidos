class UserExisteException(Exception):
    def __init__(self, user_name):
        # Call the base class constructor with the parameters it needs
        super().__init__(f'Nome de usuário "{user_name}" já utilizado')

        self.user = user_name

    def get_name(self):
        return self.user
