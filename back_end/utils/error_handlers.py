from calendar import monthrange
import logging
from fastapi import HTTPException, Request
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import status

# Configuração do logging
logger = logging.getLogger(__name__)

# Novo handler para erro de banco de dados
def handle_database_error(db: Session, exception: Exception):
    try:
        db.rollback()
        logger.error(f"Erro ao processar a requisição: {str(exception)}")
    except Exception as e:
        logger.error(f"Erro ao fazer rollback: {str(e)}")
    finally:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar a requisição! " + str(exception)
        )

# Handler genérico para HTTPException (qualquer erro 400, 404, etc.)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"Erro {exc.status_code}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Erro {exc.status_code} ao processar a requisição! {exc.detail}"}
    )

# Handler para capturar erros de validação
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Captura campos ausentes ou inválidos e formata a mensagem de erro
    error_messages = []
    meses_validos = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    for err in exc.errors():
        loc = err['loc'][-1]
        if loc == 'mes':
            error_messages.append(f"Campo '{loc}' inválido ou ausente. Formatos válidos: {meses_validos}.")
        elif loc == 'dia':
            ano = None
            mes = None
            for context in exc.errors():
                if context['loc'][-1] == 'ano':
                    ano = context['msg']
                if context['loc'][-1] == 'mes':
                    mes = context['msg']
            if ano and mes:
                mes_num = meses_validos.index(mes) + 1
                max_dias = monthrange(int(ano), mes_num)[1]
                error_messages.append(f"Campo '{loc}' inválido ou ausente. Para o mês de {mes}, o dia deve ser entre 1 e {max_dias}.")
            else:
                error_messages.append(f"Campo '{loc}' inválido ou ausente.")
        else:
            error_messages.append(f"Campo '{loc}' inválido ou ausente.")
    
    # Cria uma mensagem consolidada dos erros
    mensagem_formatada = " | ".join(error_messages)  # Une as mensagens com separador

    # Log detalhado do erro
    logger.error(f"Erro de validação detectado: {mensagem_formatada}")

    # Retorna a mensagem padronizada
    return JSONResponse(
        status_code=422,  # Mantém o código de erro correto
        content={
            "message": f"Erro 422 ao processar a requisição! {mensagem_formatada}"  # Mensagem padronizada
        }
    )

# Handler específico para erros de validação de dados personalizados
async def validation_exception_handler_data(request: Request, exc: ValidationError):
    # Aqui, podemos personalizar a resposta de erro para o formato que você deseja
    errors = []
    
    for error in exc.errors():
        loc = error.get("loc")  # Exemplo: loc pode ter 'mes' ou 'dia'
        if loc:
            field = loc[0]
            message = error.get("msg")
            # Caso seja um erro de 'mes', customize a mensagem de erro
            if field == 'mes':
                errors.append({
                    "message": f"Erro 422 ao processar a requisição! Campo '{field}' inválido. Deve ser um dos valores: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']."
                })
            elif field == 'dia':
                # Verifique se o erro é sobre o dia e a data fornecida
                errors.append({
                    "message": f"Erro 422 ao processar a requisição! Campo '{field}' inválido. Deve ser um dos valores: [01 a 28] ou [01 a 30] ou [01 a 31] (vai depender do mês que for colocado)."
                })
            else:
                errors.append({
                    "message": f"Erro 422 ao processar a requisição! Campo '{field}' inválido. {message}."
                })
    
    # Aqui estamos retornando uma resposta personalizada
    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )
