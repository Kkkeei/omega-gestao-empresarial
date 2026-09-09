import asyncio
import logging

from app.services.empresas_service import listar_empresas, sincronizar_empresa

logger = logging.getLogger("omega.sincronizacao")


async def sincronizar_todas_ao_iniciar(concorrencia: int = 4) -> None:
    """Sincroniza as empresas ativas assim que o backend é iniciado.

    A rotina roda em segundo plano para que a API fique disponível imediatamente.
    Cada empresa é isolada: uma falha não interrompe as demais.
    """
    empresas = listar_empresas(ativo=True)
    if not empresas:
        logger.info("Sincronização inicial: nenhuma empresa ativa encontrada.")
        return

    sem = asyncio.Semaphore(concorrencia)

    async def sincronizar_um(empresa):
        async with sem:
            try:
                _, alteracoes = await sincronizar_empresa(empresa["id"])
                logger.info(
                    "Sincronização inicial concluída: empresa_id=%s alteracoes=%s",
                    empresa["id"],
                    len(alteracoes),
                )
                return True
            except Exception as exc:
                logger.exception(
                    "Falha na sincronização inicial da empresa_id=%s: %s",
                    empresa["id"],
                    exc,
                )
                return False

    resultados = await asyncio.gather(*(sincronizar_um(e) for e in empresas))
    ok = sum(resultados)
    erros = len(resultados) - ok
    logger.info(
        "Sincronização inicial finalizada: total=%s sucesso=%s erros=%s",
        len(resultados),
        ok,
        erros,
    )
