from models.jogo import JogoCreate, JogoDB, JogoUpdate
from db.jogo import jogo_collection
from bson import ObjectId
from utils.logger import info_, error_

async def criar_jogo(jogo: JogoCreate) -> JogoDB:
    try:
        novo = await jogo_collection.insert_one(jogo.dict())
        info_(f"[SUCESSO] Jogo criado com ID {str(novo.inserted_id)}")
        return JogoDB(**jogo.dict(), id=str(novo.inserted_id))
    except Exception as e:
        error_(f"[ERRO] Falha ao criar jogo: {str(e)}")
        raise

async def listar_jogos() -> list[JogoDB]:
    try:
        jogos = await jogo_collection.find().to_list(length=100)
        info_(f"[SUCESSO] Listagem de {len(jogos)} jogo(s) realizada")
        return [JogoDB(**j) for j in jogos]
    except Exception as e:
        error_(f"[ERRO] Falha ao listar jogos: {str(e)}")
        raise

async def buscar_por_id(jogo_id: str) -> JogoDB | None:
    try:
        doc = await jogo_collection.find_one({"_id": ObjectId(jogo_id)})
        if doc:
            info_(f"[SUCESSO] Jogo encontrado com ID {jogo_id}")
            return JogoDB(**doc)
        else:
            error_(f"[ERRO] Jogo com ID {jogo_id} não encontrado")
            return None
    except Exception as e:
        error_(f"[ERRO] Erro ao buscar jogo por ID {jogo_id}: {str(e)}")
        raise

async def atualizar_jogo(jogo_id: str, dados: JogoUpdate) -> bool:
    try:
        result = await jogo_collection.update_one(
            {"_id": ObjectId(jogo_id)},
            {"$set": {k: v for k, v in dados.dict(exclude_unset=True).items()}}
        )
        if result.matched_count:
            info_(f"[SUCESSO] Jogo atualizado com ID {jogo_id}")
            return True
        else:
            error_(f"[ERRO] Jogo com ID {jogo_id} não encontrado para atualização")
            return False
    except Exception as e:
        error_(f"[ERRO] Falha ao atualizar jogo {jogo_id}: {str(e)}")
        raise

async def deletar_jogo(jogo_id: str) -> bool:
    try:
        result = await jogo_collection.delete_one({"_id": ObjectId(jogo_id)})
        if result.deleted_count:
            info_(f"[SUCESSO] Jogo deletado com ID {jogo_id}")
            return True
        else:
            error_(f"[ERRO] Jogo com ID {jogo_id} não encontrado para exclusão")
            return False
    except Exception as e:
        error_(f"[ERRO] Falha ao deletar jogo {jogo_id}: {str(e)}")
        raise
