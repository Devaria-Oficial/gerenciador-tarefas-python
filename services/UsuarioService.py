from database.database import SessionLocal
from models.Usuario import Usuario
from utils.Criptografia import verificar_senha, criptografar_senha

db = SessionLocal()

class UsuarioService:
    def __init__(self):
        pass

    def login(self, email, senha):
        usuario = db.query(Usuario).filter(Usuario.email == email).first()

        if not usuario:
            return None
        if not verificar_senha(senha, usuario.senha):
            return None

        return usuario

    def filter_by_email(self, email):
        return db.query(Usuario).filter(Usuario.email == email).first()

    def filter_by_id(self, id):
        return db.query(Usuario).filter(Usuario.id == id).first()

    def criar_usuario(self, nome, email, senha):
        if self.filter_by_email(email):
            return None

        novo_usuario = Usuario(nome=nome, email=email, senha=criptografar_senha(senha))

        db.add(novo_usuario)
        db.commit()

        return novo_usuario

