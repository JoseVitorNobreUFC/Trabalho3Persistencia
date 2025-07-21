from db.database import familia_collection
from models.familia import FamiliaCreate, FamiliaUpdate
from bson import ObjectId
from bson.errors import InvalidId
from utils.helper import convert_date_to_datetime, parse_mongo_id
from typing import Optional
from pymongo import ASCENDING, DESCENDING

async def insert_familia(data: FamiliaCreate) -> str:
    data = data.dict()
    data["data_criacao"] = convert_date_to_datetime(data["data_criacao"])
    result = await familia_collection.insert_one(data)
    return str(result.inserted_id)

async def get_all_familias() -> list[dict]:
    docs = await familia_collection.find().to_list(100)
    return [parse_mongo_id(doc) for doc in docs]

async def get_familia_by_id(familia_id: str) -> dict | None:
    if not ObjectId.is_valid(familia_id):
        raise InvalidId("ID de família inválido")

    doc = await familia_collection.find_one({"_id": ObjectId(familia_id)})
    return parse_mongo_id(doc) if doc else None

async def update_familia(familia_id: str, data: FamiliaUpdate) -> bool:
    if not ObjectId.is_valid(familia_id):
        raise InvalidId("ID de família inválido")
    
    update_data = {k: v for k, v in data.dict(exclude_unset=True).items()}
    if "data_criacao" in update_data:
        update_data["data_criacao"] = convert_date_to_datetime(update_data["data_criacao"])
    
    result = await familia_collection.update_one({"_id": ObjectId(familia_id)}, {"$set": update_data})
    return result.matched_count > 0

async def delete_familia(familia_id: str) -> bool:
    if not ObjectId.is_valid(familia_id):
        raise InvalidId("ID de família inválido")
    
    result = await familia_collection.delete_one({"_id": ObjectId(familia_id)})
    return result.deleted_count > 0

async def get_familia_by_criador_id(creator_id: str) -> dict | None:
    if not ObjectId.is_valid(creator_id):
        raise InvalidId("ID de família inválido")
    
    doc = await familia_collection.find_one({"criador_id": creator_id})
    return parse_mongo_id(doc) if doc else None

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
) -> dict:
    filtro = {}
    
    if nome:
        filtro["nome"] = {"$regex": nome, "$options": "i"}
    if descricao:
        filtro["descricao"] = {"$regex": descricao, "$options": "i"}
    if is_public is not None:
        filtro["is_public"] = is_public

    if dia or mes or ano:
        filtro["$expr"] = {
            "$and": [
                {"$eq": [{"$dayOfMonth": "$data_criacao"}, dia]} if dia else {},
                {"$eq": [{"$month": "$data_criacao"}, mes]} if mes else {},
                {"$eq": [{"$year": "$data_criacao"}, ano]} if ano else {},
            ]
        }

    total = await familia_collection.count_documents(filtro)
    
    ordenacao = ASCENDING if order_dir.lower() == "asc" else DESCENDING
    
    cursor = (
        familia_collection
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
