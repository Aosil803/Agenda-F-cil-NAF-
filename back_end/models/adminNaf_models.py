from sqlalchemy import Column, Integer, String
from back_end.create_db import Base

class AdminNaf(Base):
    __tablename__ = 'adminNaf' 

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    matricula = Column(String, unique=True, nullable=False)  # Matrícula única e obrigatória
    email = Column(String, unique=True, nullable=False)   # Email único e obrigatória
    senha = Column(String, nullable=False)  # Senha obrigatória
    perfil = Column(String, nullable=False )  # Perfil obrigatório


   
   

   