from fastapi import FastAPI
from back_end.create_db import create_tables  # Importe a função de criação de tabelas
from back_end.routes.usuario import router as usuario_rotas

app = FastAPI()

# Chama a função para criar as tabelas
create_tables()

# Inclui as rotas
app.include_router(usuario_rotas)
