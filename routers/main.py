from fastapi import FastAPI
from roteadores import auth, usuarios, mensagens

app = FastAPI(title="Kaivora API")

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(mensagens.router)
