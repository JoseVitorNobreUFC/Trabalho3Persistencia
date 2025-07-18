import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import random

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "jogosdb"

async def popular():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["dlcs"]

    dlcs = []
    for i in range(1, 31):
        dlcs.append({
            "_id": i,
            "titulo": f"DLC {i}",
            "descricao": f"Descrição do Jogo {i}",
            "data_lancamento": datetime(2024, 1, 1) + timedelta(days=i),
            "preco": int(round((random.randint(10, 100) + i * 1.5) * 100)),  # ← aqui!
            "jogo_id": f"{i}"
        })

    result = await collection.insert_many(dlcs)
    print(f"{len(result.inserted_ids)} dlcs inseridos.")

if __name__ == "__main__":
    asyncio.run(popular())
