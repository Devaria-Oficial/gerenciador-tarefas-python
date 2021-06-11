from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def criptografar_senha(senha):
    return pwd_context.encrypt(senha)

def verificar_senha(senha, senha_criptografada):
    try:
        return pwd_context.verify(senha, senha_criptografada)
    except Exception:
        return False