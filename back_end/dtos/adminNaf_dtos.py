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

    class Config:
        from_attributes = True  # Permite integração direta com modelos ORM (banco de dados)
        orm_mode = True

class AdminNafResposta(AdminNafCriar):
    data_criacao: str  # Vai ser retornada como string

    @validator('data_criacao', pre=True)
    def format_data_criacao(cls, v):
        if isinstance(v, date):
            return v.strftime('%d/%m/%Y')
        return v  # Se já for string, retorna como está

    class Config:
        from_attributes = True  # Garante compatibilidade com objetos do ORM
