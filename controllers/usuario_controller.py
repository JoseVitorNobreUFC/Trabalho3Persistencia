from fastapi import APIRouter, HTTPException, Query
from services import usuario_service
from models.usuario import UsuarioCreate, UsuarioUpdate
from typing import Optional

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/")
async def criar_usuario(data: UsuarioCreate):
  try:
    return await usuario_service.criar_usuario(data)
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
  
@router.get("/")
async def listar_usuarios():
  try:
    return await usuario_service.listar_usuarios()
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
@router.get("/quantidade")
async def exibir_quantidade():
  try:
    quantidade = await usuario_service.exibir_quantidade()
    return {"quantidade": quantidade}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
@router.get("/buscar")
async def buscar_usuarios(
  nome: Optional[str] = None,
  dia: Optional[int] = Query(None, ge=1, le=31),
  mes: Optional[int] = Query(None, ge=1, le=12),
  ano: Optional[int] = Query(None, ge=1900),
  email: Optional[str] = None,
  pais: Optional[str] = None,
  page: int = Query(1, ge=1),
  size: int = Query(10, ge=1, le=100),
  orderBy: str = "nome",
  orderDir: str = Query("asc", pattern="^(asc|desc)$")
):
  try:
    return await usuario_service.buscar_usuarios(
      nome, dia, mes, ano, email, pais,
      page, size, orderBy, orderDir
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
@router.put("/{usuario_id}")
async def atualizar_usuario(usuario_id: str, data: UsuarioUpdate):
  try:
    atualizado = await usuario_service.atualizar_usuario(usuario_id, data)
    if not atualizado:
      raise HTTPException(status_code=404, detail="Usuário nao encontrado para atualizar")
    return {"message": "Usuário atualizado com sucesso"}
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{usuario_id}")
async def deletar_usuario(usuario_id: str):
  try:
    sucesso = await usuario_service.deletar_usuario(usuario_id)
    if not sucesso:
      raise HTTPException(status_code=404, detail="Usuário nao encontrado")
    return {"message": "Usuário deletado com sucesso"}
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
  
@router.get("/{usuario_id}")
async def buscar_por_id(usuario_id: str):
  try:
    usuario = await usuario_service.buscar_por_id(usuario_id)
    if not usuario:
      raise HTTPException(status_code=404, detail="Usuário nao encontrado")
    return usuario
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
  
@router.patch("/{usuario_id}/adicionarNaFamilia/{familia_id}")
async def adicionar_usuario_em_familia(usuario_id: str, familia_id: str):
    try:
        sucesso = await usuario_service.adicionar_usuario_em_familia(usuario_id, familia_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {"message": f"Usuário adicionado à família com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{criador_id}/adicionarEmFamiliaPrivada/{familia_id}/{usuario_id}")
async def adicionar_em_familia_privada(usuario_id: str, familia_id: str, criador_id: str):
    try:
        sucesso = await usuario_service.adicionar_usuario_em_familia_privada(usuario_id, familia_id, criador_id)
        return {"success": sucesso}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.patch("/{usuario_id}/removerDaFamilia")
async def remover_usuario_da_familia(usuario_id: str):
    try:
        sucesso = await usuario_service.remover_usuario_da_familia(usuario_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {"message": f"Usuário removido da família com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))