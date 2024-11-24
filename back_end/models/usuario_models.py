from datetime import datetime
from sqlalchemy import Column, Integer, String, Date
from back_end.create_db import Base

# Modelo Usuario
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    perfil = Column(String, nullable=False)
    email = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    rua = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    bairro = Column(String, nullable=False)
    complemento = Column(String, nullable=True)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    telefone = Column(String, nullable=True)
    data_criacao = Column(Date, default=datetime.utcnow)

