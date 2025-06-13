from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "API funcionando! Seja bem-vindo(a)."}