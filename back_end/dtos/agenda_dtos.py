from datetime import date
from pydantic import BaseModel, validator
from typing import Optional

class AgendamentoCriar(BaseModel):
    id: Optional[int] = None
    ano: int
    mes: str
    dia: int
    hora: str  # Hora armazenada como string
    turno: str
    status: bool
    
    class Config:
        from_attributes = True  # Atualização para Pydantic V2
        
class UsuarioAgendamento(BaseModel):
    ano: int
    mes: str
    dia: int
    hora: str
    turno: str

    class Config:
        from_attributes = True  # Atualização para Pydantic V2

class AgendamentoResposta(AgendamentoCriar):
    data_criacao: str  # Vai ser retornada como string

    @validator('data_criacao', pre=True)
    def format_data_criacao(cls, v):
        # Certifica-se que a data seja formatada corretamente para o formato DD/MM/YYYY
        if isinstance(v, date):
            return v.strftime('%d/%m/%Y')
        return v  # Se já for string, retorna como está
    
    class Config:
        from_attributes = True  # Atualização para Pydantic V2
