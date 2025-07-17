from fastapi import APIRouter, HTTPException, Query
from services import dlc_service
from models.dlc import DLCCreate, DLCUpdate
from typing import Optional

router = APIRouter(prefix="/dlcs", tags=["DLCs"])

@router.post("/")
async def criar_dlc(data: DLCCreate):
    try:
        return await dlc_service.criar_dlc(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def listar_dlcs():
    try:
        return await dlc_service.listar_dlcs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{dlc_id}")
async def atualizar_dlc(dlc_id: str, data: DLCUpdate):
    try:
        atualizado = await dlc_service.atualizar_dlc(dlc_id, data)
        if not atualizado:
            raise HTTPException(status_code=404, detail="DLC nao encontrado para atualizar")
        return {"message": "DLC atualizado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{dlc_id}")
async def deletar_dlc(dlc_id: str):
    try:
        sucesso = await dlc_service.deletar_dlc(dlc_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="DLC nao encontrado")
        return {"message": "DLC deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/quantidade")
async def exibir_quantidade():
    try:
        quantidade = await dlc_service.exibir_quantidade()
        return {"quantidade": quantidade}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def buscar_jogos(
    titulo: Optional[str] = None,
    descricao: Optional[str] = None,
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
        return await dlc_service.buscar_dlcs(
            titulo, descricao,
            dia, mes, ano,
            precoAcimaDe, precoAbaixoDe,
            page, size, orderBy, orderDir
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{dlc_id}")
async def buscar_por_id(dlc_id: str):
    try:
        dlc = await dlc_service.buscar_por_id(dlc_id)
        if not dlc:
            raise HTTPException(status_code=404, detail="DLC nao encontrado")
        return dlc
    except ValueError:
        raise HTTPException(status_code=404, detail="Formato de ID invalido")
