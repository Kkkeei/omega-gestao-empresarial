from fastapi import APIRouter
from app.api.v1.empresas.routes import router as empresas_router
from app.api.v1.certidoes.routes import router as certidoes_router
from app.api.v1.pendencias.routes import router as pendencias_router
from app.api.v1.automacoes.routes import router as automacoes_router
from app.api.v1.dashboard.routes import router as dashboard_router

router = APIRouter()
router.include_router(empresas_router)
router.include_router(certidoes_router)
router.include_router(pendencias_router)
router.include_router(automacoes_router)
router.include_router(dashboard_router)
