from fastapi import APIRouter, HTTPException
from models.jogo import JogoCreate, JogoDB, JogoUpdate
from services import jogo_service

router = APIRouter(prefix="/jogos", tags=["Jogos"])

@router.post("/", response_model=JogoDB)
async def criar_jogo(jogo: JogoCreate):
    return await jogo_service.criar_jogo(jogo)

@router.get("/", response_model=list[JogoDB])
async def listar_jogos():
    return await jogo_service.listar_jogos()

@router.get("/{jogo_id}", response_model=JogoDB)
async def obter_jogo(jogo_id: str):
    jogo = await jogo_service.buscar_por_id(jogo_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return jogo

@router.put("/{jogo_id}", response_model=dict)
async def atualizar_jogo(jogo_id: str, dados: JogoUpdate):
    atualizado = await jogo_service.atualizar_jogo(jogo_id, dados)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Jogo não encontrado para atualizar")
    return {"message": "Jogo atualizado com sucesso"}

@router.delete("/{jogo_id}", response_model=dict)
async def deletar_jogo(jogo_id: str):
    deletado = await jogo_service.deletar_jogo(jogo_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Jogo não encontrado para deletar")
    return {"message": "Jogo deletado com sucesso"}
