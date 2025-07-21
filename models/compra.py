from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum
import math

class FormaPagamento(str, Enum):
    CARTAO = "Cartão"
    BOLETO = "Boleto"
    PIX = "Pix"

class CompraBase(BaseModel):
    usuario_id: str
    item_id: str 
    preco_pago: float
    forma_pagamento: FormaPagamento
    data_compra: date

    def dict(self, **kwargs):
        base = super().dict(**kwargs)
        base["preco_pago"] = int(math.floor(self.preco_pago * 100))
        return base

class CompraCreate(CompraBase):
    pass

class CompraUpdate(BaseModel):
    preco_pago: Optional[float] = None
    forma_pagamento: Optional[FormaPagamento] = None

    def dict(self, **kwargs):
        base = super().dict(**kwargs)
        if "preco_pago" in base and base["preco_pago"] is not None:
            base["preco_pago"] = int(math.floor(base["preco_pago"] * 100))
        return base

class CompraDB(CompraBase):
    id: str = Field(alias="_id")

    @classmethod
    def from_mongo(cls, data: dict):
        data["preco_pago"] = f"{data['preco_pago'] / 100:.2f}"
        return cls(**data)

    class Config:
        from_attributes = True