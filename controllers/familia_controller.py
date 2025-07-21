from fastapi import APIRouter, HTTPException, Query
from services import familia_service
from models.familia import FamiliaCreate, FamiliaUpdate
from typing import Optional

router = APIRouter(prefix="/familias", tags=["Famílias"])

@router.post("/")
async def criar_familia(data: FamiliaCreate):
    try:
        return await familia_service.criar_familia(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def listar_familias():
    try:
        return await familia_service.listar_familias()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quantidade")
async def exibir_quantidade():
    try:
        quantidade = await familia_service.exibir_quantidade()
        return {"quantidade": quantidade}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/membros/{familia_id}")
async def exibir_membros_familia(familia_id: str):
    try:
        membros = await familia_service.exibir_membros_familia(familia_id)
        return membros
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/buscar")
async def buscar_familias(
    nome: Optional[str] = None,
    descricao: Optional[str] = None,
    is_public: Optional[bool] = None,
    dia: Optional[int] = Query(None, ge=1, le=31),
    mes: Optional[int] = Query(None, ge=1, le=12),
    ano: Optional[int] = Query(None, ge=1900),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    orderBy: str = "nome",
    orderDir: str = Query("asc", pattern="^(asc|desc)$")
):
    try:
        return await familia_service.buscar_familias(
            nome, descricao, is_public,
            dia, mes, ano,
            page, size, orderBy, orderDir
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{familia_id}")
async def buscar_por_id(familia_id: str):
    try:
        familia = await familia_service.buscar_por_id(familia_id)
        if not familia:
            raise HTTPException(status_code=404, detail="Família não encontrada")
        return familia
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{familia_id}")
async def atualizar_familia(familia_id: str, data: FamiliaUpdate):
    try:
        atualizado = await familia_service.atualizar_familia(familia_id, data)
        if not atualizado:
            raise HTTPException(status_code=404, detail="Família não encontrada para atualizar")
        return {"message": "Família atualizada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{familia_id}")
async def deletar_familia(familia_id: str):
    try:
        sucesso = await familia_service.deletar_familia(familia_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Família não encontrada")
        return {"message": "Família deletada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))