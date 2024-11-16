import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Caminho absoluto para o banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'NAF_agenda.db')
print(f"Caminho do banco de dados: {db_path}")

# Configuração do banco de dados
db = create_engine(f"sqlite:///{db_path}", echo=True)

# Conexão com o banco de dados
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

# Criação das tabelas
Base.metadata.create_all(bind=db)

# Verificar se o banco de dados foi criado
if os.path.exists(db_path):
    print(f"Banco de dados {db_path} foi criado com sucesso!")
else:
    print("Falha na criação do banco de dados.")
