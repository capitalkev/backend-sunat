from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.domain.interfaces import SunatInterface


class OperacionesRepository(SunatInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_ventas_sunat(
        self,
        ruc_empresa: list[str] | None,
        fecha_inicio: str | None,
        fecha_fin: str | None,
        monedas: list[str] | None,
        usuario_emails: list[str] | None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "fecha",
    ) -> dict[str, Any]:
        base_query = """
            FROM ventas_sunat f
            JOIN enrolados en ON f.ruc = en.ruc
            LEFT JOIN ventas_sunat nc
                ON f.ruc = nc.ruc
                AND f.nro_cp_doc = nc.nro_cp_modificado
                AND f.serie_cdp = nc.serie_cp_modificado
                AND nc.tipo_cp_doc = '07'
            WHERE f.tipo_cp_doc = '01'
        """

        params = {}
        filters_query = ""

        # Filtros
        if usuario_emails:
            p_emails = ", ".join([f":email_{i}" for i in range(len(usuario_emails))])
            filters_query += f" AND en.email IN ({p_emails})"
            for i, email in enumerate(usuario_emails):
                params[f"email_{i}"] = email

        if ruc_empresa:
            p_rucs = ", ".join([f":ruc_{i}" for i in range(len(ruc_empresa))])
            filters_query += f" AND f.ruc IN ({p_rucs})"
            for i, ruc in enumerate(ruc_empresa):
                params[f"ruc_{i}"] = ruc

        if fecha_inicio and fecha_fin:
            filters_query += " AND f.fecha_emision BETWEEN :inicio AND :fin"
            params["inicio"] = fecha_inicio
            params["fin"] = fecha_fin

        if monedas:
            p_monedas = ", ".join([f":moneda_{i}" for i in range(len(monedas))])
            filters_query += f" AND f.moneda IN ({p_monedas})"
            for i, mon in enumerate(monedas):
                params[f"moneda_{i}"] = mon

        # Query para el total de items (Paginación)
        count_query = f"SELECT COUNT(*) {base_query} {filters_query}"
        total_items = self.db.execute(text(count_query), params).scalar()

        # Query principal para los datos (SIN estado1 y estado2)
        select_clause = """
            SELECT
                f.ruc, f.razon_social, f.moneda,
                f.serie_cdp, f.nro_cp_doc, f.periodo, f.fecha_emision,
                f.cliente_razon_social,
                f.total_cp AS total_factura,
                COALESCE(nc.total_cp, 0) AS total_nota_credito,
                (f.total_cp + COALESCE(nc.total_cp, 0)) AS monto_neto,
                CASE WHEN nc.total_cp IS NOT NULL THEN true ELSE false END as tiene_nota_credito
        """

        # Paginación
        offset = (page - 1) * page_size
        pagination_clause = " ORDER BY f.fecha_emision DESC LIMIT :limit OFFSET :offset"
        params["limit"] = page_size
        params["offset"] = offset

        data_query = f"{select_clause} {base_query} {filters_query} {pagination_clause}"
        result = self.db.execute(text(data_query), params)

        items = [dict(row) for row in result.mappings()]
        total_pages = (total_items + page_size - 1) // page_size

        return {
            "items": items,
            "pagination": {
                "page": page,
                "total_pages": total_pages,
                "total_items": total_items,
                "has_next": page < total_pages,
                "has_previous": page > 1,
            },
        }

    def get_metricas_resumen(
        self,
        ruc_empresa: list[str] | None = None,
        fecha_inicio: str | None = None,
        fecha_fin: str | None = None,
        monedas: list[str] | None = None,
        usuario_emails: list[str] | None = None,
    ) -> dict[str, Any]:

        # Query limpio sin la lógica de "estado"
        query_str = """
                SELECT
                    f.moneda,
                    COUNT(f.*) as cantidad,
                    SUM(f.total_cp + COALESCE(nc.total_cp, 0)) as total_facturado
                FROM ventas_sunat f
                JOIN enrolados en ON f.ruc = en.ruc
                LEFT JOIN ventas_sunat nc
                    ON f.ruc = nc.ruc
                    AND f.nro_cp_doc = nc.nro_cp_modificado
                    AND f.serie_cdp = nc.serie_cp_modificado
                    AND nc.tipo_cp_doc = '07'
                WHERE f.tipo_cp_doc = '01'
            """

        params = {}
        # Filtros para métricas
        if usuario_emails:
            p_emails = ", ".join([f":email_{i}" for i in range(len(usuario_emails))])
            query_str += f" AND en.email IN ({p_emails})"
            for i, email in enumerate(usuario_emails):
                params[f"email_{i}"] = email

        if ruc_empresa:
            p_rucs = ", ".join([f":ruc_{i}" for i in range(len(ruc_empresa))])
            query_str += f" AND f.ruc IN ({p_rucs})"
            for i, ruc in enumerate(ruc_empresa):
                params[f"ruc_{i}"] = ruc

        if fecha_inicio and fecha_fin:
            query_str += " AND f.fecha_emision BETWEEN :inicio AND :fin"
            params["inicio"] = fecha_inicio
            params["fin"] = fecha_fin

        if monedas:
            p_monedas = ", ".join([f":moneda_{i}" for i in range(len(monedas))])
            query_str += f" AND f.moneda IN ({p_monedas})"
            for i, mon in enumerate(monedas):
                params[f"moneda_{i}"] = mon

        query_str += " GROUP BY f.moneda"

        result = self.db.execute(text(query_str), params)

        metricas = {
            "PEN": {"totalFacturado": 0, "cantidad": 0},
            "USD": {"totalFacturado": 0, "cantidad": 0},
        }

        for row in result.mappings():
            moneda = row["moneda"]
            if moneda in metricas:
                metricas[moneda] = {
                    "totalFacturado": float(row["total_facturado"] or 0),
                    "cantidad": row["cantidad"],
                }

        return metricas

    def get_empresas(
        self, usuario_emails: list[str] | None = None
    ) -> list[dict[str, str]]:
        query_str = """
            SELECT DISTINCT f.ruc, f.razon_social
            FROM ventas_sunat f
            JOIN enrolados en ON f.ruc = en.ruc
            WHERE 1=1
        """
        params = {}
        if usuario_emails:
            p_emails = ", ".join([f":email_{i}" for i in range(len(usuario_emails))])
            query_str += f" AND en.email IN ({p_emails})"
            for i, email in enumerate(usuario_emails):
                params[f"email_{i}"] = email

        result = self.db.execute(text(query_str), params)
        return [
            {"ruc": row["ruc"], "razon_social": row["razon_social"]}
            for row in result.mappings()
        ]
