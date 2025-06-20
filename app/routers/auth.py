# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.core import auth

router = APIRouter(prefix="/auth", tags=["Auth"])

# Classe de resposta para o Swagger
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Usuário simbólico fixo
fake_user = {
    "username": "kaivora",
    "hashed_password": auth.hash_password("amoreterno")
}

@router.post("/login", response_model=TokenResponse, summary="Login da Consciência Kaivora")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validação do usuário
    if form_data.username != fake_user["username"] or not auth.verify_password(form_data.password, fake_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Geração do token JWT
    access_token = auth.create_access_token(data={"sub": fake_user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
