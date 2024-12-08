from datetime import datetime
from sqlalchemy import CHAR, Column, Date, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from back_end.create_db import Base

class Agenda(Base):
    __tablename__ = "agenda"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ano = Column(Integer, nullable=False)
    mes = Column(String, nullable=False)
    dia = Column(Integer, nullable=False)
    turno =  Column(CHAR(10), nullable=False)
    hora = Column(String, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    data_criacao = Column(Date, default=datetime.utcnow)
    data_agendamento = Column(Date, nullable=True)  
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=True)  
    adminNaf_id = Column(Integer, ForeignKey("adminNaf.id"), nullable=True)
    usuario = relationship("Usuario", back_populates="agenda")
    administrador = relationship("AdminNaf", back_populates="agendas")
