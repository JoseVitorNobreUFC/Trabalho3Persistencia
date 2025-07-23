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
    
    usuario_collection = db["usuarios"]
    await usuario_collection.delete_many({})
    
    familia_collection = db["familias"]
    await familia_collection.delete_many({})
    
    compra_collection = db["compras"]
    await compra_collection.delete_many({})
    
    print("Banco de dados limpo com sucesso!")
  
if __name__ == "__main__":
    asyncio.run(limpar_banco())