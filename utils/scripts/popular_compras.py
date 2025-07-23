import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils.id_factory import get_game_id, generate_id, create_id, get_dlc_id, get_user_id
from models.compra import FormaPagamento

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "jogosdb"

formas_de_pagamento: list[FormaPagamento] = [FormaPagamento.CARTAO, FormaPagamento.BOLETO, FormaPagamento.PIX]

async def popular():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["compras"]

    compras = []
    for i in range(0, 30):
      for j in range(0, 3):
        compras.append({
            "_id": generate_id(),
            "usuario_id": f"{get_user_id(i)}",
            "item_id": f"{get_game_id(random.randint(0, 29))}",
            "data_compra": datetime(2024, 1, 1) + timedelta(days=i),
            "preco_pago": int(round((random.randint(5, 30) + i * 1.5) * 100)),
            "forma_pagamento": formas_de_pagamento[random.randint(0, 2)]
        })
      for j in range(0, 3):
        compras.append({
            "_id": generate_id(),
            "usuario_id": f"{get_user_id(i)}",
            "item_id": f"{get_dlc_id(random.randint(0, 29))}",
            "data_compra": datetime(2024, 1, 1) + timedelta(days=i),
            "preco_pago": int(round((random.randint(5, 30) + i * 1.5) * 100)),
            "forma_pagamento": formas_de_pagamento[random.randint(0, 2)]
        })

    result = await collection.insert_many(compras)
    print(f"{len(result.inserted_ids)} compras inseridas.")

if __name__ == "__main__":
    asyncio.run(popular())
