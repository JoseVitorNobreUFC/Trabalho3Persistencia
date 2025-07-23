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

comentario = [
    "Esse jogo é muito bom",
    "Achei mais divertido do que eu esperava",
    "Recomendo",
    "Achei mais ou menos",
    "Nao recomendo",
    "Nao gostei",
    "Um dos jogos já feitos",
    "Essa DLC não vale esse preço"
]

async def popular():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection_compra = db["compras"]
    collection_avaliacao = db["avaliacoes"]

    compras = []
    avaliacoes = []
    for i in range(0, 30):
      for j in range(0, 3):
        item_id = get_game_id(random.randint(0, 29))
        compras.append({
            "_id": generate_id(),
            "usuario_id": f"{get_user_id(i)}",
            "item_id": f"{item_id}",
            "data_compra": datetime(2024, 1, 1) + timedelta(days=i),
            "preco_pago": int(round((random.randint(5, 30) + i * 1.5) * 100)),
            "forma_pagamento": formas_de_pagamento[random.randint(0, 2)]
        })
        avaliacoes.append({
            "_id": generate_id(),
            "usuario_id": f"{get_user_id(i)}",
            "item_id": f"{item_id}",
            "nota": random.randint(1, 10),
            "data_avaliacao": datetime(2024, 1, 1) + timedelta(days=i),
            "comentario": f"{comentario[random.randint(0, 7)]}"
        })
      for j in range(0, 3):
        item_id = get_dlc_id(random.randint(0, 29))
        compras.append({
            "_id": generate_id(),
            "usuario_id": f"{get_user_id(i)}",
            "item_id": f"{item_id}",
            "data_compra": datetime(2024, 1, 1) + timedelta(days=i),
            "preco_pago": int(round((random.randint(5, 30) + i * 1.5) * 100)),
            "forma_pagamento": formas_de_pagamento[random.randint(0, 2)]
        })
        avaliacoes.append({
            "_id": generate_id(),
            "usuario_id": f"{get_user_id(i)}",
            "item_id": f"{item_id}",
            "data_avaliacao": datetime(2024, 1, 1) + timedelta(days=i),
            "nota": random.randint(1, 10),
            "comentario": f"{comentario[random.randint(0, 7)]}"
        })

    result = await collection_compra.insert_many(compras)
    print(f"{len(result.inserted_ids)} compras inseridas.")

    result = await collection_avaliacao.insert_many(avaliacoes)
    print(f"{len(result.inserted_ids)} avaliacoes inseridas.")

if __name__ == "__main__":
    asyncio.run(popular())
