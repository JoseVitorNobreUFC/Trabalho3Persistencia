from fastapi import APIRouter, HTTPException, Query
from services import avaliacao_service
from models.avaliacao import AvaliacaoCreate, AvaliacaoUpdate
from typing import Optional

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])

@router.post("/")
async def criar_avaliacao(data: AvaliacaoCreate):
    try:
        return await avaliacao_service.criar_avaliacao(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def listar_avaliacoes():
    try:
        return await avaliacao_service.listar_avaliacoes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quantidade")
async def exibir_quantidade():
    try:
        quantidade = await avaliacao_service.exibir_quantidade()
        return {"quantidade": quantidade}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/buscar")
async def buscar_avaliacoes(
    usuario_id: Optional[str] = None,
    item_id: Optional[str] = None,
    nota_min: Optional[int] = Query(None, ge=0, le=10),
    nota_max: Optional[int] = Query(None, ge=0, le=10),
    dia: Optional[int] = Query(None, ge=1, le=31),
    mes: Optional[int] = Query(None, ge=1, le=12),
    ano: Optional[int] = Query(None, ge=1900),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    orderBy: str = "data_avaliacao",
    orderDir: str = Query("asc", pattern="^(asc|desc)$")
):
    try:
        return await avaliacao_service.buscar_avaliacoes(
            usuario_id, item_id, nota_min, nota_max,
            dia, mes, ano, page, size, orderBy, orderDir
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{avaliacao_id}")
async def buscar_por_id(avaliacao_id: str):
    try:
        avaliacao = await avaliacao_service.buscar_por_id(avaliacao_id)
        if not avaliacao:
            raise HTTPException(status_code=404, detail="Avaliação não encontrada")
        return avaliacao
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{avaliacao_id}")
async def atualizar_avaliacao(avaliacao_id: str, data: AvaliacaoUpdate):
    try:
        atualizado = await avaliacao_service.atualizar_avaliacao(avaliacao_id, data)
        if not atualizado:
            raise HTTPException(status_code=404, detail="Avaliação não encontrada para atualizar")
        return {"message": "Avaliação atualizada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{avaliacao_id}")
async def deletar_avaliacao(avaliacao_id: str):
    try:
        sucesso = await avaliacao_service.deletar_avaliacao(avaliacao_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Avaliação não encontrada")
        return {"message": "Avaliação deletada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))