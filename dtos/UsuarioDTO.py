class UsuarioBaseDTO:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

class UsuarioLoginDTO(UsuarioBaseDTO):
    def __init__(self, nome, email, token):
        super().__init__(nome, email)
        self.token = token
