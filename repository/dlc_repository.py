from bson import ObjectId
from bson.errors import InvalidId
from db.database import dlc_collection
from models.dlc import DLCCreate, DLCUpdate
from utils.helper import convert_date_to_datetime
from typing import Optional
from pymongo import ASCENDING, DESCENDING

def parse_mongo_id(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc

async def insert_dlc(data: DLCCreate) -> str:
    if not ObjectId.is_valid(data.jogo_id):
        raise InvalidId(f"{data.jogo_id}")
    
    doc = data.dict()
    doc["data_lancamento"] = convert_date_to_datetime(doc["data_lancamento"])
    result = await dlc_collection.insert_one(doc)
    return str(result.inserted_id)

async def get_all_dlcs() -> list[dict]:
    docs = await dlc_collection.find().to_list(100)
    return [parse_mongo_id(doc) for doc in docs]

async def get_dlc_by_id(dlc_id: str) -> dict | None:
    if not ObjectId.is_valid(dlc_id):
        raise InvalidId("ID de DLC inválido")
    
    doc = await dlc_collection.find_one({"_id": ObjectId(dlc_id)})
    return parse_mongo_id(doc) if doc else None

async def update_dlc(dlc_id: str, data: DLCUpdate) -> bool:
    if not ObjectId.is_valid(dlc_id):
        raise InvalidId("ID de DLC inválido")
    
    update_data = {k: v for k, v in data.dict(exclude_unset=True).items()}
    if "data_lancamento" in update_data:
        update_data["data_lancamento"] = convert_date_to_datetime(update_data["data_lancamento"])
    result = await dlc_collection.update_one(
        {"_id": ObjectId(dlc_id)}, {"$set": update_data}
    )
    return result.modified_count > 0

async def get_dlc_by_jogo(jogo_id: str) -> dict | None:
    if not ObjectId.is_valid(jogo_id):
        raise InvalidId("ID de jogo inválido")

    doc = await dlc_collection.find_one({"jogo_id": jogo_id})
    return parse_mongo_id(doc) if doc else None

async def delete_dlc(dlc_id: str) -> bool:
    if not ObjectId.is_valid(dlc_id):
        raise InvalidId("ID de DLC inválido")
    
    result = await dlc_collection.delete_one({"_id": ObjectId(dlc_id)})
    return result.deleted_count > 0

async def buscar_dlcs(
    titulo: Optional[str],
    descricao: Optional[str],
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

    # Filtro de data
    if dia or mes or ano:
        filtro["$expr"] = {
            "$and": [
                {"$eq": [{"$dayOfMonth": "$data_lancamento"}, dia]} if dia else {},
                {"$eq": [{"$month": "$data_lancamento"}, mes]} if mes else {},
                {"$eq": [{"$year": "$data_lancamento"}, ano]} if ano else {},
            ]
        }

    if preco_min is not None or preco_max is not None:
        filtro["preco"] = {}
        if preco_min is not None:
            filtro["preco"]["$gte"] = preco_min * 100
        if preco_max is not None:
            filtro["preco"]["$lte"] = preco_max * 100

    total = await dlc_collection.count_documents(filtro)

    ordenacao = ASCENDING if order_dir.lower() == "asc" else DESCENDING

    cursor = (
        dlc_collection
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