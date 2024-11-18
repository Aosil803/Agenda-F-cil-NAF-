from back_end.create_db import db, Base  # Importa o engine e o Base
from back_end.models.usuario_models import Usuario, Endereco  # Tabelas relacionadas a usuários
from back_end.models.funcionario_models import Funcionario  # Tabelas relacionadas a funcionários
from back_end.models.agenda_models import Agenda  # Tabelas relacionadas a agenda
from back_end.models.horarioDisponivel_models import HorarioDisponivel  # Tabelas relacionadas a horários

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=db)

# Verificar se as tabelas foram criadas
print(f"Tabelas criadas no banco de dados {db}")
