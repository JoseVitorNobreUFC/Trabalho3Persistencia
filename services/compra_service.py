from bson import ObjectId
from bson.errors import InvalidId
from db.database import compra_collection
from models.compra import CompraCreate, CompraUpdate
from utils.helper import convert_date_to_datetime, parse_mongo_id
from typing import Optional
from pymongo import ASCENDING, DESCENDING

async def insert_compra(data: CompraCreate) -> str:
    if not ObjectId.is_valid(data.usuario_id):
        raise InvalidId("ID de usuário inválido")
    if not ObjectId.is_valid(data.item_id):
        raise InvalidId("ID de jogo/DLC inválido")
    
    doc = data.dict()
    doc["data_compra"] = convert_date_to_datetime(doc["data_compra"])
    result = await compra_collection.insert_one(doc)
    return str(result.inserted_id)

async def get_all_compras() -> list[dict]:
    docs = await compra_collection.find().to_list(100)
    return [parse_mongo_id(doc) for doc in docs]

async def get_compra_by_id(compra_id: str) -> dict | None:
    if not ObjectId.is_valid(compra_id):
        raise InvalidId("ID de compra inválido")

    doc = await compra_collection.find_one({"_id": ObjectId(compra_id)})
    return parse_mongo_id(doc) if doc else None

async def update_compra(compra_id: str, data: CompraUpdate) -> bool:
    if not ObjectId.is_valid(compra_id):
        raise InvalidId("ID de compra inválido")

    update_data = {k: v for k, v in data.dict(exclude_unset=True).items()}
    if "data_compra" in update_data:
        update_data["data_compra"] = convert_date_to_datetime(update_data["data_compra"])

    result = await compra_collection.update_one(
        {"_id": ObjectId(compra_id)}, {"$set": update_data}
    )
    return result.modified_count > 0

async def delete_compra(compra_id: str) -> bool:
    if not ObjectId.is_valid(compra_id):
        raise InvalidId("ID de compra inválido")

    result = await compra_collection.delete_one({"_id": ObjectId(compra_id)})
    return result.deleted_count > 0

async def buscar_compras(
    forma_pagamento: Optional[str],
    dia: Optional[int],
    mes: Optional[int],
    ano: Optional[int],
    preco_min: Optional[float],
    preco_max: Optional[float],
    page: int,
    size: int,
    order_by: str = "data_compra",
    order_dir: str = "asc"
) -> dict:
    filtro = {}

    if forma_pagamento:
        filtro["forma_pagamento"] = forma_pagamento

    if dia or mes or ano:
        filtro["$expr"] = {
            "$and": [
                {"$eq": [{"$dayOfMonth": "$data_compra"}, dia]} if dia else {},
                {"$eq": [{"$month": "$data_compra"}, mes]} if mes else {},
                {"$eq": [{"$year": "$data_compra"}, ano]} if ano else {},
            ]
        }

    if preco_min is not None or preco_max is not None:
        filtro["preco_pago"] = {}
        if preco_min is not None:
            filtro["preco_pago"]["$gte"] = int(preco_min * 100)
        if preco_max is not None:
            filtro["preco_pago"]["$lte"] = int(preco_max * 100)

    total = await compra_collection.count_documents(filtro)
    ordenacao = ASCENDING if order_dir.lower() == "asc" else DESCENDING

    cursor = (
        compra_collection
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