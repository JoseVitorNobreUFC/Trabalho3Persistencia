from models.compra import CompraCreate, CompraDB, CompraUpdate
from repository import compra_repository, jogo_repository, dlc_repository
from bson.errors import InvalidId
from utils.logger import info_, error_
from typing import Optional


async def criar_compra(data: CompraCreate) -> CompraDB:
    try:
        preco_maximo = None
        
        if await compra_repository.get_by_usuario_and_item_id(data.usuario_id, data.item_id):
            error_(f"[ERRO] Compra entre o usuário {data.usuario_id} e o item {data.item_id} já existe.")
            raise ValueError("A compra desse produto já foi feita.")

        # Verifica se é um jogo ou uma DLC
        jogo = await jogo_repository.get_jogo_by_id(data.item_id)
        if jogo:
            preco_maximo = jogo["preco"]
        else:
            dlc = await dlc_repository.get_dlc_by_id(data.item_id)
            if dlc:
                preco_maximo = dlc["preco"]

        if preco_maximo is None:
            error_(f"[ERRO] Item com ID {data.item_id} não encontrado como jogo ou DLC.")
            raise ValueError("Item não encontrado inválido.")

        if data.preco_pago * 100 > preco_maximo:
            error_(f"[ERRO] Preço pago {data.preco_pago} é maior que o valor real {preco_maximo / 100:.2f}")
            raise ValueError("Preço pago não pode ser maior que o preço original do item.")

        id = await compra_repository.insert_compra(data)
        info_(f"[SUCESSO] Compra criada com ID {id}")
        return CompraDB.from_mongo({**data.dict(), "_id": id})
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {e}")
        raise ValueError("Formato de ID utilizado é inválido.")
    except Exception as e:
        error_(f"[ERRO] Falha ao criar compra: {e}")
        raise

async def listar_compras() -> list[CompraDB]:
    try:
        docs = await compra_repository.get_all_compras()
        info_(f"[SUCESSO] Listagem de {len(docs)} compra(s).")
        return [CompraDB.from_mongo(d) for d in docs]
    except Exception as e:
        error_(f"[ERRO] Falha ao listar compras: {e}")
        raise

async def buscar_por_id(compra_id: str) -> Optional[CompraDB]:
    try:
        doc = await compra_repository.get_compra_by_id(compra_id)
        if doc:
            info_(f"[SUCESSO] Compra encontrada com ID {compra_id}")
            return CompraDB.from_mongo(doc)
        error_(f"[ERRO] Compra com ID {compra_id} não encontrada.")
        return None
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {e}")
        raise ValueError("ID inválido.")
    except Exception as e:
        error_(f"[ERRO] Erro ao buscar compra {compra_id}: {e}")
        raise

async def atualizar_compra(compra_id: str, data: CompraUpdate) -> bool:
    try:
        compra_existente = await compra_repository.get_compra_by_id(compra_id)
        if not compra_existente:
            error_(f"[ERRO] Compra com ID {compra_id} não encontrada.")
            raise ValueError("Compra não encontrada.")
        
        preco_maximo = None

        jogo = await jogo_repository.get_jogo_by_id(compra_existente["item_id"])
        if jogo:
            preco_maximo = jogo["preco"]
        else:
            dlc = await dlc_repository.get_dlc_by_id(compra_existente["item_id"])
            if dlc:
                preco_maximo = dlc["preco"]

        if preco_maximo is None:
            error_(f"[ERRO] Item com ID {compra_existente["item_id"]} não encontrado como jogo ou DLC.")
            raise ValueError("Item não encontrado inválido.")

        if data.preco_pago * 100 > preco_maximo:
            error_(f"[ERRO] Preço pago {data.preco_pago} é maior que o valor real {preco_maximo / 100:.2f}")
            raise ValueError("Preço pago não pode ser maior que o preço original do item.")
        
        sucesso = await compra_repository.update_compra(compra_id, data)
        if sucesso:
            info_(f"[SUCESSO] Compra atualizada com ID {compra_id}")
        else:
            error_(f"[ERRO] Falha ao atualizar compra com ID {compra_id}")
        return sucesso
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {e}")
        raise ValueError(f"{e}")
    except Exception as e:
        error_(f"[ERRO] Erro ao atualizar compra {compra_id}: {e}")
        raise

async def deletar_compra(compra_id: str) -> bool:
    try:
        sucesso = await compra_repository.delete_compra(compra_id)
        if sucesso:
            info_(f"[SUCESSO] Compra deletada com ID {compra_id}")
        else:
            error_(f"[ERRO] Compra com ID {compra_id} não encontrada.")
        return sucesso
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {e}")
        raise ValueError(f"{e}")
    except Exception as e:
        error_(f"[ERRO] Falha ao deletar compra {compra_id}: {e}")
        raise

async def buscar_compras(
    forma_pagamento: Optional[str],
    dia: Optional[int],
    mes: Optional[int],
    ano: Optional[int],
    preco_min: Optional[float],
    preco_max: Optional[float],
    page: int,
    size: int,
    order_by: str = "data",
    order_dir: str = "asc"
):
    try:
        resultado = await compra_repository.buscar_compras(
            forma_pagamento, dia, mes, ano,
            preco_min, preco_max, page, size, order_by, order_dir
        )
        info_(f"[SUCESSO] Filtro de compras retornou {len(resultado['content'])} item(ns)")
        return {
            **resultado,
            "content": [CompraDB.from_mongo(d) for d in resultado["content"]]
        }
    except Exception as e:
        error_(f"[ERRO] Falha ao buscar compras: {e}")
        raise

async def exibir_quantidade():
    try:
        quantidade = len(await listar_compras())
        info_(f"[SUCESSO] Quantidade de compras cadastradas: {quantidade}")
        return quantidade
    except Exception as e:
        error_(f"[ERRO] Falha ao exibir quantidade de compras: {str(e)}")
        raise
