from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
import math

class DLCBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_lancamento: date
    preco: float
    jogo_id: str

    def dict(self, **kwargs):
        base = super().dict(**kwargs)
        base["preco"] = int(math.floor(self.preco * 100)) 
        return base

class DLCCreate(DLCBase):
    pass

class DLCUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_lancamento: Optional[date] = None
    preco: Optional[float] = None
    jogo_id: Optional[str] = None

    def dict(self, **kwargs):
        base = super().dict(**kwargs)
        if "preco" in base and base["preco"] is not None:
            base["preco"] = int(math.floor(base["preco"] * 100))
        return base

class DLCDB(DLCBase):
    id: str = Field(alias="_id")

    @classmethod
    def from_mongo(cls, data: dict):
        data["preco"] = f"{data['preco'] / 100:.2f}"
        return cls(**data)

    class Config:
        from_attributes = True
