import sys
import os

# Agrega el directorio `src` al PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers import auth_router, patients_router, doctors_router, appointments_router, users_router, dashboard_router
from integrations.twilio_webhook import twilio_router  # Importar el webhook de Twilio
from utils.openapi_tags import openapi_tags

app = FastAPI(
    title="Mi Embarazo",
    summary="API para el control de embarazos",
    version="1.0.0",
    openapi_tags=openapi_tags,
)

# Incluir routers existentes
app.include_router(auth_router, tags=["auth"])
app.include_router(patients_router, tags=["patients"])
app.include_router(doctors_router, tags=["doctors"])
app.include_router(appointments_router, tags=["appointments"])
app.include_router(twilio_router, tags=["twilio"])  # Incluir el router del webhook de Twilio
app.include_router(users_router, tags=["users"])
app.include_router(dashboard_router, tags=["dashboard"])

@app.get("/")
def read_root():
    return {
        "Mi Embarazo": "API para el control de embarazos",
    }

# Configurar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
