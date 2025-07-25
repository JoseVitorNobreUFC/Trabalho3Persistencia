from fastapi import APIRouter, HTTPException
from services import query_complexas_service

router = APIRouter(prefix="/query", tags=["Consultas Complexas"])

@router.get("/item/{item_id}/reviews")
async def obter_dados_item(jogo_id: str):
    try:
        return await query_complexas_service.obter_dados_item(jogo_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/usuario/{usuario_id}/perfil")
async def obter_perfil_usuario(usuario_id: str):
    try:
        return await query_complexas_service.obter_perfil_usuario(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/familia/dados")
async def obter_dados_familias():
    try:
        return await query_complexas_service.obter_dados_familias()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
