from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from back_end.create_db import get_db
from back_end.dtos.agenda_dtos import AgendaCriar, AgendaResposta, AgendamentoCriar, AgendamentoResposta
from back_end.models.adminNaf_models import AdminNaf
from back_end.models.agenda_models import Agenda
from back_end.models.usuario_models import Usuario
from back_end.utils.get_usuario_id import get_usuario_id  # Ajuste o caminho conforme necessário
from back_end.utils.error_handlers import handle_database_error

router = APIRouter()

# Função para retornar todos os agendamentos
@router.get("/agenda/", response_model=list[AgendaResposta])
async def get_agendamentos(db: Session = Depends(get_db)):
    agendamentos = db.query(Agenda).all()
    if not agendamentos:
        raise HTTPException(status_code=404, detail="Nenhum agendamento encontrado no Banco de Dados.")
    return agendamentos

# Função para retornar agendamento por id
@router.get("/agenda/{agenda_id}", response_model=AgendaResposta)
async def get_agenda(agenda_id: int, db: Session = Depends(get_db)):
    # Busca o usuário no banco de dados
    agenda = db.query(Agenda).filter(Agenda.id == agenda_id).first()
    if not agenda:
        raise HTTPException(status_code=404, detail=f"Agendamento com Id {agenda_id} não existe no Banco de Dados.")
    return agenda

# Função para criar uma data de agendamento
@router.post("/agenda/", response_model=AgendaResposta)
def criar_horario(agenda: AgendaCriar, db: Session = Depends(get_db)):
    try:
        # Verifica se a matrícula fornecida corresponde a um AdminNaf existente
        admin = db.query(AdminNaf).filter(AdminNaf.matricula == agenda.matricula).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Administrador não encontrado para a matrícula fornecida.")

        # Verifica se o horário já existe
        horario = db.query(Agenda).filter(
            Agenda.ano == agenda.ano,
            Agenda.mes == agenda.mes,
            Agenda.dia == agenda.dia,
            Agenda.turno == agenda.turno,
            Agenda.hora == agenda.hora
        ).first()

        if horario is not None:
            raise HTTPException(status_code=400, detail="Horário com esses dados já existe no Banco de Dados.")

        # Cria novo horário associado ao AdminNaf
        novo_horario = Agenda(
            ano=agenda.ano,
            mes=agenda.mes,
            dia=agenda.dia,
            turno=agenda.turno,
            hora=agenda.hora,
            status=True,
            adminNaf_id=admin.id
        )
        db.add(novo_horario)
        db.commit()
        db.refresh(novo_horario)
        
        return novo_horario
    except HTTPException as e:
        raise e
    except Exception as e:
        handle_database_error(db, e)

# Função para deletar uma data de agendamento por id 
@router.delete("/agenda/{agenda_id}", status_code=200)
async def deletar_agendamento(agenda_id: int, db: Session = Depends(get_db)):
    agendamento = db.query(Agenda).filter(Agenda.id == agenda_id).first()
    
    if not agendamento:
        # Lançando a exceção que será tratada no error_handlers.py
        raise HTTPException(status_code=404, detail=f"Agendamento com ID {agenda_id} não encontrado no Banco de Dados.")

    # Remove o usuário
    db.delete(agendamento)
    db.commit()
    
    # Retorna apenas uma mensagem de sucesso
    return {"message": f"Agendamento com ID {agenda_id} deletado com sucesso do Banco de Dados!"}

# Função para marcar agendamento de acordo agenda
@router.post("/agendamento/", response_model=AgendamentoResposta)
def criar_agendamento(agenda: AgendamentoCriar, db: Session = Depends(get_db), usuario_id: int = Depends(get_usuario_id)):
    try:
        # Verificar se o horário existe
        horario = db.query(Agenda).filter(
            Agenda.ano == agenda.ano,
            Agenda.mes == agenda.mes,
            Agenda.dia == agenda.dia,
            Agenda.hora == agenda.hora,
            Agenda.turno == agenda.turno
        ).first()

        if not horario:
            raise HTTPException(status_code=422, detail="Horário não encontrado para agendamento.")

        if not horario.status:
            raise HTTPException(status_code=422, detail="Horário já se encontra ocupado.")

        # Atualizar o horário
        horario.status = False
        horario.usuario_id = usuario_id  # Setar o ID do usuário identificado
        horario.data_agendamento = datetime.utcnow()

        db.commit()
        db.refresh(horario)

        return horario  # Retorno da resposta no modelo

    except HTTPException as e:
        raise e
    except Exception as e:
        handle_database_error(db, e)
