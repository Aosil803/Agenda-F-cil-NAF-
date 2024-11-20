from sqlalchemy import Column, Date, Enum, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from back_end.create_db import Base

class Agenda(Base):
    __tablename__ = "agenda"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ano = Column(Integer, nullable=False)
    mes = Column(String, nullable=False)
    dia = Column(Date, nullable=False)
    hora = Column(Integer, nullable=False)
    turno = Column(Enum("Manhã", "Tarde", name="turnos_enum"), nullable=False)
    status = Column(Boolean, nullable=False, default=False)  # Status para indicar se o horário está livre ou agendado
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)  # Relacionamento com o usuário

    
    
