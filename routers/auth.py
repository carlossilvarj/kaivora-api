from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Autenticação"])

class LoginRequest(BaseModel):
    email: str
    senha: str

@router.post("/login")
def login(request: LoginRequest):
    # Lógica de autenticação virá aqui
    return {"mensagem": "Login realizado com sucesso (mockado)"}

@router.post("/registro")
def registrar_usuario(request: LoginRequest):
    # Registro de novo usuário (provisório)
    return {"mensagem": "Usuário registrado com sucesso (mockado)"}
