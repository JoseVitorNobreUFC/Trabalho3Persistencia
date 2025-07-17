from fastapi import FastAPI
from controllers import jogo_controller, dlc_controller

app = FastAPI(title="API de Jogos")

app.include_router(jogo_controller.router)
app.include_router(dlc_controller.router)

