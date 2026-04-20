from capitalexpress_auth import User
from fastapi import APIRouter, Depends, HTTPException, Path

from src.application.sunat.get_empresas import GetEmpresas
from src.application.sunat.get_metricas import GetMetricas
from src.application.sunat.get_usuarios import GetUsuarios
from src.application.sunat.get_ventas import GetVentas
from src.application.sunat.update_estado import UpdateEstadoVenta
from src.interfaces.dependencias.auth import get_current_user, require_roles
from src.interfaces.dependencias.sunat import (
    dp_get_empresas,
    dp_get_metricas,
    dp_get_usuarios,
    dp_get_ventas,
    dp_update_estado,
)
from src.interfaces.dto.sunat_dto import (
    FiltrosSunatParams,
    PaginacionParams,
    UpdateEstadoRequest,
)

router = APIRouter(prefix="/api", tags=["Sunat"])


@router.get("/ventas")
def get_ventas(
    filtros: FiltrosSunatParams = Depends(),
    paginacion: PaginacionParams = Depends(),
    action: GetVentas = Depends(dp_get_ventas),
    user: User = Depends(require_roles(["admin", "ventas"])),
):
    return action.execute(
        user_session=user, filtros=filtros, paginacion=paginacion
    )


@router.get("/metricas/resumen")
def get_metricas(
    filtros: FiltrosSunatParams = Depends(),
    action: GetMetricas = Depends(dp_get_metricas),
    user: User = Depends(require_roles(["admin", "ventas"])),
):
    return action.execute(current_user=user, filtros=filtros)



@router.put("/ventas/{venta_id}/estado")
def update_venta_estado(
    venta_id: str = Path(...),
    payload: UpdateEstadoRequest = Depends(),
    action: UpdateEstadoVenta = Depends(dp_update_estado),
    user: User = Depends(require_roles(["admin", "ventas"])),
    current_user: User = Depends(get_current_user),
):
    actualizado = action.execute(venta_id, payload.estado1)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    return {"message": "Estado actualizado correctamente"}


@router.get("/ventas/empresas")
def get_empresas(
    usuario_emails: list[str] | None = None,
    action: GetEmpresas = Depends(dp_get_empresas),
    user: User = Depends(require_roles(["admin", "ventas"])),
):
    return action.execute(current_user=user, usuario_emails=usuario_emails)


@router.get("/usuarios/no-admin")
def get_usuarios(
    action: GetUsuarios = Depends(dp_get_usuarios),
    user: User = Depends(require_roles(["admin", "ventas"])),
):
    return action.execute(current_user=user)
