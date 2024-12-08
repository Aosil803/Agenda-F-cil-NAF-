from back_end.create_db import db, Base  
from back_end.models.usuario_models import Usuario 
from back_end.models.adminNaf_models import AdminNaf  
from back_end.models.agenda_models import Agenda    
from back_end.models.login_models import Login


Base.metadata.create_all(bind=db)

print(f"Tabelas criadas no banco de dados {db}")
