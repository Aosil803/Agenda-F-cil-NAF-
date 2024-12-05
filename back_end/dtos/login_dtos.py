from datetime import date
from typing import Optional
from pydantic import BaseModel, validator

class UsuarioLoginCriar(BaseModel):
    id_login: Optional[int] = None
    usuario: str
    email: str
    senha: str
    matricula: Optional[str] = None 
     
class UsuarioLoginRespostaSemToken(BaseModel):
    id_login: Optional[int]
    usuario: str
    email: str
    data_criacao: str

    @validator('data_criacao', pre=True)
    def format_data_criacao(cls, v):
        if isinstance(v, date):
            return v.strftime('%d/%m/%Y')
        return v

    class Config:
        orm_mode = True
        from_attributes = True

class UsuarioLoginRespostaComToken(UsuarioLoginCriar):
    access_token: str
    token_type: str = "bearer"
    senha: str = "*******(Sem visualização)"
    data_criacao: str

    @validator('data_criacao', pre=True)
    def format_data_criacao(cls, v):
        if isinstance(v, date):
            return v.strftime('%d/%m/%Y')
        return v

    class Config:
        orm_mode = True
