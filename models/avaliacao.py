from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date

class AvaliacaoBase(BaseModel):
    usuario_id: str
    item_id: str 
    nota: int
    comentario: Optional[str] = None
    data_avaliacao: date

    @validator("nota")
    def nota_deve_ser_valida(cls, v):
        if not (0 <= v <= 10):
            raise ValueError("Nota deve estar entre 0 e 10")
        return v

class AvaliacaoCreate(AvaliacaoBase):
    pass

class AvaliacaoUpdate(BaseModel):
    usuario_id: Optional[str] = None
    item_id: Optional[str] = None
    nota: Optional[int] = None
    comentario: Optional[str] = None
    data_avaliacao: Optional[date] = None

    @validator("nota")
    def nota_deve_ser_valida(cls, v):
        if v is not None and not (0 <= v <= 10):
            raise ValueError("Nota deve estar entre 0 e 10")
        return v

class AvaliacaoDB(AvaliacaoBase):
    id: str = Field(alias="_id")

    @classmethod
    def from_mongo(cls, data: dict):
        return cls(**data)

    class Config:
        from_attributes = True