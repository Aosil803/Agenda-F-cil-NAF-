from sqlalchemy import Column, Integer, String
from back_end.create_db import Base

class AdminNaf(Base):
    __tablename__ = 'admin_naf' 

    id = Column(Integer, primary_key=True, autoincrement=True)  
    matricula = Column(String, unique=True, nullable=False)  # Matrícula única e obrigatória
    email = Column(String, unique=True, nullable=False)   # Email único e obrigatória
    senha = Column(String, nullable=False)  # Senha obrigatória
    perfil = Column(String, nullable=False )  # Perfil obrigatório
   

    def __repr__(self):
        return f"<AdminNaf(id={self.id}, matricula={self.matricula}, email={self.email})>"
