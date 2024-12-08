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

    # Função para criar as tabelas
    def create_tables():
        from back_end.models.usuario_models import Usuario  
        from back_end.models.adminNaf_models import AdminNaf  
        from back_end.models.agenda_models import Agenda
        from back_end.models.login_models import Login
        
        Base.metadata.create_all(bind=db)  
        print("BANCO DE DADOS E TABELAS CRIADAS COM SUCESSO!")

    # Verificar se o banco de dados existe
    if os.path.exists(db_path):
        print("BANCO DE DADOS JÁ EXISTE!")
    else:
        print(f"{db_path} BANCO DE DADOS NÃO ECONTRADO, CRIANDO...")
        create_tables()
        print("BANCO DE DADOS E TABELAS CRIADOS COM SUCESSO!")

except Exception as e:
    print(f"ERRO: FALHA AO CRIAR BANCO DE DADOS! {str(e)}")

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
