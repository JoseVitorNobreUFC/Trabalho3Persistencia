from models.usuario import UsuarioDB, UsuarioCreate, UsuarioUpdate
from repository import usuario_repository
from utils.logger import info_, error_
from bson.errors import InvalidId
from typing import Optional

async def criar_usuario(usuario: UsuarioCreate) -> UsuarioDB:
  try:
    if await usuario_repository.get_usuario_by_email(usuario.email):
      error_(f"Usuário com email {usuario.email} ja cadastrado")
      raise ValueError(f"Usuário com email {usuario.email} ja cadastrado")
    
    id = await usuario_repository.insert_usuario(usuario)
    info_(f"Usuário criado com ID {id}")
    return UsuarioDB.from_mongo({**usuario.dict(), "_id":id})
  except InvalidId as e:
    error_(f"ID {str(e)} é inválido")
    raise ValueError("ID de usuário inválndo")
  except Exception as e:
    error_(f"Erro ao criar usuário: {e}")
    raise
  
async def listar_usuarios() -> list[UsuarioDB]:
  try:
    docs = await usuario_repository.get_all_usuarios()
    info_(f"Listagem de {len(docs)} usuário(s)")
    return [UsuarioDB.from_mongo(doc) for doc in docs]
  except Exception as e:
    error_(f"Erro ao listar usuários: {e}")
    raise

async def buscar_por_id(usuario_id: str) -> Optional[UsuarioDB]:
  try:
    doc = await usuario_repository.get_usuario_by_id(usuario_id)
    if doc:
      info_(f"Usuário encontrado com ID {usuario_id}")
      return UsuarioDB.from_mongo(doc)
    error_(f"Usuário com ID {usuario_id} nao encontrado")
    return None
  except InvalidId as e:
    error_(f"ID {str(e)} é inválido")
    raise ValueError("ID de usuário inválndo")
  except Exception as e:
    error_(f"Erro ao buscar usuário {usuario_id}: {e}")
    raise
  
async def atualizar_usuario(usuario_id: str, data: UsuarioUpdate) -> bool:
  try:
    usuario_existente = await usuario_repository.get_usuario_by_id(usuario_id)
    if not usuario_existente:
      error_(f"Usuário com ID {usuario_id} nao encontrado")
      raise ValueError("Jogo nao encontrado.")
    
    if data.email and await usuario_repository.get_usuario_by_email(data.email):
      error_(f"Usuário com email {data.email} ja cadastrado")
      raise ValueError(f"Jogo {data.email} ja cadastrado")
    
    sucesso = await usuario_repository.update_usuario(usuario_id, data)
    if sucesso:
      info_(f"Usuário atualizado com ID {usuario_id}")
    else:
      error_(f"Usuário com ID {usuario_id} nao encontrado")
    return sucesso
  except InvalidId as e:
    error_(f"ID {str(e)} é inválido")
    raise ValueError("ID de usuário inválndo")
  except Exception as e:
    error_(f"Erro ao atualizar usuário {usuario_id}: {e}")
    raise
  
async def deletar_usuario(usuario_id: str) -> bool: # Futuramente adicionar checagem para familia se for o dono dela
  try:
    sucesso = await usuario_repository.delete_usuario(usuario_id)
    if sucesso:
      info_(f"Usuário deletado com ID {usuario_id}")
    else:
      error_(f"Usuário com ID {usuario_id} nao encontrado")
    return sucesso
  except InvalidId as e:
    error_(f"ID {str(e)} é inválido")
    raise ValueError("ID de usuário inválndo")
  except Exception as e:
    error_(f"Erro ao deletar usuário {usuario_id}: {e}")
    raise
  
async def buscar_usuarios(
    nome: Optional[str],
    dia: Optional[int],
    mes: Optional[int],
    ano: Optional[int],
    email: Optional[str],
    pais: Optional[str],
    page: int,
    size: int,
    order_by: str = "nome",
    order_dir: str = "asc"
):
  try:
    resultado = await usuario_repository.buscar_usuarios(
        nome, mes, dia, ano, email, pais, page, size, order_by, order_dir
    )
    info_(f"[SUCESSO] Filtro de usuários retornou {len(resultado['content'])} item(ns)")
    return resultado
  except Exception as e:
    error_(f"[ERRO] Falha ao filtrar usuários: {str(e)}")
    raise
  
async def exibir_quantidade():
  try:
    quantidade = len(await listar_usuarios())
    info_(f"[SUCESSO] Quantidade de usuários cadastrados: {quantidade}")
    return quantidade
  except Exception as e:
    error_(f"[ERRO] Falha ao exibir quantidade de usuários: {str(e)}")
    raise