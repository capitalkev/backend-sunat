from src.domain.interfaces import SunatInterface
from src.domain.models import User


class GetMetricas:
    def __init__(self, repository: SunatInterface):
        self.repository = repository

    def execute(self, current_user: User, filtros):
        usuario_emails = filtros.usuario_emails

        if not current_user.is_admin():
            usuario_emails = [current_user.email]

        return self.repository.get_metricas_resumen(
            ruc_empresa=filtros.rucs_empresa,
            fecha_inicio=filtros.fecha_desde,
            fecha_fin=filtros.fecha_hasta,
            monedas=filtros.monedas,
            usuario_emails=usuario_emails,
        )
