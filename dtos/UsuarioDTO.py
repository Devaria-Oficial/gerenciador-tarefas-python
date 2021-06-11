class UsuarioBaseDTO:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

class UsuarioCreateDTO(UsuarioBaseDTO):
    def __init__(self, id, nome, usuario, senha):
        super().__init__(nome, usuario)
        self.id = id
        self.senha = senha

class UsuarioLoginDTO(UsuarioBaseDTO):
    def __init__(self, nome, email, token):
        super().__init__(nome, email)
        self.token = token
