import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils.helper import get_game_id, generate_id, create_id

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "jogosdb"

async def popular():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["dlcs"]

    dlcs = []
    for i in range(1, 31):
        dlcs.append({
            "_id": generate_id(),
            "titulo": f"DLC {i}",
            "descricao": f"Descrição da DLC {i}",
            "data_lancamento": datetime(2024, 1, 1) + timedelta(days=i),
            "preco": int(round((random.randint(10, 100) + i * 1.5) * 100)),
            "jogo_id": f"{get_game_id(i-1)}"
        })

    result = await collection.insert_many(dlcs)
    print(f"{len(result.inserted_ids)} dlcs inseridas.")

if __name__ == "__main__":
    asyncio.run(popular())
