from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers import auth_router, patients_router, doctors_router, appointments_router

from utils.openapi_tags import openapi_tags

app = FastAPI(
    title= "Mi Embarazo",
    summary="API para el control de embarazos",
    version="1.0.0",
    openapi_tags=openapi_tags
)

app.include_router(auth_router, tags=["auth"])
app.include_router(patients_router, tags=["patients"])
app.include_router(doctors_router, tags=["doctors"])
app.include_router(appointments_router, tags=["appointments"])

@app.get("/")
def read_root():
    return {
        "Mi Embarazo": "API para el control de embarazos",
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)