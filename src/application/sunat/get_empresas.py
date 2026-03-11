from src.domain.interfaces import SunatInterface
from src.domain.models import User


class GetEmpresas:
    def __init__(self, repository: SunatInterface):
        self.repository = repository

    def execute(self, current_user: User, usuario_emails: list[str] = None):
        if not current_user.is_admin():
            usuario_emails = [current_user.email]

        return self.repository.get_empresas(usuario_emails)
