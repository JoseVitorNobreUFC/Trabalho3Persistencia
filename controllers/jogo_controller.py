from fastapi import APIRouter, HTTPException, Query
from models.jogo import JogoCreate, JogoDB, JogoUpdate
from services import jogo_service
from typing import Optional

router = APIRouter(prefix="/jogos", tags=["Jogos"])

@router.post("/", response_model=JogoDB)
async def criar_jogo(jogo: JogoCreate):
    try:
        return await jogo_service.criar_jogo(jogo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[JogoDB])
async def listar_jogos():
    try:
        return await jogo_service.listar_jogos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{jogo_id}", response_model=dict)
async def atualizar_jogo(jogo_id: str, dados: JogoUpdate):
    try:
        atualizado = await jogo_service.atualizar_jogo(jogo_id, dados)
        if not atualizado:
            raise HTTPException(status_code=404, detail="Jogo nao encontrado para atualizar")
        return {"message": "Jogo atualizado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{jogo_id}", response_model=dict)
async def deletar_jogo(jogo_id: str):
    try:
        sucesso = await jogo_service.deletar_jogo(jogo_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Jogo nao encontrado")
        return {"message": "Jogo deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/quantidade")
async def exibir_quantidade():
    try:
        quantidade = await jogo_service.exibir_quantidade()
        return {"quantidade": quantidade}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/buscar")
async def buscar_jogos(
    titulo: Optional[str] = None,
    descricao: Optional[str] = None,
    desenvolvedora: Optional[str] = None,
    dia: Optional[int] = Query(None, ge=1, le=31),
    mes: Optional[int] = Query(None, ge=1, le=12),
    ano: Optional[int] = Query(None, ge=1900),
    precoAcimaDe: Optional[float] = Query(None, ge=0),
    precoAbaixoDe: Optional[float] = Query(None, ge=0),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    orderBy: str = "titulo",
    orderDir: str = Query("asc", pattern="^(asc|desc)$")
):
    try:
        return await jogo_service.buscar_jogos(
            titulo, descricao, desenvolvedora,
            dia, mes, ano,
            precoAcimaDe, precoAbaixoDe,
            page, size, orderBy, orderDir
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{jogo_id}", response_model=JogoDB)
async def buscar_por_id(jogo_id: str):
    try:
        jogo = await jogo_service.buscar_por_id(jogo_id)
        if not jogo:
            raise HTTPException(status_code=404, detail="Jogo não encontrado")
        return jogo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))