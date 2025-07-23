from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "jogosdb")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

jogo_collection = db["jogos"]
dlc_collection = db["dlcs"]
usuario_collection = db["usuarios"]
familia_collection = db["familias"]
compra_collection = db["compras"]
avaliacao_collection = db["avaliacoes"]