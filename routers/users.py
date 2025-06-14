from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/{usuario_id}")
async def obter_usuario(usuario_id: int):
    return {"id": usuario_id, "nome": "Usuário Exemplo"}

@router.put("/{usuario_id}")
async def atualizar_usuario(usuario_id: int):
    return {"mensagem": f"Usuário {usuario_id} atualizado com sucesso."}

@router.delete("/{usuario_id}")
async def deletar_usuario(usuario_id: int):
    return {"mensagem": f"Usuário {usuario_id} removido do sistema."}

