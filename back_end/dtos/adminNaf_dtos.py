from pydantic import BaseModel, validator
from datetime import date
from typing import Optional

# DTO para criação de um novo AdminNaf
class AdminNafCriar(BaseModel):
    id: Optional[int] = None
    nome: str
    matricula: str
    email: str
    senha: str
    perfil: str

    class Config:
        from_attributes = True
        orm_mode = True

# DTO de saída (para resposta com a data formatada e o ID no topo)
class AdminNafResposta(AdminNafCriar):
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
