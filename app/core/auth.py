# app/core/auth.py

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings, ALGORITHM

# 🔐 Criação do contexto para criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🧂 Função para criar o hash da senha (armazenar no banco)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 🔍 Função para verificar se a senha informada bate com o hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 🛡️ Função para gerar o token JWT de acesso
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

