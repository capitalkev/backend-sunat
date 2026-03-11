from src.domain.interfaces import SunatInterface


class UpdateEstadoVenta:
    def __init__(self, repository: SunatInterface):
        self.repository = repository

    def execute(self, venta_id: str, nuevo_estado: str) -> bool:
        return self.repository.update_venta_estado(venta_id, nuevo_estado)
