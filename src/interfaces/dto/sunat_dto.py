from fastapi import Query
from pydantic import BaseModel


class FiltrosSunatParams:
    """Dependencia para capturar parámetros Query de la URL de forma limpia"""

    def __init__(
        self,
        fecha_desde: str | None = Query(None),
        fecha_hasta: str | None = Query(None),
        moneda: list[str] | None = Query(
            None, alias="monedas"
        ),  # alias por si el frontend manda "monedas"
        rucs_empresa: list[str] | None = Query(None),
        usuario_emails: list[str] | None = Query(None),
    ):
        self.fecha_desde = fecha_desde
        self.fecha_hasta = fecha_hasta
        self.monedas = moneda
        self.rucs_empresa = rucs_empresa
        self.usuario_emails = usuario_emails


class PaginacionParams:
    """Dependencia para capturar la paginación"""

    def __init__(
        self,
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1),
        sort_by: str = Query("fecha"),
    ):
        self.page = page
        self.page_size = page_size
        self.sort_by = sort_by


class UpdateEstadoRequest(BaseModel):
    """Modelo Pydantic para el Body del PUT"""

    estado1: str
