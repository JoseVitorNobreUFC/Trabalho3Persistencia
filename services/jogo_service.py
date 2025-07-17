from models.jogo import JogoCreate, JogoDB, JogoUpdate
from repository import jogo_repository
from utils.logger import info_, error_
from typing import Optional

async def criar_jogo(jogo: JogoCreate) -> JogoDB:
    try:
        id = await jogo_repository.insert_jogo(jogo)
        info_(f"[SUCESSO] Jogo criado com ID {id}")
        return JogoDB(**jogo.dict(), _id=id)
    except Exception as e:
        error_(f"[ERRO] Falha ao criar jogo: {str(e)}")
        raise

async def listar_jogos() -> list[JogoDB]:
    try:
        docs = await jogo_repository.get_all_jogos()
        info_(f"[SUCESSO] Listagem de {len(docs)} jogo(s)")
        return [JogoDB.from_mongo(j) for j in docs]
    except Exception as e:
        error_(f"[ERRO] Falha ao listar jogos: {str(e)}")
        raise

async def buscar_por_id(jogo_id: str) -> JogoDB | None:
    try:
        doc = await jogo_repository.get_jogo_by_id(jogo_id)
        if doc:
            info_(f"[SUCESSO] Jogo encontrado com ID {jogo_id}")
            return JogoDB.from_mongo(doc)
        error_(f"[ERRO] Jogo com ID {jogo_id} não encontrado")
        return None
    except Exception as e:
        error_(f"[ERRO] Erro ao buscar jogo {jogo_id}: {str(e)}")
        raise

async def atualizar_jogo(jogo_id: str, dados: JogoUpdate) -> bool:
    try:
        sucesso = await jogo_repository.update_jogo(jogo_id, dados)
        if sucesso:
            info_(f"[SUCESSO] Jogo atualizado com ID {jogo_id}")
        else:
            error_(f"[ERRO] Jogo com ID {jogo_id} não encontrado para atualizar")
        return sucesso
    except Exception as e:
        error_(f"[ERRO] Falha ao atualizar jogo {jogo_id}: {str(e)}")
        raise

async def deletar_jogo(jogo_id: str) -> bool:
    try:
        sucesso = await jogo_repository.delete_jogo(jogo_id)
        if sucesso:
            info_(f"[SUCESSO] Jogo deletado com ID {jogo_id}")
        else:
            error_(f"[ERRO] Jogo com ID {jogo_id} não encontrado para deletar")
        return sucesso
    except Exception as e:
        error_(f"[ERRO] Falha ao deletar jogo {jogo_id}: {str(e)}")
        raise

async def buscar_jogos(
    titulo: Optional[str],
    descricao: Optional[str],
    desenvolvedora: Optional[str],
    dia: Optional[int],
    mes: Optional[int],
    ano: Optional[int],
    preco_min: Optional[float],
    preco_max: Optional[float],
    page: int = 1,
    size: int = 10,
    order_by: str = "titulo",
    order_dir: str = "asc"
):
    try:
        resultado = await jogo_repository.buscar_jogos(
            titulo, descricao, desenvolvedora, dia, mes, ano,
            preco_min, preco_max, page, size, order_by, order_dir
        )
        info_(f"[SUCESSO] Filtro de jogos retornou {len(resultado['content'])} item(ns)")
        return resultado
    except Exception as e:
        error_(f"[ERRO] Falha ao filtrar jogos: {str(e)}")
        raise
