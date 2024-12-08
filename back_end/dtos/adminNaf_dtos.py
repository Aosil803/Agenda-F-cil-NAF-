from datetime import date
from pydantic import BaseModel, validator
from typing import Optional

class AdminNafCriar(BaseModel):
    id: Optional[int] = None
    nome: str
    matricula: str
    polo: str
    telefone: str
    email: str
    senha: str
    perfil_admin: str

    @validator('perfil_admin')
    def validar_perfil(cls, perfil_admin):
        perfis_validos = ["Estudante", "Professor", "Colaborador"]
        if perfil_admin not in perfis_validos:
            formatos_validos = ", ".join([f'"{p}"' for p in perfis_validos])
            raise ValueError(f"Campo 'perfil_admin' inválido ou ausente. Formatos válidos: [{formatos_validos}].")
        return perfil_admin
    
    @validator('polo')
    def validar_polo(cls, polo):
        polos_validos = ["Teresópolis", "Petrópolis", "Magé", "Saquarema"]
        if polo not in polos_validos:
            formatos_validos = ", ".join([f'"{p}"' for p in polos_validos])
            raise ValueError(f"Campo 'polo' inválido ou ausente. Formatos válidos: [{formatos_validos}].")
        return polo

    class Config:
        from_attributes = True 
       

class AdminNafResposta(AdminNafCriar):
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
