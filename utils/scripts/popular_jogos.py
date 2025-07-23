import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils.id_factory import get_game_id, create_id

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "jogosdb"

jogos_titulo = [
    "Celeste",
    "Dark Souls",
    "The Legend of Zelda",
    "Super Mario",
    "Resident Evil",
    "Hollow Knight",
    "Braid",
    "God of War",
    "Horizonton Zero Dawn",
    "Nine Sols",
    "Tunic",
    "The Witcher",
    "The Last of Us",
    "The Legend of Zelda: Breath of the Wild",
    "Undertale",
    "Deltarune",
    "Ori and the Will of the Wisps",
    "Ori and the Blind Forest",
    "Left 4 Dead 2",
    "Minecraft",
    "Terraria",
    "Stardew Valley",
    "The Binding of Isaac",
    "Enter the Gungeon",
    "Devil May Cry",
    "Dark Souls II",
    "Sekiro",
    "Expedition 33",
    "Dark Souls III",
    "Borderlands 3"
]

desenvolvedores_nomes = [
    "FromSoftware",
    "Nintendo",
    "Team Cherry",
    "Capcom",
    "Ubisoft",
    "Sony",
    "Square Enix",
    "Bandai Namco",
    "Microsoft",
    "Rockstar Games"
]
async def popular():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["jogos"]

    jogos = []
    for i in range(1, 31):
        jogos.append({
            "_id": create_id(get_game_id(i-1)),
            "titulo": f"{jogos_titulo[i-1]}",
            "descricao": f"Descrição do Jogo {i}",
            "data_lancamento": datetime(2024, 1, 1) + timedelta(days=i),
            "preco": int(round((random.randint(10, 100) + i * 1.5) * 100)),
            "desenvolvedora": f"{desenvolvedores_nomes[random.randint(0, 9)]}"
        })

    result = await collection.insert_many(jogos)
    print(f"{len(result.inserted_ids)} jogos inseridos.")

if __name__ == "__main__":
    asyncio.run(popular())