import logging
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from back_end.create_db import create_tables  # Função para criação de tabelas
from back_end.route.usuario_route import router as usuario_route
from back_end.utils.error_handlers import http_exception_handler, validation_exception_handler  # Importando os handlers

app = FastAPI()

# Configuração do logging
logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Chama a função de criação das tabelas durante o evento de startup do FastAPI
@app.on_event("startup")
async def startup():
    create_tables()  # Cria as tabelas quando o aplicativo for iniciado

# Inclui as rotas
app.include_router(usuario_route)
# app.include_router(adminNaf_route)
# app.include_router(agenda_route)

# Adiciona os handlers de erro ao FastAPI
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
