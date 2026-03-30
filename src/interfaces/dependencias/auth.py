from typing import Callable

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

    # 1. Validar el token con Firebase independientemente
    try:
        decoded_token = auth.verify_id_token(token)
        email = decoded_token.get("email")
    except Exception as e:
        print(f"🔴 ERROR FIREBASE: {e}")
        raise HTTPException(
            status_code=401, detail="Token de Firebase inválido o expirado"
        )

    # 2. Consultar el usuario en PostgreSQL
    try:
        # Quitamos la columna 'nombre' porque no existe
        sql = "SELECT email, rol FROM usuarios WHERE email = :email"
        result = db.execute(text(sql), {"email": email}).fetchone()

        if not result:
            print(
                f"🟡 AVISO: El correo {email} entró por Firebase pero no existe en PostgreSQL"
            )
            raise HTTPException(
                status_code=401, detail="Usuario no registrado en la BD"
            )

        return User(
            email=result._mapping["email"],
            nombre=result._mapping[
                "email"
            ],  # Usamos el email para rellenar el campo nombre requerido
            rol=result._mapping["rol"],
        )

    except HTTPException:
        # Dejar pasar el error 401 de "Usuario no registrado"
        raise
    except Exception as e:
        print(f"🔴 ERROR BASE DE DATOS (Auth): {e}")
        raise HTTPException(
            status_code=500, detail="Error interno verificando usuario en BD"
        )


def require_roles(allowed_roles: list[str]) -> Callable[[User], User]:
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.rol not in allowed_roles:
            raise HTTPException(status_code=403, detail="Permisos insuficientes")
        return current_user

    return role_checker
