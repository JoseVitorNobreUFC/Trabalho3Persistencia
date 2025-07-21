from models.familia import FamiliaCreate, FamiliaUpdate, FamiliaDB
from models.usuario import UsuarioUpdate
from repository import familia_repository, usuario_repository
from utils.logger import info_, error_
from bson.errors import InvalidId
from typing import Optional
from bson import ObjectId

async def criar_familia(data: FamiliaCreate) -> FamiliaDB:
    try:
        usuario = await usuario_repository.get_usuario_by_id(data.criador_id)
        if not usuario:
            error_(f"[ERRO] Usuário com ID {data.criador_id} não encontrado para vincular à família")
            raise ValueError("Usuário criador não encontrado")

        id = await familia_repository.insert_familia(data)
        await usuario_repository.adicionar_usuario_em_familia(data.criador_id, id)
        info_(f"[SUCESSO] Família criada com ID {id} e vinculada ao usuário {data.criador_id}")
        return FamiliaDB.from_mongo({**data.dict(), "_id": id})
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {str(e)}")
        raise ValueError("ID de usuario inválido")
    except Exception as e:
        error_(f"[ERRO] Falha ao criar família: {str(e)}")
        raise

async def listar_familias() -> list[FamiliaDB]:
    try:
        docs = await familia_repository.get_all_familias()
        info_(f"[SUCESSO] Listagem de {len(docs)} família(s)")
        return [FamiliaDB.from_mongo(doc) for doc in docs]
    except Exception as e:
        error_(f"[ERRO] Falha ao listar famílias: {str(e)}")
        raise

async def buscar_por_id(familia_id: str) -> Optional[FamiliaDB]:
    try:
        doc = await familia_repository.get_familia_by_id(familia_id)
        if doc:
            info_(f"[SUCESSO] Família encontrada com ID {familia_id}")
            return FamiliaDB.from_mongo(doc)
        error_(f"[ERRO] Família com ID {familia_id} não encontrada")
        return None
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {str(e)}")
        raise ValueError("ID de família inválido")
    except Exception as e:
        error_(f"[ERRO] Falha ao buscar família {familia_id}: {str(e)}")
        raise

async def atualizar_familia(familia_id: str, data: FamiliaUpdate) -> bool:
    try:
        existente = await familia_repository.get_familia_by_id(familia_id)
        if not existente:
            error_(f"[ERRO] Família com ID {familia_id} não encontrada para atualizar")
            raise ValueError("Família não encontrada")
        
        sucesso = await familia_repository.update_familia(familia_id, data)
        if sucesso:
            info_(f"[SUCESSO] Família atualizada com ID {familia_id}")
        else:
            error_(f"[ERRO] Família com ID {familia_id} não encontrada para atualizar")
        return sucesso
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {str(e)}")
        raise ValueError("ID de família inválido")
    except Exception as e:
        error_(f"[ERRO] Falha ao atualizar família {familia_id}: {str(e)}")
        raise

async def deletar_familia(familia_id: str) -> bool:
    try:
        sucesso = await familia_repository.delete_familia(familia_id)
        if sucesso:
            info_(f"[SUCESSO] Família deletada com ID {familia_id}")
        else:
            error_(f"[ERRO] Família com ID {familia_id} não encontrada para exclusão")
        
        usuarios_na_familia = await usuario_repository.get_usuarios_by_familia_id(familia_id)
        for usuario in usuarios_na_familia:
            await usuario_repository.remover_usuario_da_familia(str(usuario["_id"]))
        return sucesso
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {str(e)}")
        raise ValueError("ID de família inválido")
    except Exception as e:
        error_(f"[ERRO] Falha ao deletar família {familia_id}: {str(e)}")
        raise

async def buscar_familias(
    nome: Optional[str],
    descricao: Optional[str],
    is_public: Optional[bool],
    dia: Optional[int],
    mes: Optional[int],
    ano: Optional[int],
    page: int,
    size: int,
    order_by: str = "nome",
    order_dir: str = "asc"
):
    try:
        resultado = await familia_repository.buscar_familias(
            nome, descricao, is_public, dia, mes, ano, page, size, order_by, order_dir
        )
        info_(f"[SUCESSO] Filtro de famílias retornou {len(resultado['content'])} item(ns)")
        return resultado
    except Exception as e:
        error_(f"[ERRO] Falha ao filtrar famílias: {str(e)}")
        raise

async def exibir_quantidade():
    try:
        quantidade = len(await listar_familias())
        info_(f"[SUCESSO] Quantidade de famílias cadastradas: {quantidade}")
        return quantidade
    except Exception as e:
        error_(f"[ERRO] Falha ao exibir quantidade de famílias: {str(e)}")
        raise

async def exibir_membros_familia(familia_id: str):
    try:
        membros = await usuario_repository.get_usuarios_by_familia_id(familia_id)
        info_(f"[SUCESSO] Listagem de membros da família com ID {familia_id}")
        return membros
    except InvalidId as e:
        error_(f"[ERRO] ID inválido: {str(e)}")
        raise ValueError("ID de família inválido")
    except Exception as e:
        error_(f"[ERRO] Falha ao exibir membros da família {familia_id}: {str(e)}")
        raise