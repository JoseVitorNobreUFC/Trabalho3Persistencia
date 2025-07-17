from repository import dlc_repository
from repository.jogo_repository import get_jogo_by_id
from models.dlc import DLCCreate, DLCUpdate, DLCDB
from utils.logger import info_, error_
from bson.errors import InvalidId
from typing import Optional

async def criar_dlc(dlc: DLCCreate):
    # Verifica se o jogo existe
    jogo = await get_jogo_by_id(dlc.jogo_id)
    if not jogo:
        error_(f"[ERRO] Jogo {dlc.jogo_id} não encontrado.")
        raise ValueError("O jogo informado não existe.")

    # Verifica se já existe uma DLC associada
    if await dlc_repository.get_dlc_by_jogo(dlc.jogo_id):
        error_(f"[ERRO] Jogo {dlc.jogo_id} já possui DLC.")
        raise ValueError("Esse jogo já possui uma DLC registrada.")

    try:
        id = await dlc_repository.insert_dlc(dlc)
        info_(f"[SUCESSO] DLC criada com id {id}")
        return DLCDB.from_mongo({**dlc.dict(), "_id": id})
    except Exception as e:
        error_(f"[ERRO] Falha ao criar DLC: {e}")
        raise

async def listar_dlcs():
    try:
        docs = await dlc_repository.get_all_dlcs()
        info_(f"[SUCESSO] Listagem de {len(docs)} DLC(s)")
        return [DLCDB.from_mongo(d) for d in docs]
    except Exception as e:
        error_(f"[ERRO] Falha ao listar DLCs: {e}")
        raise

async def buscar_por_id(dlc_id: str):
    try:
        docs = await dlc_repository.get_dlc_by_id(dlc_id)
        if docs:
            info_(f"[SUCESSO] DLC encontrado com id {dlc_id}")
            return DLCDB.from_mongo(docs)
        error_(f"[ERRO] DLC com id {dlc_id} nao encontrado")
        return None
    except Exception as e:
        error_(f"[ERRO] Erro ao buscar DLC {dlc_id}: {e}")
        raise

async def atualizar_dlc(dlc_id: str, data: DLCUpdate):
    try:
        # Verifica se a DLC existe
        dlc_existente = await dlc_repository.get_dlc_by_id(dlc_id)
        if not dlc_existente:
            error_(f"[ERRO] DLC {dlc_id} não encontrada.")
            raise ValueError("DLC não encontrada.")

        # Se o jogo_id for atualizado, validar novamente
        if data.jogo_id and data.jogo_id != dlc_existente["jogo_id"]:
            jogo = await get_jogo_by_id(data.jogo_id)
            if not jogo:
                error_(f"[ERRO] Jogo {data.jogo_id} não encontrado.")
                raise ValueError("O jogo informado não existe.")

            if await dlc_repository.get_dlc_by_jogo(data.jogo_id):
                error_(f"[ERRO] Jogo {data.jogo_id} já possui DLC.")
                raise ValueError("Esse jogo já possui uma DLC registrada.")

        if await dlc_repository.update_dlc(dlc_id, data):
            info_(f"[SUCESSO] DLC {dlc_id} atualizada.")
            return True

        error_(f"[ERRO] Falha ao atualizar DLC {dlc_id}")
        return False

    except InvalidId:
        error_(f"[ERRO] ID inválido ao atualizar DLC: {dlc_id}")
        raise ValueError("ID de DLC inválido")

async def deletar_dlc(dlc_id: str):
    try:
        sucesso = await dlc_repository.delete_dlc(dlc_id)
        if sucesso:
            info_(f"[SUCESSO] DLC deletado com id {dlc_id}")
        else:
            error_(f"[ERRO] DLC com id {dlc_id} nao encontrado para deletar")
        return sucesso
    except Exception as e:
        error_(f"[ERRO] Falha ao deletar DLC {dlc_id}: {e}")
        raise

async def buscar_dlcs(
    titulo: Optional[str],
    descricao: Optional[str],
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
        resultado = await dlc_repository.buscar_dlcs(
            titulo, descricao, dia, mes, ano,
            preco_min, preco_max, page, size, order_by, order_dir
        )
        info_(f"[SUCESSO] Filtro de DLCs retornou {len(resultado['content'])} item(ns)")
        return resultado
    except Exception as e:
        error_(f"[ERRO] Falha ao filtrar DLCs: {str(e)}")
        raise
    
async def exibir_quantidade():
    try:
        quantidade = len(await listar_dlcs())
        info_(f"[SUCESSO] Quantidade de DLCs cadastrados: {quantidade}")
        return quantidade
    except Exception as e:
        error_(f"[ERRO] Falha ao exibir quantidade de DLCs: {str(e)}")
        raise