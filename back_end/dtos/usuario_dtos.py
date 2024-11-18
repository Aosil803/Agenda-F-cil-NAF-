from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# DTO para criar campos de endereço
class CamposEndereco(BaseModel):
    cep: str
    rua: str
    numero: int
    bairro: str
    complemento: Optional[str] = None  # Campo opcional
    cidade: str
    estado: str
    

    class Config:
        from_attributes = True


# DTO para criação de um novo usuário
class UsuarioCriar(BaseModel):
    nome: str
    email: str
    cpf: str
    telefone: str
    endereco: CamposEndereco 
    perfil: str
    senha: str
    data_criacao: datetime = datetime.utcnow()

    class Config:
       from_attributes = True


# DTO Base para retornar dados de usuários (sem expor informações sensíveis)
class UsuarioBase(BaseModel):
    id: int
    nome: str
    email: str
    endereco: CamposEndereco 
    perfil: str
    data_criacao: datetime

    class Config:
        from_attributes = True  