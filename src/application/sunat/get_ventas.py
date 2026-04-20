from typing import Any

from capitalexpress_auth import User

from src.domain.interfaces import SunatInterface
from src.interfaces.dto.sunat_dto import FiltrosSunatParams, PaginacionParams


class GetVentas:
    def __init__(self, repository: SunatInterface) -> None:
        self.repository = repository

    def execute(
        self,
        user_session: User,
        filtros: FiltrosSunatParams,
        paginacion: PaginacionParams,
    ) -> dict[str, Any]:

        usuario_emails = filtros.usuario_emails
        if not user_session.is_admin():
            usuario_emails = [user_session.email]

        return self.repository.get_ventas_sunat(
            ruc_empresa=filtros.rucs_empresa,
            fecha_inicio=filtros.fecha_desde,
            fecha_fin=filtros.fecha_hasta,
            monedas=filtros.monedas,
            usuario_emails=usuario_emails,
            page=paginacion.page,
            page_size=paginacion.page_size,
            sort_by=paginacion.sort_by,
        )
