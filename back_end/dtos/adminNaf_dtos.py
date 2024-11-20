from pydantic import BaseModel
from datetime import datetime

# DTO para criação de um novo AdminNaf
class AdminNafCriar(BaseModel):
    nome: str
    matricula: str
    email: str
    perfil: str

    class Config:
        from_attributes = True
        orm_mode = True

# DTO Base para retornar dados de usuários
class AdminNafBase(BaseModel):
    id:int
    nome: str
    matricula: str
    email: str
    perfil: str
    data_criacao: datetime

    class Config:
        from_attributes = True
        orm_mode = True


   