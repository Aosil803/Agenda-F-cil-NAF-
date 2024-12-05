from calendar import monthrange
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, date

# DTO para criação de horários
class AgendaCriar(BaseModel):
    id: Optional[int] = None
    matricula: str
    ano: int
    mes: str
    dia: int
    turno: str
    hora: str

class AgendamentoCriar(BaseModel):
    id: Optional[int] = None
    cpf: Optional[str] = None
    ano: int
    mes: str
    dia: int
    turno: str
    hora: str

    # Validação do mês
    @validator('mes')
    def validar_mes(cls, mes):
        meses_validos = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        if mes not in meses_validos:
            formatos_validos = ", ".join([f'"{m}"' for m in meses_validos])
            raise ValueError(f"inválido ou ausente, formatos válidos [{formatos_validos}]")
        return mes

    # Validação do dia
    @validator('dia')
    def validar_dia(cls, dia, values):
        ano = values.get("ano")
        mes = values.get("mes")

        if not ano or not mes:
            return dia

        meses_validos = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        mes_num = meses_validos.index(mes) + 1
        max_dias = monthrange(ano, mes_num)[1]

        if dia < 1 or dia > max_dias:
            raise ValueError(f"Para o mês de {mes}, o dia deve ser entre 1 a {max_dias}")

        return dia

    # Validação do turno
    @validator('turno')
    def validar_turno(cls, turno):
        if turno not in ["manhã", "tarde"]:
            raise ValueError("Turno inválido. Deve ser 'manhã' ou 'tarde'.")
        return turno

    # Validação da hora
    @validator('hora')
    def validar_hora(cls, hora, values):
        turno = values.get("turno")
        hora_obj = datetime.strptime(hora, "%H:%M").time()

        if turno == "manhã":
            hora_inicio = datetime.strptime("09:00", "%H:%M").time()
            hora_fim = datetime.strptime("11:59", "%H:%M").time()
            if not (hora_inicio <= hora_obj <= hora_fim):
                raise ValueError(f"Para o turno 'manhã', a hora deve estar entre 9:00 e 11:59.")
        elif turno == "tarde":
            hora_inicio = datetime.strptime("12:00", "%H:%M").time()
            hora_fim = datetime.strptime("18:00", "%H:%M").time()
            if not (hora_inicio <= hora_obj <= hora_fim):
                raise ValueError(f"Para o turno 'tarde', a hora deve estar entre 12:00 e 18:00.")

        return hora

# DTO para resposta de criação de horários
class AgendaResposta(BaseModel):
    id: int
    ano: int
    mes: str
    dia: int
    turno: str
    hora: str
    data_criacao: str

    @validator('data_criacao', pre=True)
    def format_data_criacao(cls, v):
        if isinstance(v, date):
            return v.strftime('%d/%m/%Y')
        return v

    class Config:
        from_attributes = True

# DTO para agendamento de horário (POST específico)
# # class Agendamento(BaseModel):    
# #     cpf: str
# #     ano: int
# #     mes: str
# #     dia: int
# #     turno: str
# #     hora: str

# #     # Validação do mês
# #     @validator('mes')
# #     def validar_mes(cls, mes):
# #         meses_validos = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
# #         if mes not in meses_validos:
# #             formatos_validos = ", ".join([f'"{m}"' for m in meses_validos])
# #             raise ValueError(f"inválido ou ausente, formatos válidos [{formatos_validos}]")
# #         return mes

#     # Validação da hora
#     @validator('hora')
#     def validar_hora(cls, hora):
#         try:
#             datetime.strptime(hora, "%H:%M")
#         except ValueError:
#             raise ValueError("Formato de hora inválido. Deve ser HH:MM.")
#         return hora

# DTO para resposta do agendamento
class AgendamentoResposta(BaseModel):
    id: int
    ano: int
    mes: str
    dia: int
    turno: str
    hora: str
    data_criacao: str
    data_agendamento: str

    @validator('data_criacao', pre=True)
    def format_data_criacao(cls, v):
        if isinstance(v, date):
            return v.strftime('%d/%m/%Y')
        return v

    class Config:
        from_attributes = True
