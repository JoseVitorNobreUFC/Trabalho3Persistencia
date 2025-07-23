from db.database import avaliacao_collection, compra_collection, usuario_collection, jogo_collection, dlc_collection, familia_collection
from bson import ObjectId
from statistics import mean

async def obter_dados_item(item_id: str):
    item_obj_id = ObjectId(item_id)

    jogo = await jogo_collection.find_one({"_id": item_obj_id})
    if jogo:
        nome_jogo = jogo["titulo"]
    else:
        dlc = await dlc_collection.find_one({"_id": item_obj_id})
        if dlc:
            nome_jogo = dlc["titulo"]
        else:
            return {"erro": "Item não encontrado"}

    compras = await compra_collection.find({"item_id": item_id}).to_list(length=None)
    quantidade_usuarios = len(set(compra["usuario_id"] for compra in compras))

    avaliacoes = await avaliacao_collection.find({"item_id": item_id}).to_list(length=None)
    notas = [a["nota"] for a in avaliacoes]
    media_nota = round(sum(notas) / len(notas), 2) if notas else 0.0

    comentarios = []
    for a in avaliacoes:
        if a.get("comentario"):
            usuario = await usuario_collection.find_one({"_id": ObjectId(a["usuario_id"])})
            nome_usuario = usuario["nome"] if usuario else "Desconhecido"
            comentarios.append({
                "nome": nome_usuario,
                "nota": a["nota"],
                "comentario": a["comentario"]
            })

    return {
        "nome_jogo": nome_jogo,
        "quantidadeDeCompras": quantidade_usuarios,
        "media_nota": media_nota,
        "comentarios": comentarios
    }

async def obter_perfil_usuario(usuario_id: str):
    usuario_obj_id = ObjectId(usuario_id)

    # 1. Buscar usuário
    usuario = await usuario_collection.find_one({"_id": usuario_obj_id})
    if not usuario:
        raise ValueError("Usuário não encontrado")

    # 2. Buscar avaliações
    avaliacoes_raw = await avaliacao_collection.find({"usuario_id": usuario_id}).to_list(length=None)
    avaliacoes = []
    for a in avaliacoes_raw:
        item_id = a["item_id"]
        nome_item = None

        jogo = await jogo_collection.find_one({"_id": ObjectId(item_id)})
        if jogo:
            nome_item = jogo["titulo"]
        else:
            dlc = await dlc_collection.find_one({"_id": ObjectId(item_id)})
            if dlc:
                nome_item = dlc["titulo"]
            else:
                nome_item = "Desconhecido"

        avaliacoes.append({
            "id": str(a["_id"]),
            "nome_item": nome_item,
            "nota": a["nota"],
            "comentario": a.get("comentario", ""),
            "data_avaliacao": a["data_avaliacao"]
        })

    # 3. Buscar compras
    compras_raw = await compra_collection.find({"usuario_id": usuario_id}).to_list(length=None)
    compras = []
    total_economizado = 0.0

    for c in compras_raw:
        item_id = c["item_id"]
        preco_pago = c["preco_pago"] / 100  # convertido de centavos para float
        data_compra = c["data_compra"]

        nome_item = None
        preco_cheio = 0.0

        jogo = await jogo_collection.find_one({"_id": ObjectId(item_id)})
        if jogo:
            nome_item = jogo["titulo"]
            preco_cheio = jogo["preco"] / 100
        else:
            dlc = await dlc_collection.find_one({"_id": ObjectId(item_id)})
            if dlc:
                nome_item = dlc["titulo"]
                preco_cheio = dlc["preco"] / 100
            else:
                nome_item = "Desconhecido"
                preco_cheio = preco_pago  # evita erro na economia

        compras.append({
            "nome_item": nome_item,
            "preco_cheio": round(preco_cheio, 2),
            "preco_pago": round(preco_pago, 2),
            "data_compra": data_compra
        })

        total_economizado += preco_cheio - preco_pago

    return {
        "nome": usuario["nome"],
        "total_economizado": round(total_economizado, 2),
        "avaliacoes": avaliacoes,
        "compras": compras
    }

async def obter_dados_familias():
    familias = await familia_collection.find({}).to_list(length=None)
    resultado = []

    for familia in familias:
        familia_id = str(familia["_id"])
        nome_familia = familia["nome"]

        # Buscar usuários da família
        usuarios = await usuario_collection.find({"familia_id": familia_id}).to_list(length=None)
        quantidade_usuarios = len(usuarios)
        valor_total_familia = 0.0
        usuarios_info = []

        for usuario in usuarios:
            usuario_id = str(usuario["_id"])
            nome_usuario = usuario["nome"]
            compras_usuario = await compra_collection.find({"usuario_id": usuario_id}).to_list(length=None)

            total_gasto = 0.0
            jogos_comprados = []

            for compra in compras_usuario:
                preco_pago = compra["preco_pago"] / 100
                item_id = compra["item_id"]

                # Buscar nome do item
                nome_item = "Desconhecido"
                jogo = await jogo_collection.find_one({"_id": ObjectId(item_id)})
                if jogo:
                    nome_item = jogo["titulo"]
                else:
                    dlc = await dlc_collection.find_one({"_id": ObjectId(item_id)})
                    if dlc:
                        nome_item = dlc["titulo"]

                jogos_comprados.append({
                    "titulo": nome_item,
                    "preco_pago": round(preco_pago, 2)
                })

                total_gasto += preco_pago

            valor_total_familia += total_gasto

            usuarios_info.append({
                "nome": nome_usuario,
                "jogos_comprados": jogos_comprados,
                "total_gasto": round(total_gasto, 2)
            })

        resultado.append({
            "nome": nome_familia,
            "quantidade_usuarios": quantidade_usuarios,
            "valor_total_gasto": round(valor_total_familia, 2),
            "usuarios": usuarios_info
        })

    return resultado
