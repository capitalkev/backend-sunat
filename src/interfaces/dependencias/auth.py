from fastapi import Depends, Header, HTTPException
from firebase_admin import auth
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.domain.models import User
from src.infrastructure.postgresql.connection_sunat import get_db


def get_current_user(
    authorization: str = Header(None), db: Session = Depends(get_db)
) -> User:
    if not authorization:
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    token = authorization.replace("Bearer ", "")

    try:
        # 1. Firebase verifica que el token sea criptográficamente válido
        decoded_token = auth.verify_id_token(token)
        email = decoded_token.get("email")

        # 2. Consultas rápidamente tu BD compartida para saber su rol
        sql = "SELECT email, nombre, rol FROM usuarios WHERE email = :email"
        result = db.execute(text(sql), {"email": email}).fetchone()

        if not result:
            raise HTTPException(
                status_code=401, detail="Usuario no registrado en la BD"
            )

        # 3. Retornas el usuario
        return User(
            email=result._mapping["email"],
            nombre=result._mapping["nombre"],
            rol=result._mapping["rol"],
        )

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e!s}")


def require_roles(allowed_roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.rol not in allowed_roles:
            raise HTTPException(status_code=403, detail="Permisos insuficientes")
        return current_user

    return role_checker
