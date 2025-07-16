from fastapi import FastAPI
from controllers import jogo_controller

app = FastAPI(title="API de Jogos")

app.include_router(jogo_controller.router)

