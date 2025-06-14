from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from essencial.seguranca import autenticar_usuario, criar_token_acesso, verificar_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = autenticar_usuario(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )
    access_token = criar_token_acesso(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verificar")
async def verificar_token_route(token: str = Depends(oauth2_scheme)):
    user = verificar_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )
    return {"mensagem": f"Token válido. Bem-vindo, {user['username']}!"}

