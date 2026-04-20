from typing import Any, Protocol


class SunatInterface(Protocol):
    def get_ventas_sunat(
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
    ) -> dict[str, Any]: ...

    def get_empresas(
        self, usuario_emails: list[str] | None
    ) -> list[dict[str, str]]: ...
