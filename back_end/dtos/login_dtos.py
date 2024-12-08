
import datetime
from datetime import date
from typing import Optional
from pydantic import BaseModel, validator, Field
import jwt

# Configurações do JWT
SECRET_KEY = "sua_chave_secreta"
ALGORITHM = "HS256"

def criar_access_token(dados: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    to_encode = dados.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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
        from_attributes = True

class UsuarioLoginRespostaComToken(BaseModel):
    id_login: Optional[int]
    usuario: str
    email: str
    senha: str
    access_token: Optional[str] = Field(None, description="Token de autenticação")
    data_criacao: str
   
    @validator('data_criacao', pre=True)
    def format_data_criacao(cls, v):
        if isinstance(v, date):
            return v.strftime('%d/%m/%Y')
        return v
    
    class Config:
        from_attributes = True
