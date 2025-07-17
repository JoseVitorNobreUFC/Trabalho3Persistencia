from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class JogoBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_lancamento: date
    preco: float 
    desenvolvedora: str

    def dict(self, **kwargs):
        """Ao converter para dict, transforma preco em centavos (int)."""
        base = super().dict(**kwargs)
        base["preco"] = int(round(self.preco * 100))  # Float -> Int (centavos)
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
            base["preco"] = int(round(base["preco"] * 100))
        return base

class JogoDB(JogoBase):
    id: str = Field(alias="_id")

    @classmethod
    def from_mongo(cls, data: dict):
        data["preco"] = data["preco"] / 100  # Int -> Float (exibição)
        return cls(**data)

    class Config:
        from_attributes = True
