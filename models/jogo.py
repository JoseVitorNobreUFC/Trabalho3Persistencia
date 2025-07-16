from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from bson import ObjectId

class JogoBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_lancamento: date
    preco: float
    desenvolvedora: str

class JogoCreate(JogoBase):
    pass

class JogoDB(JogoBase):
    id: str = Field(alias="_id")

    class Config:
        allow_population_by_field_name = True

class JogoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_lancamento: Optional[date] = None
    preco: Optional[float] = None
    desenvolvedora: Optional[str] = None
