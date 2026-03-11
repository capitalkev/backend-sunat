from src.infrastructure.postgresql.repositories_sunat.sunat import OperacionesRepository


class SunatUseCases:
    def __init__(self, repo: OperacionesRepository):
        self.repo = repo

    def get_ventas(self, user_session, filters: dict):
        usuario_emails = filters.get("usuario_emails")

        if not user_session.is_admin():
            usuario_emails = [user_session.email]

        return self.repo.get_ventas_sire(
            ruc_empresa=filters.get("rucs_empresa"),
            fecha_inicio=filters.get("fecha_desde"),
            fecha_fin=filters.get("fecha_hasta"),
            monedas=filters.get("monedas"),
            usuario_emails=usuario_emails,
            page=filters.get("page", 1),
            page_size=filters.get("page_size", 20),
            sort_by=filters.get("sort_by", "fecha"),
        )

    def get_metricas(self, user_session, filters: dict):
        usuario_emails = filters.get("usuario_emails")

        # CORRECCIÓN AQUÍ TAMBIÉN
        if not user_session.is_admin():
            usuario_emails = [user_session.email]

        return self.repo.get_metricas_resumen(
            ruc_empresa=filters.get("rucs_empresa"),
            fecha_inicio=filters.get("fecha_desde"),
            fecha_fin=filters.get("fecha_hasta"),
            monedas=filters.get("monedas"),
            usuario_emails=usuario_emails,
        )

    def update_estado(self, venta_id: str, nuevo_estado: str):
        return self.repo.update_venta_estado(venta_id, nuevo_estado)

    def get_empresas(self, user_session, usuario_emails: list = None):
        # CORRECCIÓN AQUÍ TAMBIÉN
        if not user_session.is_admin():
            usuario_emails = [user_session.email]
        return self.repo.get_empresas(usuario_emails)

    def get_usuarios(self, user_session):
        if not user_session.is_admin():
            return []
        return self.repo.get_usuarios_no_admin()
