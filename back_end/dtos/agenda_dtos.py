# from pydantic import BaseModel
# from datetime import datetime


# # DTO para criação de um novo Agendamento
# class AgendaCriar(BaseModel):
#     id: int
#     ano: int
#     mes: str
#     dia: datetime
#     hora: int
#     turno: str
#     status: bool
#     usuario_id: int

# class Config:
#         from_attributes = True
#         orm_mode = True

# # DTO Base para retornar dados de agendamento
# class AgendaBase(BaseModel):
#     id: int
#     ano: int
#     mes: str
#     dia: datetime
#     hora: int
#     turno: str
#     status: bool
#     usuario_id: int

#     class Config:
#         from_attributes = True
#         orm_mode = True
