from calendar import monthrange
from pydantic import BaseModel, validator
from typing import Literal, Optional
from datetime import date, datetime

class Agendamento(BaseModel):
    id: Optional[int] = None
    ano: int
    mes: Literal["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    dia: int
    turno: str
    hora: str
    status: Optional[bool] = None

    # Função para converter a string de data em um objeto datetime
    def converte_str_datetime(self):
        meses = {
            'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6,
            'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12
        }
        try:
            mes_num = meses[self.mes.lower()]  # Converte o mês para número
            data = datetime(int(self.ano), mes_num, self.dia)  # Converte a data
            return data
        except KeyError:
            raise ValueError(self.mes.lower())  # Apenas retorna o nome do mês em minúsculo
        except ValueError as e:
            raise ValueError(str(e))  # Retorna o erro como string sem mensagem adicional

    @validator('mes')
    def validar_mes(cls, mes):
        meses_validos = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        if mes not in meses_validos:
            formatos_validos = ", ".join([f'"{m}"' for m in meses_validos])
            raise ValueError(f"inválido ou ausente, formatos válidos [{formatos_validos}]")
        return mes

    @validator('dia')
    def validar_dia(cls, dia, values):
        ano = values.get("ano")
        mes = values.get("mes")

        if not ano or not mes:
            return dia

        # Mapeamento do mês para número
        meses_validos = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        mes_num = meses_validos.index(mes) + 1

        # Verifica o número de dias válidos para o mês e ano
        max_dias = monthrange(ano, mes_num)[1]

        if dia < 1 or dia > max_dias:
            raise ValueError(f"inválido ou ausente. Para o mês de {mes}, o dia deve ser entre 1 e {max_dias}.")

        return dia

class UsuarioAgendamento(Agendamento):
    usuario_id: Optional[int] = None

class AgendamentoResposta(Agendamento):
    usuario_id: Optional[int] = None
    data_criacao: str  # Vai ser retornada como string
    
    @validator('data_criacao', pre=True)
    def format_data_criacao(cls, v):
        # Certifique-se de que a data seja formatada corretamente para o formato DD/MM/YYYY
        if isinstance(v, date):
            return v.strftime('%d/%m/%Y')
        return v

class AgendaOcupadaResposta(Agendamento):
    data_criacao: str
    
    @validator('data_criacao', pre=True)
    def format_data_criacao(cls, v):
        # Certifique-se de que a data seja formatada corretamente para o formato DD/MM/YYYY
        if isinstance(v, date):
            return v.strftime('%d/%m/%Y')
        return v

    class Config:
        from_attributes = True  # Atualização para Pydantic V2
