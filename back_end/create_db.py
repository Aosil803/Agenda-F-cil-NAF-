import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Caminho absoluto para o banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'NAF_agenda.db')

# Configuração do banco de dados
try:
    db = create_engine(f"sqlite:///{db_path}", echo=True)

    # Conexão com o banco de dados
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)

    Base = declarative_base()

    # Verificar se o banco de dados existe
    if os.path.exists(db_path):
        print(f"{db_path} Banco de Dados OK!")
    else:
        Base.metadata.create_all(bind=db)
        print(f"{db_path} Banco de Dados Criado com Sucesso!")

except Exception as e:
    print("ERRO: Falha ao criar Banco de Dados!")

# Função para criar as tabelas
def create_tables():
    Base.metadata.create_all(bind=db)
    print("Tabelas criadas com sucesso!")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
