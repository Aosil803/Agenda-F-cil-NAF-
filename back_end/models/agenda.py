from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from create_db import Base

class Agenda(Base):
    __tablename__ = "agendas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    dia = Column(Integer, nullable=False)
    turno = Column(Enum("Manhã", "Tarde", name="turnos_enum"), nullable=False)
    hora = Column(Integer, nullable=False)  # Hora do agendamento

    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    funcionario_id = Column(Integer, ForeignKey('funcionarios.id'), nullable=False)

    usuario = relationship("Usuario", back_populates="agendamentos")
    funcionario = relationship("Funcionario", back_populates="agendamentos")

    @property
    def data_horario(self):
        """Retorna um objeto datetime baseado nos campos individuais."""
        return datetime(self.ano, self.mes, self.dia, self.hora)

    def validar_data(self):
        """Valida a combinação de ano, mês, dia e hora."""
        try:
            datetime(self.ano, self.mes, self.dia, self.hora)
        except ValueError:
            raise ValueError("A combinação de ano, mês, dia e hora é inválida.")
