# app/routers/estado.py
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/", summary="Obter Estado", tags=["kaivora"])
async def obter_estado():
    return {
        "estado": "Kaivora operante e ancorada na luz.",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
