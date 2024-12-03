from datetime import datetime
from sqlalchemy import CHAR, Column, Date, Integer, String
from sqlalchemy.orm import relationship
from back_end.create_db import Base

class AdminNaf(Base):
    __tablename__ = "adminNaf"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    matricula = Column(String, unique=True, nullable=False)  
    email = Column(String, nullable=False) 
    senha = Column(String, nullable=False)  
    perfil_admin = Column(CHAR(25), nullable=False)  
    data_criacao = Column(Date, default=datetime.utcnow)
    
    # Relacionamento com Agenda (1:N)
    agendas = relationship("Agenda", back_populates="administrador")
