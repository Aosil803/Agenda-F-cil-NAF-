from back_end.create_db import db, Base  
from back_end.models.usuario_models import Usuario 
#from back_end.models.adminNaf_models import AdminNaf  
#from back_end.models.agenda_models import Agenda    


# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=db)

# Verificar se as tabelas foram criadas
print(f"Tabelas criadas no banco de dados {db}")
