from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from back_end.create_db import get_db
from back_end.dtos.agenda_dtos import AgendamentoCriar, AgendamentoResposta, UsuarioAgendamento
from back_end.models.agenda_models import Agenda
from back_end.utils.error_handlers import horario_nao_disponivel, validar_hora
# from .auth import get_current_user  # Deixe comentado para evitar erros

router = APIRouter()

# Função para criar um agendamento
@router.post("/agenda/", response_model=AgendamentoResposta)
def criar_horario(agenda: AgendamentoCriar, db: Session = Depends(get_db)):
    # Usa a função de validação para validar e formatar a hora
    hora_formatada = validar_hora(agenda.hora)

    novo_horario = Agenda(
        ano=agenda.ano,
        mes=agenda.mes,
        dia=agenda.dia,
        hora=hora_formatada,  # Armazena a hora como string no formato HH:MM
        turno=agenda.turno,
        status=True  # O status é True para indicar que o horário está livre
    )

    db.add(novo_horario)
    db.commit()
    db.refresh(novo_horario)

    return novo_horario


# Função para usuario criar um agendamento
@router.post("/agendar/", response_model=AgendamentoResposta)
def agendar_horario(agendamento: UsuarioAgendamento, db: Session = Depends(get_db)):
    # current_user: dict = Depends(get_current_user)  # Comentar a autenticação por enquanto

    # Verifica se o horário está disponível
    horario = db.query(Agenda).filter(
        Agenda.ano == agendamento.ano,
        Agenda.mes == agendamento.mes,
        Agenda.dia == agendamento.dia,
        Agenda.hora == agendamento.hora,
        Agenda.turno == agendamento.turno,
        Agenda.status == True
    ).first()
    
    if not horario:
        horario_nao_disponivel()  # Função que lança exceção se o horário não estiver disponível

    # Atualiza o status do horário para False
    horario.status = False
    # horario.usuario_id = current_user['id']  # Comentar por enquanto

    db.commit()
    db.refresh(horario)

    return horario




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

