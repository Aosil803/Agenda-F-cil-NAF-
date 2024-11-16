from create_db import db
from models.usuario import Usuario, Endereco
from models.funcionario import Funcionario
from models.agenda import Agenda
from models.horario_disponivel import HorarioDisponivel

# Agora, você cria as tabelas
Usuario.metadata.create_all(bind=db)
Endereco.metadata.create_all(bind=db)
Funcionario.metadata.create_all(bind=db)
Agenda.metadata.create_all(bind=db)
HorarioDisponivel.metadata.create_all(bind=db)