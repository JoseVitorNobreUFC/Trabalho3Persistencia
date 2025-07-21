from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class FamiliaBase(BaseModel):
    nome: str
    data_criacao: date
    is_public: bool
    descricao: Optional[str] = None

class FamiliaCreate(FamiliaBase):
    criador_id: str

class FamiliaUpdate(BaseModel):
    nome: Optional[str]
    data_criacao: Optional[date]
    is_public: Optional[bool]
    descricao: Optional[str]

class FamiliaDB(FamiliaBase):
    id: str
    criador_id: str

    @classmethod
    def from_mongo(cls, data: dict):
        data["id"] = str(data.pop("_id"))
        return cls(**data)

    class Config:
        from_attributes = True
