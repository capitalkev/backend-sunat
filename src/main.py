from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Asumo que mantienes tu inicializador de firebase en infrastructure
from src.infrastructure.auth.firebase_init import initialize_firebase
from src.interfaces.router import sunat


def create_application() -> FastAPI:
    """
    Punto de entrada exclusivo para el Microservicio SUNAT.
    """
    application = FastAPI(
        title="API SUNAT - Capital Express",
        description="Microservicio dedicado a la integración y visualización de ventas SUNAT.",
        version="1.0.0",
    )

    # Inicializar Firebase para poder validar los tokens que envía el frontend
    initialize_firebase()

    # Orígenes permitidos (tu frontend local y en producción)
    origins = [
        "https://operaciones-capitalexpress.web.app",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Registramos ÚNICAMENTE el router de SUNAT
    application.include_router(sunat.router)

    # Endpoint de salud para Cloud Run / Infraestructura
    @application.get("/health", tags=["Health"])
    def health_check():
        return {"status": "ok", "service": "sunat-microservice"}

    return application


app = create_application()
