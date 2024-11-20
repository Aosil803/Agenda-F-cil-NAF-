from fastapi import FastAPI
from back_end.create_db import create_tables  # Importe a função de criação de tabelas
from back_end.routas.usuario_rotas import router as usuario_rotas
from back_end.routas.adminNaf_rotas import router as adminNaf_rotas
from back_end.routas.agenda_rotas import router as agenda_rotas

app = FastAPI()

# Chama a função de criação das tabelas durante o evento de startup do FastAPI
@app.on_event("startup")
async def startup():
    create_tables()  # Cria as tabelas quando o aplicativo for iniciado

# Inclui as rotas
app.include_router(usuario_rotas)
app.include_router(adminNaf_rotas)
app.include_router(agenda_rotas)