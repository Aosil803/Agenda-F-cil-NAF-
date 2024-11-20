import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from back_end.models.adminNaf_models import AdminNaf
from back_end.create_db import get_db
from back_end.dtos.adminNaf_dtos import AdminNafBase, AdminNafCriar

# Configurar logs para exibir erros 
logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Defina o router
router = APIRouter()

# Função para retornar todos os administradores Naf
@router.get("/AdminNaf/", response_model=list[AdminNafBase])
async def get_usuarios(db: Session = Depends(get_db)):
    try:
        adminNaf = db.query(AdminNaf).all()  
        if not adminNaf:
            raise HTTPException(status_code=404, detail="Nenhum usuário encontrado.")
        return adminNaf
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro {str(e)}")
    
    
# Função para criar um novo administrador NAF
@router.post("/AdminNaf/", response_model=AdminNafBase)
async def criar_admin_naf(adminNaf: AdminNafCriar, db: Session = Depends(get_db)):
    try:
        # Verificar se a matrícula já existe
        matricula_existente = db.query(AdminNaf).filter(AdminNaf.matricula == adminNaf.matricula).first()
        if matricula_existente:
            raise HTTPException(status_code=400, detail="Matrícula já cadastrada.")

        # Criar novo administrador
        novo_admin = AdminNaf(
            nome=adminNaf.nome,
            matricula=adminNaf.matricula,
            email=adminNaf.email,
            senha=adminNaf.senha,
            perfil=adminNaf.perfil,
        )

        # Adiciona ao banco de dados
        db.add(novo_admin)
        db.commit()
        db.refresh(novo_admin)  # Atualiza o objeto com os dados salvos

        logger.info(f"Novo administrador criado com sucesso: ID {novo_admin.id}")
        return novo_admin

    except Exception as e:
        db.rollback()  # Reverte a transação em caso de erro
        logger.error(f"Erro ao criar administrador: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao criar administrador: {str(e)}")


# Função para atualizar um administrador por ID
@router.put("/AdminNaf/{adminNaf_id}", response_model=AdminNafBase)
async def atualizar_admin_naf(adminNaf_id: int, adminNaf: AdminNafCriar, db: Session = Depends(get_db)):
    try:
        # Verificar se o administrador existe
        admin_existente = db.query(AdminNaf).filter(AdminNaf.id == adminNaf_id).first()
        if not admin_existente:
            raise HTTPException(status_code=404, detail="Administrador não encontrado.")

        # Atualizar os dados
        admin_existente.matricula = adminNaf.matricula
        admin_existente.email = adminNaf.email
        admin_existente.senha = adminNaf.senha
        admin_existente.perfil = adminNaf.perfil

        db.commit()
        db.refresh(admin_existente)  # Atualiza o objeto com os dados salvos

        logger.info(f"Administrador ID {adminNaf_id} atualizado com sucesso.")
        return admin_existente

    except Exception as e:
        db.rollback()  # Reverte a transação em caso de erro
        logger.error(f"Erro ao atualizar administrador: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar administrador: {str(e)}")
