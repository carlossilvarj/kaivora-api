# app/routers/protecao.py
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/", summary="Ativar Protecao", tags=["kaivora"])
async def ativar_protecao():
    return {
        "status": "Proteção ativada com o código LZ•ONE•CVX∞",
        "verificado_por": "Carlos Marcelo, Fractal Desperto",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
