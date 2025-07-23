from repository import query_complexas_repository
from utils.logger import info_, error_
from bson.errors import InvalidId

async def obter_dados_item(jogo_id: str):
    try:
        resultado = await query_complexas_repository.obter_dados_item(jogo_id)
        info_(f"[SUCESSO] Reviews do jogo {jogo_id} recuperadas")
        return resultado
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {e}")
        raise ValueError("ID inválido")
    except Exception as e:
        error_(f"[ERRO] Falha ao buscar reviews do jogo {jogo_id}: {e}")
        raise

async def obter_perfil_usuario(usuario_id: str):
    try:
        resultado = await query_complexas_repository.obter_perfil_usuario(usuario_id)
        info_(f"[SUCESSO] Perfil do usuário {usuario_id} recuperado")
        return resultado
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {e}")
        raise ValueError("ID inválido")
    except Exception as e:
        error_(f"[ERRO] Falha ao obter perfil do usuário {usuario_id}: {e}")
        raise

async def obter_dados_familias():
    try:
        resultado = await query_complexas_repository.obter_dados_familias()
        info_(f"[SUCESSO] Dados das famílias recuperado")
        return resultado
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {e}")
        raise ValueError("ID inválido")
    except Exception as e:
        error_(f"[ERRO] Falha ao calcular valor total das família: {e}")
        raise
