import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(_file_), "../..")))
from utils.id_factory import get_game_id, create_id

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "jogosdb"

async def popular():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["jogos"]

    jogos = []
    for i in range(1, 31):
        jogos.append({
            "_id": create_id(get_game_id(i-1)),
            "titulo": f"Jogo {i}",
            "descricao": f"Descrição do Jogo {i}",
            "data_lancamento": datetime(2024, 1, 1) + timedelta(days=i),
            "preco": int(round((random.randint(10, 100) + i * 1.5) * 100)),
            "desenvolvedora": f"Estúdio {i % 5 + 1}"
        })

    result = await collection.insert_many(jogos)
    print(f"{len(result.inserted_ids)} jogos inseridos.")

if __name__ == "__main__":
    asyncio.run(popular())