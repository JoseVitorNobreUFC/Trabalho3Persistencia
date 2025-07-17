from db.database import jogo_collection
from bson import ObjectId
from models.jogo import JogoCreate, JogoUpdate
from utils.helper import convert_date_to_datetime
from typing import Optional
from pymongo import ASCENDING, DESCENDING

# Função para converter _id de ObjectId para str
def parse_mongo_id(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc

async def insert_jogo(jogo: JogoCreate) -> str:
    data = jogo.dict()
    data["data_lancamento"] = convert_date_to_datetime(data["data_lancamento"])
    result = await jogo_collection.insert_one(data)
    return str(result.inserted_id)

async def get_all_jogos() -> list[dict]:
    jogos = await jogo_collection.find().to_list(length=100)
    return [parse_mongo_id(j) for j in jogos]

async def get_jogo_by_id(jogo_id: str) -> dict | None:
    doc = await jogo_collection.find_one({"_id": ObjectId(jogo_id)})
    return parse_mongo_id(doc) if doc else None

async def update_jogo(jogo_id: str, dados: JogoUpdate) -> bool:
    update_data = {k: v for k, v in dados.dict(exclude_unset=True).items()}
    if "data_lancamento" in update_data:
        update_data["data_lancamento"] = convert_date_to_datetime(update_data["data_lancamento"])
    result = await jogo_collection.update_one({"_id": ObjectId(jogo_id)}, {"$set": update_data})
    return result.matched_count > 0

async def delete_jogo(jogo_id: str) -> bool:
    result = await jogo_collection.delete_one({"_id": ObjectId(jogo_id)})
    return result.deleted_count > 0

async def buscar_jogos(
    titulo: Optional[str],
    descricao: Optional[str],
    desenvolvedora: Optional[str],
    dia: Optional[int],
    mes: Optional[int],
    ano: Optional[int],
    preco_min: Optional[float],
    preco_max: Optional[float],
    page: int,
    size: int,
    order_by: str = "titulo",
    order_dir: str = "asc"
) -> dict:
    filtro = {}

    if titulo:
        filtro["titulo"] = {"$regex": titulo, "$options": "i"}
    if descricao:
        filtro["descricao"] = {"$regex": descricao, "$options": "i"}
    if desenvolvedora:
        filtro["desenvolvedora"] = {"$regex": desenvolvedora, "$options": "i"}

    # Filtro de data
    if dia or mes or ano:
        filtro["$expr"] = {
            "$and": [
                {"$eq": [{"$dayOfMonth": "$data_lancamento"}, dia]} if dia else {},
                {"$eq": [{"$month": "$data_lancamento"}, mes]} if mes else {},
                {"$eq": [{"$year": "$data_lancamento"}, ano]} if ano else {},
            ]
        }

    # Filtro de preço
    if preco_min or preco_max:
        filtro["preco"] = {}
        if preco_min is not None:
            filtro["preco"]["$gte"] = preco_min
        if preco_max is not None:
            filtro["preco"]["$lte"] = preco_max

    total = await jogo_collection.count_documents(filtro)

    ordenacao = ASCENDING if order_dir.lower() == "asc" else DESCENDING

    cursor = (
        jogo_collection
        .find(filtro)
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