from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    data_cadastro: date
    pais: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    data_cadastro: Optional[date] = None
    pais: Optional[str] = None

class UsuarioDB(UsuarioBase):
    id: str = Field(..., alias="_id")
    familia_id: Optional[str] = ""

    @classmethod
    def from_mongo(cls, doc: dict):
        return cls(**doc)

    class Config:
        from_attributes = True
