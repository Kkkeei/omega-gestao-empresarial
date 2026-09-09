import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import criar_tabelas
from app.api.v1.routes import router as api_router
from app.services.sincronizacao_inicial import sincronizar_todas_ao_iniciar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("omega")


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()

    # Inicia a sincronização sem bloquear a subida da API.
    # Ao executar/reiniciar o backend, todas as empresas ativas são sincronizadas.
    tarefa_sync = asyncio.create_task(sincronizar_todas_ao_iniciar())
    app.state.sincronizacao_inicial = tarefa_sync

    try:
        yield
    finally:
        if not tarefa_sync.done():
            tarefa_sync.cancel()
            try:
                await tarefa_sync
            except asyncio.CancelledError:
                pass


app = FastAPI(
    title="ÔMEGA - Gestão Empresarial",
    version="1.0.0",
    description="Backend MVP da Plataforma ÔMEGA de Gestão Empresarial.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok", "sistema": "ÔMEGA"}


@app.get("/", tags=["Sistema"])
def raiz():
    return {"sistema": "ÔMEGA - Gestão Empresarial", "status": "online", "versao": "1.0.0"}


app.include_router(api_router)
