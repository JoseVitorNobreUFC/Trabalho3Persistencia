import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import random
import sys
import os
from bson import ObjectId
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(_file_), "../..")))
from utils.id_factory import generate_id, get_user_id, get_family_id, create_id

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "jogosdb"

async def popular():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection_familia = db["familias"]
    collection_usuario = db["usuarios"]
    
    familias = []
    for i in range(1, 9):
        familias.append({
            "_id": create_id(get_family_id(i-1)),
            "nome": f"Familia {i}",
            "descricao": f"Descrição da Familia {i}",
            "data_criacao": datetime(2024, 1, 1) + timedelta(days=i),
            "is_public": False if i > 6 else True,
            "criador_id": f"{get_user_id(i-1)}"
        })
        await collection_usuario.update_one(
            {"_id": ObjectId(get_user_id(i-1))},
            {"$set": {"familia_id": get_family_id(i-1)}}
        )

    result = await collection_familia.insert_many(familias)
    print(f"{len(result.inserted_ids)} familias inseridas.")

if __name__ == "__main__":
    asyncio.run(popular())