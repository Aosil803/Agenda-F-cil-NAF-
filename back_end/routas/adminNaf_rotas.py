# back_end/routas/adminNaf_rotas.py

from fastapi import APIRouter

# Defina o router
router = APIRouter()

# Adicione algumas rotas de exemplo
@router.get("/admin")
async def admin_dashboard():
    return {"message": "Dashboard do administrador"}

