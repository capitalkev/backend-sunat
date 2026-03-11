from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.sunat.get_empresas import GetEmpresas
from src.application.sunat.get_metricas import GetMetricas
from src.application.sunat.get_usuarios import GetUsuarios
from src.application.sunat.get_ventas import GetVentas
from src.application.sunat.update_estado import UpdateEstadoVenta
from src.infrastructure.postgresql.connection_sunat import get_db
from src.infrastructure.postgresql.repositories_sunat.sunat import OperacionesRepository


def dp_get_ventas(db: Session = Depends(get_db)) -> GetVentas:
    return GetVentas(OperacionesRepository(db))


def dp_get_metricas(db: Session = Depends(get_db)) -> GetMetricas:
    return GetMetricas(OperacionesRepository(db))


def dp_update_estado(db: Session = Depends(get_db)) -> UpdateEstadoVenta:
    return UpdateEstadoVenta(OperacionesRepository(db))


def dp_get_empresas(db: Session = Depends(get_db)) -> GetEmpresas:
    return GetEmpresas(OperacionesRepository(db))


def dp_get_usuarios(db: Session = Depends(get_db)) -> GetUsuarios:
    return GetUsuarios(OperacionesRepository(db))
