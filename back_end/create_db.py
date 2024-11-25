import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Caminho absoluto para o banco de dados na raiz do projeto
db_path = os.path.join(os.path.dirname(__file__), '..', 'NAF_agenda.db')

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
        print(f"{db_path} Banco de Dados não encontrado, criando...")
        Base.metadata.create_all(bind=db)
        print(f"{db_path} Banco de Dados Criado com Sucesso!")

except Exception as e:
    print("ERRO: Falha ao criar Banco de Dados!")

# Importar os modelos para garantir que o SQLAlchemy registre as tabelas
from back_end.models.usuario_models import Usuario  
from back_end.models.adminNaf_models import AdminNaf  
from back_end.models.agenda_models import Agenda

# Função para criar as tabelas
def create_tables():
    try:
        Base.metadata.create_all(bind=db)  # Criar todas as tabelas
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {str(e)}")

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
