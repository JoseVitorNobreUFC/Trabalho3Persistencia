import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils.id_factory import get_game_id, generate_id, create_id, get_dlc_id

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "jogosdb"

dlcs_nomes = [
    "Farewell",
    "The Old Man and the Sea",
    "Dual Sword DLC",
    "Wario DLC",
    "Chris DLC",
    "Godmaster",
    "Expansion Pack",
    "Valhalla DLC",
    "Directors Cut DLC",
    "Pantheom of Bosses",
    "Secret Island",
    "Iron and Blood DLC",
    "The Last Stand DLC",
    "Gaster DLC",
    "Chapter 8",
    "Crow DLC",
    "Definitive Edition",
    "Bill DLC",
    "Bee Update",
    "The final Update",
    "1.6 Update",
    "Extra Content Pack 1",
    "Extra Content Pack 2",
    "Extra Content Pack 3",
    "Extra Content Pack 4",
    "Extra Content Pack 5",
    "Extra Content Pack 6",
    "Extra Content Pack 7",
    "Extra Content Pack 8",
    "Extra Content Pack 9",
]

async def popular():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["dlcs"]

    dlcs = []
    for i in range(1, 31):
        dlcs.append({
            "_id": create_id(get_dlc_id(i-1)),
            "titulo": f"{dlcs_nomes[i-1]}",
            "descricao": f"Descrição da DLC {i}",
            "data_lancamento": datetime(2024, 1, 1) + timedelta(days=i),
            "preco": int(round((random.randint(10, 100) + i * 1.5) * 100)),
            "jogo_id": f"{get_game_id(i-1)}"
        })

    result = await collection.insert_many(dlcs)
    print(f"{len(result.inserted_ids)} dlcs inseridas.")

if __name__ == "__main__":
    asyncio.run(popular())