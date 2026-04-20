from fastapi import Query


class FiltrosSunatParams:
    def __init__(
        self,
        fecha_desde: str | None = Query(None),
        fecha_hasta: str | None = Query(None),
        moneda: list[str] | None = Query(None, alias="monedas"),
        rucs_empresa: list[str] | None = Query(None),
        usuario_emails: list[str] | None = Query(None),
    ):
        self.fecha_desde = fecha_desde
        self.fecha_hasta = fecha_hasta
        self.monedas = moneda
        self.rucs_empresa = rucs_empresa
        self.usuario_emails = usuario_emails


class PaginacionParams:
    def __init__(
        self,
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1),
        sort_by: str = Query("fecha"),
    ):
        self.page = page
        self.page_size = page_size
        self.sort_by = sort_by
