from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
import math

class JogoBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_lancamento: date
    preco: float 
    desenvolvedora: str

    def dict(self, **kwargs):
        base = super().dict(**kwargs)
        base["preco"] = int(math.floor(self.preco * 100)) 
        return base

class JogoCreate(JogoBase):
    pass

class JogoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_lancamento: Optional[date] = None
    preco: Optional[float] = None
    desenvolvedora: Optional[str] = None

    def dict(self, **kwargs):
        base = super().dict(**kwargs)
        if "preco" in base and base["preco"] is not None:
            base["preco"] = int(math.floor(base["preco"] * 100))
        return base

class JogoDB(JogoBase):
    id: str = Field(alias="_id")

    @classmethod
    def from_mongo(cls, data: dict):
        data["preco"] = f"{data['preco'] / 100:.2f}"
        return cls(**data)

    class Config:
        from_attributes = True
