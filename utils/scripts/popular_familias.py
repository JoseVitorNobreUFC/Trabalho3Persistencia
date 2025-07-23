import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import random
import sys
import os
from bson import ObjectId
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils.id_factory import generate_id, get_user_id, get_family_id, create_id

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "jogosdb"

familia_nomes = [
    "CSGO Team",
    "Indie Lovers",
    "Triple A Force",
    "The Last Stand",
    "Nintendo Haters",
    "Single Player Enjoyers",
    "Multiplayer Lovers",
    "Horror Lovers"
]

descricoes = [
    "Somos ruins",
    "Amamos jogos a baixo de 40 reais",
    "Odiamos jogos a baixo de 40 reais",
    "",
    "Nintendo tem que piratear mesmo",
    "Pra que jogar online",
    "Se for pra ver historia eu vejo um livro ou filme",
    "Hideo Kojima é um genio"
]

async def popular():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection_familia = db["familias"]
    collection_usuario = db["usuarios"]
    
    familias = []
    for i in range(1, 9):
        familias.append({
            "_id": create_id(get_family_id(i-1)),
            "nome": f"{familia_nomes[i-1]}",
            "descricao": f"{descricoes[i-1]}",
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