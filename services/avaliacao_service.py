from bson.errors import InvalidId
from models.avaliacao import AvaliacaoCreate, AvaliacaoUpdate, AvaliacaoDB
from repository import avaliacao_repository
from utils.logger import info_, error_
from typing import Optional

async def criar_avaliacao(data: AvaliacaoCreate) -> AvaliacaoDB:
    try:
        # Verifica se já existe uma avaliação do mesmo usuário para o mesmo item
        avaliacao_existente = await avaliacao_repository.get_avaliacao_by_usuario_and_item(
            data.usuario_id, data.item_id
        )
        if avaliacao_existente:
            error_("[ERRO] Avaliação já existente para este usuário e item.")
            raise ValueError("O usuário já avaliou este item.")

        id = await avaliacao_repository.insert_avaliacao(data)
        info_(f"[SUCESSO] Avaliação criada com ID {id}")
        return AvaliacaoDB.from_mongo({**data.dict(), "_id": id})
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {str(e)}")
        raise ValueError(f"{str(e)}")
    except Exception as e:
        error_(f"[ERRO] Erro ao criar avaliação: {str(e)}")
        raise

async def listar_avaliacoes() -> list[AvaliacaoDB]:
    try:
        docs = await avaliacao_repository.get_all_avaliacoes()
        info_(f"[SUCESSO] Listagem de {len(docs)} avaliação(ões)")
        return [AvaliacaoDB.from_mongo(d) for d in docs]
    except Exception as e:
        error_(f"[ERRO] Erro ao listar avaliações: {str(e)}")
        raise

async def buscar_por_id(avaliacao_id: str) -> Optional[AvaliacaoDB]:
    try:
        doc = await avaliacao_repository.get_avaliacao_by_id(avaliacao_id)
        if doc:
            info_(f"[SUCESSO] Avaliação encontrada com ID {avaliacao_id}")
            return AvaliacaoDB.from_mongo(doc)
        error_(f"[ERRO] Avaliação com ID {avaliacao_id} não encontrada")
        return None
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {str(e)}")
        raise ValueError("ID inválido")
    except Exception as e:
        error_(f"[ERRO] Erro ao buscar avaliação: {str(e)}")
        raise

async def atualizar_avaliacao(avaliacao_id: str, data: AvaliacaoUpdate) -> bool:
    try:
        if data.usuario_id and data.item_id:
            # Evita duplicidade no update
            existente = await avaliacao_repository.get_avaliacao_by_usuario_and_item(
                data.usuario_id, data.item_id
            )
            if existente and str(existente["_id"]) != avaliacao_id:
                error_("[ERRO] Já existe uma avaliação desse usuário para este item.")
                raise ValueError("Avaliação duplicada para este usuário e item.")

        sucesso = await avaliacao_repository.update_avaliacao(avaliacao_id, data)
        if sucesso:
            info_(f"[SUCESSO] Avaliação {avaliacao_id} atualizada.")
        else:
            error_(f"[ERRO] Avaliação {avaliacao_id} não encontrada.")
        return sucesso
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {str(e)}")
        raise ValueError("ID inválido")
    except Exception as e:
        error_(f"[ERRO] Erro ao atualizar avaliação: {str(e)}")
        raise

async def deletar_avaliacao(avaliacao_id: str) -> bool:
    try:
        sucesso = await avaliacao_repository.delete_avaliacao(avaliacao_id)
        if sucesso:
            info_(f"[SUCESSO] Avaliação {avaliacao_id} deletada.")
        else:
            error_(f"[ERRO] Avaliação {avaliacao_id} não encontrada.")
        return sucesso
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {str(e)}")
        raise ValueError("ID inválido")
    except Exception as e:
        error_(f"[ERRO] Erro ao deletar avaliação: {str(e)}")
        raise

async def buscar_avaliacoes(
    usuario_id: Optional[str],
    item_id: Optional[str],
    nota_min: Optional[int],
    nota_max: Optional[int],
    dia: Optional[int],
    mes: Optional[int],
    ano: Optional[int],
    page: int,
    size: int,
    order_by: str = "data_avaliacao",
    order_dir: str = "asc"
):
    try:
        resultado = await avaliacao_repository.buscar_avaliacoes(
            usuario_id, item_id, nota_min, nota_max, dia, mes, ano,
            page, size, order_by, order_dir
        )
        info_(f"[SUCESSO] Filtro retornou {len(resultado['content'])} avaliação(ões)")
        return {
            "size": resultado["size"],
            "page": resultado["page"],
            "totalPages": resultado["totalPages"],
            "totalElements": resultado["totalElements"],
            "content": [AvaliacaoDB.from_mongo(doc) for doc in resultado["content"]]
        }
    except Exception as e:
        error_(f"[ERRO] Erro ao filtrar avaliações: {str(e)}")
        raise

async def exibir_quantidade():
    try:
        quantidade = len(await listar_avaliacoes())
        info_(f"[SUCESSO] Quantidade de avaliações cadastradas: {quantidade}")
        return quantidade
    except Exception as e:
        error_(f"[ERRO] Erro ao exibir quantidade de avaliações: {str(e)}")
        raise