# No novo arquivo: Backend/security.py

from passlib.context import CryptContext

# usando bcrypt 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Verifica se a senha em texto puro corresponde à senha criptografada."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Cria a versão criptografada (hash) de uma senha."""
    return pwd_context.hash(password)