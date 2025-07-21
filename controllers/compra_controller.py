from fastapi import APIRouter, HTTPException, Query
from services import compra_service
from models.compra import CompraCreate, CompraUpdate
from typing import Optional

router = APIRouter(prefix="/compras", tags=["Compras"])

@router.post("/")
async def criar_compra(data: CompraCreate):
    try:
        return await compra_service.criar_compra(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def listar_compras():
    try:
        return await compra_service.listar_compras()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quantidade")
async def exibir_quantidade():
    try:
        quantidade = await compra_service.exibir_quantidade()
        return {"quantidade": quantidade}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/buscar")
async def buscar_compras(
    forma_pagamento: Optional[str] = Query(None, regex="^(Cartão|Boleto|Pix)$"),
    dia: Optional[int] = Query(None, ge=1, le=31),
    mes: Optional[int] = Query(None, ge=1, le=12),
    ano: Optional[int] = Query(None, ge=1900),
    preco_min: Optional[float] = Query(None, ge=0),
    preco_max: Optional[float] = Query(None, ge=0),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    orderBy: str = "data",
    orderDir: str = Query("asc", pattern="^(asc|desc)$")
):
    try:
        return await compra_service.buscar_compras(
            forma_pagamento, dia, mes, ano,
            preco_min, preco_max, page, size, orderBy, orderDir
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{compra_id}")
async def buscar_por_id(compra_id: str):
    try:
        compra = await compra_service.buscar_por_id(compra_id)
        if not compra:
            raise HTTPException(status_code=404, detail="Compra não encontrada")
        return compra
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{compra_id}")
async def atualizar_compra(compra_id: str, data: CompraUpdate):
    try:
        sucesso = await compra_service.atualizar_compra(compra_id, data)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Compra não encontrada para atualizar")
        return {"message": "Compra atualizada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{compra_id}")
async def deletar_compra(compra_id: str):
    try:
        sucesso = await compra_service.deletar_compra(compra_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Compra não encontrada")
        return {"message": "Compra deletada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))