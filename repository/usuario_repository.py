from db.database import usuario_collection
from models.usuario import UsuarioCreate, UsuarioUpdate
from bson import ObjectId
from bson.errors import InvalidId
from utils.helper import convert_date_to_datetime, parse_mongo_id
from typing import Optional
from pymongo import ASCENDING, DESCENDING

# Vamos ter que voltar aqui quando o CRUD de familia estiver pronto
async def insert_usuario(data: UsuarioCreate) -> str:
    data = data.dict()
    data["data_cadastro"] = convert_date_to_datetime(data["data_cadastro"])
    result = await usuario_collection.insert_one(data)
    return str(result.inserted_id)

async def get_all_usuarios() -> list[dict]:
    docs = await usuario_collection.find().to_list(100)
    return [parse_mongo_id(doc) for doc in docs]

async def get_usuario_by_id(usuario_id: str) -> dict | None:
    if not ObjectId.is_valid(usuario_id):
        raise InvalidId("ID de usuário inválido")

    doc = await usuario_collection.find_one({"_id": ObjectId(usuario_id)})
    return parse_mongo_id(doc) if doc else None

async def update_usuario(usuario_id: str, data: UsuarioUpdate) -> bool:
    if not ObjectId.is_valid(usuario_id):
        raise InvalidId("ID de usuário inválido")
    
    update_data = {k: v for k, v in data.dict(exclude_unset=True).items()}
    if "data_cadastro" in update_data:
        update_data["data_cadastro"] = convert_date_to_datetime(update_data["data_nascimento"])
    result = await usuario_collection.update_one({"_id": ObjectId(usuario_id)}, {"$set": update_data})
    return result.matched_count > 0

async def delete_usuario(usuario_id: str) -> bool:
    if not ObjectId.is_valid(usuario_id):
        raise InvalidId("ID de usuário inv-lndo")
    
    result = await usuario_collection.delete_one({"_id": ObjectId(usuario_id)})
    return result.deleted_count > 0

async def get_usuario_by_email(email: str) -> dict | None:
    doc = await usuario_collection.find_one({"email": email})
    return parse_mongo_id(doc) if doc else None

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
) -> dict:
    filtro = {}
    
    if nome:
        filtro["nome"] = {"$regex": nome, "$options": "i"}
    if email:
        filtro["email"] = {"$regex": email, "$options": "i"}
    if pais:
        filtro["pais"] = {"$regex": pais, "$options": "i"}

    # Filtro de data
    if dia or mes or ano:
        filtro["$expr"] = {
            "$and": [
                {"$eq": [{"$dayOfMonth": "$data_cadastro"}, dia]} if dia else {},
                {"$eq": [{"$month": "$data_cadastro"}, mes]} if mes else {},
                {"$eq": [{"$year": "$data_cadastro"}, ano]} if ano else {},
            ]
        }

    total = await usuario_collection.count_documents(filtro)
    
    ordenacao = ASCENDING if order_dir.lower() == "asc" else DESCENDING
    
    cursor = (
        usuario_collection
        .find(filtro)
        .sort(order_by, ordenacao)
        .skip((page - 1) * size)
        .limit(size)
    )
    
    documentos = [parse_mongo_id(doc) for doc in await cursor.to_list(length=size)]
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "orderBy": order_by,
        "orderDir": order_dir,
        "content": documentos
    }