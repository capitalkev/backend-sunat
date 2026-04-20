from capitalexpress_auth import User
from fastapi import APIRouter, Depends, Query

from src.application.sunat.get_empresas import GetEmpresas
from src.application.sunat.get_metricas import GetMetricas
from src.application.sunat.get_ventas import GetVentas
from src.interfaces.dependencias.auth import require_roles
from src.interfaces.dependencias.sunat import (
    dp_get_empresas,
    dp_get_metricas,
    dp_get_ventas,
)
from src.interfaces.dto.sunat_dto import (
    FiltrosSunatParams,
    PaginacionParams,
)

router = APIRouter(prefix="/api", tags=["Sunat"])


@router.get("/ventas")
def get_ventas(
    filtros: FiltrosSunatParams = Depends(),
    paginacion: PaginacionParams = Depends(),
    action: GetVentas = Depends(dp_get_ventas),
    user: User = Depends(require_roles(["admin", "ventas"])),
):
    return action.execute(user_session=user, filtros=filtros, paginacion=paginacion)


@router.get("/metricas/resumen")
def get_metricas(
    filtros: FiltrosSunatParams = Depends(),
    action: GetMetricas = Depends(dp_get_metricas),
    user: User = Depends(require_roles(["admin", "ventas"])),
):
    return action.execute(current_user=user, filtros=filtros)


@router.get("/ventas/empresas")
def get_empresas(
    usuario_emails: list[str] | None = Query(
        None
    ),
    action: GetEmpresas = Depends(dp_get_empresas),
    user: User = Depends(require_roles(["admin", "ventas"])),
):
    return action.execute(current_user=user, usuario_emails=usuario_emails)
