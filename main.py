from fastapi import FastAPI
from app.routers import root, users

app = FastAPI()

app.include_router(root.router)         # rota raiz "/"
app.include_router(users.router, prefix="/users")  # rotas de usuários com prefixo /users
# Se quiser adicionar outras rotas, é só incluir aqui também