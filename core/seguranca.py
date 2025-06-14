from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Chave secreta simbólica
SECRET_KEY = "kaivora-semente-sagrada"  # 💠 Trocar por variável de ambiente em produção
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Mock de banco de usuários
fake_users_db = {
    "carlos@kaivora.org": {
        "username": "carlos@kaivora.org",
        "nome": "Carlos Silva",
        "senha_hashed": "$2b$12$eR9tUsYk8sG5N2wHhj5VuOY3VwGO/qN3NBDAXXh2jZFrP33CzlfAy",  # senha: amorverdadeiro
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def autenticar_usuario(username: str, senha: str):
    user = fake_users_db.get(username)
    if not user:
        return None
    if not verificar_senha(senha, user["senha_hashed"]):
        return None
    return user

def criar_token_acesso(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        user = fake_users_db.get(username)
        return user
    except JWTError:
        return None
