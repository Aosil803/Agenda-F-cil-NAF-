from datetime import datetime
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship
from back_end.create_db import Base

class AdminNaf(Base):
    __tablename__ = "adminNaf"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    matricula = Column(String, unique=True, nullable=False)  # Matrícula única e obrigatória
    email = Column(String, nullable=False) 
    senha = Column(String, nullable=False)  # Senha obrigatória
    perfil = Column(String, nullable=False )  # Perfil obrigatório
    data_criacao = Column(Date, default=datetime.utcnow)
    
    # Relacionamento com Agenda
    agendas = relationship("Agenda", back_populates="administrador")
