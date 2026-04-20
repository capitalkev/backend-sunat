from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.sunat.get_empresas import GetEmpresas
from src.application.sunat.get_metricas import GetMetricas
from src.application.sunat.get_ventas import GetVentas
from src.infrastructure.postgresql.connection_sunat import get_db
from src.infrastructure.postgresql.repositories_sunat.sunat import OperacionesRepository

DBSession = Annotated[Session, Depends(get_db)]


def dp_get_ventas(db: DBSession) -> GetVentas:
    return GetVentas(OperacionesRepository(db))


def dp_get_metricas(db: DBSession) -> GetMetricas:
    return GetMetricas(OperacionesRepository(db))


def dp_get_empresas(db: DBSession) -> GetEmpresas:
    return GetEmpresas(OperacionesRepository(db))
