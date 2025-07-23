from bson import ObjectId
from bson.errors import InvalidId
from db.database import avaliacao_collection
from models.avaliacao import AvaliacaoCreate, AvaliacaoUpdate
from utils.helper import convert_date_to_datetime, parse_mongo_id
from typing import Optional
from pymongo import ASCENDING, DESCENDING

async def insert_avaliacao(data: AvaliacaoCreate) -> str:
    if not ObjectId.is_valid(data.usuario_id):
        raise InvalidId("ID de usuário inválido")
    if not ObjectId.is_valid(data.item_id):
        raise InvalidId("ID de item (jogo/DLC) inválido")

    doc = data.dict()
    doc["data_avaliacao"] = convert_date_to_datetime(doc["data_avaliacao"])
    result = await avaliacao_collection.insert_one(doc)
    return str(result.inserted_id)

async def get_all_avaliacoes() -> list[dict]:
    docs = await avaliacao_collection.find().to_list(100)
    return [parse_mongo_id(doc) for doc in docs]

async def get_avaliacao_by_id(avaliacao_id: str) -> dict | None:
    if not ObjectId.is_valid(avaliacao_id):
        raise InvalidId("ID de avaliação inválido")

    doc = await avaliacao_collection.find_one({"_id": ObjectId(avaliacao_id)})
    return parse_mongo_id(doc) if doc else None

async def update_avaliacao(avaliacao_id: str, data: AvaliacaoUpdate) -> bool:
    if not ObjectId.is_valid(avaliacao_id):
        raise InvalidId("ID de avaliação inválido")
    
    update_data = {k: v for k, v in data.dict(exclude_unset=True).items()}
    if "data_avaliacao" in update_data:
        update_data["data_avaliacao"] = convert_date_to_datetime(update_data["data_avaliacao"])
    
    result = await avaliacao_collection.update_one(
        {"_id": ObjectId(avaliacao_id)}, {"$set": update_data}
    )
    return result.modified_count > 0
  
async def get_avaliacao_by_usuario_and_item(usuario_id: str, item_id: str) -> dict | None:
  if not ObjectId.is_valid(usuario_id):
      raise InvalidId("ID de usuário inválido")
  if not ObjectId.is_valid(item_id):
      raise InvalidId("ID de item inválido")
  
  doc = await avaliacao_collection.find_one({"usuario_id": usuario_id,"item_id": item_id})
  return parse_mongo_id(doc) if doc else None

async def delete_avaliacao(avaliacao_id: str) -> bool:
    if not ObjectId.is_valid(avaliacao_id):
        raise InvalidId("ID de avaliação inválido")

    result = await avaliacao_collection.delete_one({"_id": ObjectId(avaliacao_id)})
    return result.deleted_count > 0

async def buscar_avaliacoes(
    usuario_id: Optional[str],
    item_id: Optional[str],
    nota_min: Optional[int],
    nota_max: Optional[int],
    comentario: Optional[str],
    dia: Optional[int],
    mes: Optional[int],
    ano: Optional[int],
    page: int,
    size: int,
    order_by: str = "data_avaliacao",
    order_dir: str = "desc"
) -> dict:
    filtro = {}

    if usuario_id and ObjectId.is_valid(usuario_id):
        filtro["usuario_id"] = usuario_id
    if item_id and ObjectId.is_valid(item_id):
        filtro["item_id"] = item_id
    if comentario:
        filtro["comentario"] = {"$regex": comentario, "$options": "i"}
    if nota_min is not None or nota_max is not None:
        filtro["nota"] = {}
        if nota_min is not None:
            filtro["nota"]["$gte"] = nota_min
        if nota_max is not None:
            filtro["nota"]["$lte"] = nota_max
    if dia or mes or ano:
        filtro["$expr"] = {
            "$and": [
                {"$eq": [{"$dayOfMonth": "$data_avaliacao"}, dia]} if dia else {},
                {"$eq": [{"$month": "$data_avaliacao"}, mes]} if mes else {},
                {"$eq": [{"$year": "$data_avaliacao"}, ano]} if ano else {},
            ]
        }

    total = await avaliacao_collection.count_documents(filtro)
    ordenacao = ASCENDING if order_dir == "asc" else DESCENDING

    cursor = (
        avaliacao_collection.find(filtro)
        .sort(order_by, ordenacao)
        .skip((page - 1) * size)
        .limit(size)
    )

    documentos = [parse_mongo_id(doc) for doc in await cursor.to_list(length=size)]

    return {
        "size": size,
        "page": page,
        "totalElements": total,
        "totalPages": (total + size - 1) // size,
        "content": documentos
    }