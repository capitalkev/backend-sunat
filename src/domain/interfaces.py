from typing import Any, Protocol


class SunatInterface(Protocol):
    def get_ventas_sire(
        self,
        ruc_empresa: list[str] | None,
        fecha_inicio: str | None,
        fecha_fin: str | None,
        monedas: list[str] | None,
        usuario_emails: list[str] | None,
        page: int,
        page_size: int,
        sort_by: str,
    ) -> dict[str, Any]: ...

    def get_metricas_resumen(
        self,
        ruc_empresa: list[str] | None,
        fecha_inicio: str | None,
        fecha_fin: str | None,
        monedas: list[str] | None,
        usuario_emails: list[str] | None,
    ) -> dict[str, Any]:
        """Obtiene las métricas KPIs agrupadas por moneda (PEN, USD)"""
        ...

    def update_venta_estado(self, venta_id: str, estado: str) -> bool:
        """Actualiza el estado1 de una factura"""
        ...

    def get_empresas(self, usuario_emails: list[str] | None) -> list[dict[str, str]]:
        """Obtiene la lista de clientes/empresas únicos"""
        ...

    def get_usuarios_no_admin(self) -> list[dict[str, str]]:
        """Obtiene la lista de usuarios para los filtros"""
        ...

    def insert_enrolado(self, ruc: str, data: Any) -> None:
        """Inserta un enrolado en la base de datos"""
        ...
