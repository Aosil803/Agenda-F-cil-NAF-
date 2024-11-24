from datetime import date
from pydantic import BaseModel, validator
from typing import Optional

# DTO de entrada (para criação do usuário)
class UsuarioCriar(BaseModel):
    id: Optional[int] = None
    nome: str
    perfil: str
    email: str
    cpf: str
    telefone: str
    senha: str
    cep: str
    rua: str
    numero: str
    bairro: str
    complemento: Optional[str] = None
    cidade: str
    estado: str

    class Config:
        orm_mode = True  # Permite integração direta com modelos ORM (banco de dados)

# DTO para atualização de usuário (PUT) que herda de UsuarioCriar
class UsuarioAtualizar(BaseModel):
    # Alterando todos os campos para Optional com base nos campos de UsuarioCriar
    nome: Optional[str] = None
    perfil: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    senha: Optional[str] = None
    cep: Optional[str] = None
    rua: Optional[str] = None
    numero: Optional[str] = None
    bairro: Optional[str] = None
    complemento: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None

    class Config:
        orm_mode = True  # Permite integração direta com modelos ORM (banco de dados)

# DTO de saída (para resposta com a data formatada e o ID no topo)
class UsuarioResposta(UsuarioCriar):
    data_criacao: str  # Vai ser retornada como string

    @validator('data_criacao', pre=True)
    def format_data_criacao(cls, v):
        # Certifica-se que a data seja formatada corretamente para o formato DD/MM/YYYY
        if isinstance(v, date):
            return v.strftime('%d/%m/%Y')
        return v  # Se já for string, retorna como está
    
    

    class Config:
        from_attributes = True  # Garante compatibilidade com objetos do ORM
        orm_mode = True
