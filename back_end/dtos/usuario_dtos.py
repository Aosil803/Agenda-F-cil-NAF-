from datetime import date
from pydantic import BaseModel, validator
from typing import Optional

class UsuarioCriar(BaseModel):
    id: Optional[int] = None
    nome: str
    perfil_usuario: str
    email: str
    cpf: str
    telefone: str
    senha: str
    cep: str
    rua: str
    numero: int
    bairro: str
    complemento: Optional[str] = None
    cidade: str
    estado: str

    @validator('perfil_usuario')
    def validar_perfil(cls, perfil_usuario):
        perfis_validos = ["Morador Local", "Colaborador Unifeso", "Aluno Unifeso", "Incrito no MEI", "Micro Prod. Rural"]
        if perfil_usuario not in perfis_validos:
            formatos_validos = ", ".join([f'"{p}"' for p in perfis_validos])
            raise ValueError(f"Campo 'perfil_usuario' inválido ou ausente. Formatos válidos: [{formatos_validos}].")
        return perfil_usuario

    class Config:
        from_attributes = True  # Permite integração direta com modelos ORM (banco de dados)
        orm_mode = True

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
