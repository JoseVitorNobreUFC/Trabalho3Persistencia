import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "jogosdb"

async def limpar_banco():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    jogo_collection = db["jogos"]
    await jogo_collection.delete_many({})
    
    dlc_collection = db["dlcs"]
    await dlc_collection.delete_many({})
  
if __name__ == "__main__":
    asyncio.run(limpar_banco())
