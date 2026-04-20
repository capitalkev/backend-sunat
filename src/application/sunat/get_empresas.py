from capitalexpress_auth import User

from src.domain.interfaces import SunatInterface


class GetEmpresas:
    def __init__(self, repository: SunatInterface) -> None:
        self.repository = repository

    def execute(
        self, current_user: User, usuario_emails: list[str] | None = None
    ) -> list[dict[str, str]]:
        if not current_user.is_admin():
            usuario_emails = [current_user.email]

        return self.repository.get_empresas(usuario_emails)
