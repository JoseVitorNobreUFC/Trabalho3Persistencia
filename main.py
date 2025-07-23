from fastapi import FastAPI
from controllers import (
  jogo_controller,
  dlc_controller,
  usuario_controller,
  familia_controller,
  compra_controller,
  avaliacao_controller,
  query_complexas_controller
)
app = FastAPI(title="API de Jogos")

app.include_router(jogo_controller.router)
app.include_router(dlc_controller.router)
app.include_router(usuario_controller.router)
app.include_router(familia_controller.router)
app.include_router(compra_controller.router)
app.include_router(avaliacao_controller.router)
app.include_router(query_complexas_controller.router)
