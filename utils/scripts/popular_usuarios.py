import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(_file_), "../..")))
from utils.id_factory import get_user_id, create_id

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "jogosdb"

usuarios_names = [
  "James",
  "John",
  "Robert",
  "Michael",
  "William",
  "David",
  "Richard",
  "Joseph",
  "Thomas",
  "Charles",
  "Christopher",
  "Daniel",
  "Matthew",
  "Anthony",
  "Donald",
  "Mark",
  "Paul",
  "Steven",
  "Andrew",
  "Kenneth",
  "Joshua",
  "Kevin",
  "Brian",
  "George",
  "Edward",
  "Ronald",
  "Timothy",
  "Jason",
  "Jeffrey",
  "Ryan"
]

paises_names = [
  "Austria",
  "Germany",
  "Hungary",
  "Ireland",
  "Lithuania",
  "Malta",
  "Netherlands",
  "Brazil",
  "Portugal",
  "Romania",
]

async def popular():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["usuarios"]

    usuarios = []
    for i in range(1, 31):
        usuarios.append({
            "_id": create_id(get_user_id(i-1)),
            "nome": f"{usuarios_names[i - 1]}",
            "email": f"{usuarios_names[i - 1].lower()}@email.com",
            "senha": f"{usuarios_names[i - 1]}123@",
            "data_cadastro": datetime(2024, 1, 1) + timedelta(days=i),
            "pais": paises_names[random.randint(0, 9)], 
            "familia_id": ""
        })

    result = await collection.insert_many(usuarios)
    print(f"{len(result.inserted_ids)} usuarios inseridos.")

if __name__ == "__main__":
    asyncio.run(popular())