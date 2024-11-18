from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# DTO para criação de um novo usuário
class UsuarioCriar(BaseModel):
    nome: str
    perfil: str
    email: str
    cpf: str
    senha: str
    cep: str
    rua: str
    numero: str
    bairro: str
    complemento: Optional[str] = None
    cidade: str
    estado: str
    telefone: str

    class Config:
        from_attributes = True
        orm_mode = True

# DTO Base para retornar dados de usuários (sem expor informações sensíveis)
class UsuarioBase(BaseModel):
    id: int
    nome: str
    perfil: str
    email: str
    cpf: str
    senha: str
    cep: str
    rua: str
    numero: str
    bairro: str
    complemento: Optional[str] = None
    cidade: str
    estado: str
    telefone: str
    data_criacao: datetime

    class Config:
        from_attributes = True
        orm_mode = True