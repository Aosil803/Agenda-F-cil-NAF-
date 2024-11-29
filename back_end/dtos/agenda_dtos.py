from datetime import date
from pydantic import BaseModel, validator
from typing import Optional

class Agendamento(BaseModel):
    id: Optional[int] = None
    ano: int
    mes: str
    dia: int
    turno: str
    hora: str


class UsuarioAgendamento(Agendamento):
    ano: int
    mes: str
    dia: int
    usuario_id: Optional[int] = None

class AgendamentoResposta(Agendamento):
    data_criacao: str  # Vai ser retornada como string
    message: str = "Horário criado com sucesso!"

    @validator('data_criacao', pre=True)
    def format_data_criacao(cls, v):
        # Certifica-se que a data seja formatada corretamente para o formato DD/MM/YYYY
        if isinstance(v, date):
            return v.strftime('%d/%m/%Y')
        return v  

class AgendaOcupadaResposta(UsuarioAgendamento):
    data_criacao: str 
    message: str = "Agendamento realizado com sucesso."

    class Config:
        from_attributes = True  # Atualização para Pydantic V2
