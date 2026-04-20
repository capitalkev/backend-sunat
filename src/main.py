import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.interfaces.router import sunat

load_dotenv()

CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS")


def _parse_cors_allow_origins(raw: str | None) -> list[str]:
    if raw is None:
        return []
    raw = raw.strip()
    if not raw:
        return []
    if raw.startswith("["):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, list) and all(isinstance(item, str) for item in parsed):
            return parsed
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


def create_application() -> FastAPI:
    """
    Punto de entrada exclusivo para el Microservicio SUNAT.
    """
    application = FastAPI(
        title="API SUNAT - Capital Express",
        description="Microservicio dedicado a la integración y visualización de ventas SUNAT.",
        version="1.0.0",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=_parse_cors_allow_origins(CORS_ALLOW_ORIGINS),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(sunat.router)

    return application


app = create_application()
