# import logging
# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.orm import Session
# from back_end.models.agenda_models import Agenda
# from back_end.create_db import get_db
# from back_end.dtos.agenda_dtos import AgendaBase, AgendaCriar

# # Configurar logs para exibir erros 
# logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# logger = logging.getLogger(__name__)

# # Defina o router
# router = APIRouter()

# # Função para listar todos os agendamentos
# @router.get("/agenda/", response_model=list[AgendaBase])
# async def listar_agendamentos(db: Session = Depends(get_db)):
#     try:
#         agendamentos = db.query(Agenda).all()
#         if not agendamentos:
#             raise HTTPException(status_code=404, detail="Nenhum agendamento encontrado.")
#         return agendamentos
#     except Exception as e:
#         logger.error(f"Erro ao listar agendamentos: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"Erro ao listar agendamentos: {str(e)}")


# # Função para criar um novo agendamento
# @router.post("/agenda/", response_model=AgendaBase)
# async def criar_agendamento(agenda: AgendaCriar, db: Session = Depends(get_db)):
#     try:
#         novo_agendamento = Agenda(
#             ano=agenda.ano,
#             mes=agenda.mes,
#             dia=agenda.dia,
#             hora=agenda.hora,
#             turno=agenda.turno,
#             status=agenda.status,
#             usuario_id=agenda.usuario_id,
#         )

#         db.add(novo_agendamento)
#         db.commit()
#         db.refresh(novo_agendamento)
#         logger.info(f"Novo agendamento criado com sucesso: id {novo_agendamento.id}")
#         return novo_agendamento
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Erro ao criar agendamento: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"Erro ao criar agendamento: {str(e)}")


# # Função para atualizar um agendamento por ID
# @router.put("/agenda/{agenda_id}", response_model=AgendaBase)
# async def atualizar_agendamento(agenda_id: int, agenda: AgendaCriar, db: Session = Depends(get_db)):
#     try:
#         agendamento_existente = db.query(Agenda).filter(Agenda.id == agenda_id).first()

#         if not agendamento_existente:
#             raise HTTPException(status_code=404, detail=f"Agendamento id {agenda_id} não encontrado.")

#         # Atualizar os dados do agendamento existente
#         agendamento_existente.ano = agenda.ano
#         agendamento_existente.mes = agenda.mes
#         agendamento_existente.dia = agenda.dia
#         agendamento_existente.hora = agenda.hora
#         agendamento_existente.turno = agenda.turno
#         agendamento_existente.status = agenda.status
#         agendamento_existente.usuario_id = agenda.usuario_id

#         db.commit()
#         db.refresh(agendamento_existente)
#         logger.info(f"Agendamento id {agenda_id} atualizado com sucesso.")
#         return agendamento_existente
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Erro ao atualizar agendamento: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"Erro ao atualizar agendamento: {str(e)}")
