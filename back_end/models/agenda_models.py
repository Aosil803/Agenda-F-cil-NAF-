from datetime import datetime
from sqlalchemy import Column, Date, Integer, Boolean, ForeignKey, String, Time
from back_end.create_db import Base

class Agenda(Base):
    __tablename__ = "agenda"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ano = Column(Integer, nullable=False)
    mes = Column(String, nullable=False)
    dia = Column(Integer, nullable=False)
    hora = Column(String, nullable=False)
    turno = Column(String, nullable=False)
    status = Column(Boolean, nullable=False, default=False) 
    data_criacao = Column(Date, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True) 

    
    
