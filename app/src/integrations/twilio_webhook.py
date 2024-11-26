from fastapi import APIRouter, Request, HTTPException, Response
from twilio.twiml.messaging_response import MessagingResponse
from pydantic import BaseModel
import logging
import unicodedata  # Para normalizar acentos
from services.patients_service import PatientsService  # Importar el servicio de pacientes

# Configurar el logger
logger = logging.getLogger("twilio_webhook")
logger.setLevel(logging.INFO)

# Crear una instancia del servicio de pacientes
patients_service = PatientsService()

# Estado de la conversación
conversation_state = {}

# Crear el router
twilio_router = APIRouter()


class WhatsAppMessage(BaseModel):
    From: str
    Body: str
    To: str

def normalize_message(message: str) -> str:
    """
    Normaliza un mensaje eliminando acentos y convirtiéndolo a minúsculas.
    """
    return unicodedata.normalize("NFKD", message).encode("ascii", "ignore").decode("utf-8").lower()

@twilio_router.post("/webhook")
async def whatsapp_webhook(request: Request):
    """
    Endpoint que Twilio llamará para procesar los mensajes entrantes.
    """
    try:
        form_data = await request.form()
        message = WhatsAppMessage(
            From=form_data["From"],
            Body=normalize_message(form_data["Body"].strip()),
            To=form_data["To"]
        )

        user_number = message.From
        user_message = message.Body

        # Verificar si el usuario ya tiene un estado en la conversación
        if user_number not in conversation_state:
            conversation_state[user_number] = {"step": "inicio"}
            reply = "¡Hola! ¿Deseas agendar una cita? (Responde con 'Sí' o 'No')"
        else:
            current_step = conversation_state[user_number]["step"]

            if current_step == "inicio":
                if user_message in ["sí", "si"]:
                    conversation_state[user_number]["step"] = "primera_vez"
                    reply = "¿Es tu primera vez agendando con nosotros? (Responde con 'Sí' o 'No')"
                elif user_message == "no":
                    reply = "Lo sentimos, este medio solo es para agendar citas."
                    del conversation_state[user_number]  # Reiniciar conversación
                else:
                    reply = "Por favor, responde con 'Sí' o 'No'."
            elif current_step == "primera_vez":
                if user_message in ["sí", "si"]:
                    conversation_state[user_number]["step"] = "registrar_nombre"
                    reply = "Perfecto, por favor envía tu nombre completo."
                elif user_message == "no":
                    conversation_state[user_number]["step"] = "pedir_numero"
                    reply = "Por favor, envía el número de teléfono con el que te registraste."
                else:
                    reply = "Por favor, responde con 'Sí' o 'No'."
            elif current_step == "registrar_nombre":
                # Guardar el nombre proporcionado
                conversation_state[user_number]["nombre"] = user_message.title()
                conversation_state[user_number]["step"] = "registrar_telefono"
                reply = "Gracias. Ahora, por favor envía tu número de celular."
            elif current_step == "registrar_telefono":
                # Guardar el número de celular proporcionado
                conversation_state[user_number]["telefono"] = user_message
                conversation_state[user_number]["step"] = "seleccionar_doctor"
                reply = ("Perfecto, ya estás registrado. Ahora continuemos con el agendado de tu cita.\n"
                         "Estos son los doctores disponibles:\n"
                         "1. Dr. Juan Pérez\n"
                         "2. Dra. Ana López\n"
                         "Por favor, responde con el número del doctor que deseas.")
            elif current_step == "pedir_numero":
                try:
                    # Buscar al paciente en la base de datos usando el servicio
                    patient = patients_service.get_patient(user_message)
                    if patient:
                        nombre = patient.personalData.name  # Usar la notación de atributos
                        conversation_state[user_number]["patient"] = patient  # Guardar el paciente en el estado
                        conversation_state[user_number]["step"] = "seleccionar_doctor"  # Avanzar al siguiente paso
                        reply = (f"Gracias {nombre}. Ahora podemos continuar con el agendado de tu cita.\n"
                                "Estos son los doctores disponibles:\n"
                                "1. Dr. Juan Pérez\n"
                                "2. Dra. Ana López\n"
                                "Por favor, responde con el número del doctor que deseas.")
                    else:
                        reply = "No encontramos tu registro. Por favor, verifica el número o ID enviado."
                except Exception as e:
                    logger.error(f"Error buscando al paciente: {e}")
                    reply = "Hubo un error al buscar tu registro. Intenta nuevamente más tarde."
            elif current_step == "seleccionar_doctor":
                if user_message in ["1", "2"]:
                    doctor = "Dr. Juan Pérez" if user_message == "1" else "Dra. Ana López"
                    conversation_state[user_number]["doctor"] = doctor
                    conversation_state[user_number]["step"] = "seleccionar_fecha"
                    reply = f"Has seleccionado al {doctor}. Por favor, envía la fecha deseada en formato DD-MM-AAAA."
                else:
                    reply = "Por favor, responde con el número del doctor (1 o 2)."
            elif current_step == "seleccionar_fecha":
                # Validar formato de la fecha aquí
                conversation_state[user_number]["fecha"] = user_message
                conversation_state[user_number]["step"] = "seleccionar_horario"
                reply = "Gracias. Estos son los horarios disponibles:\n1. 10:00 AM\n2. 3:00 PM\nPor favor, responde con el número del horario que prefieres."
            elif current_step == "seleccionar_horario":
                if user_message in ["1", "2"]:
                    horario = "10:00 AM" if user_message == "1" else "3:00 PM"
                    conversation_state[user_number]["horario"] = horario
                    # Aquí puedes guardar la cita en la base de datos
                    reply = f"Tu cita ha sido registrada para el {conversation_state[user_number]['fecha']} a las {horario} con {conversation_state[user_number]['doctor']}. ¡Gracias!"
                    del conversation_state[user_number]  # Reiniciar conversación
                else:
                    reply = "Por favor, responde con el número del horario (1 o 2)."
            else:
                reply = "Lo siento, no entendí tu mensaje. Por favor, intenta de nuevo."

        # Construir la respuesta TwiML
        response = MessagingResponse()
        response.message(reply)

        # Retornar TwiML como respuesta
        return Response(content=str(response), media_type="application/xml")

    except Exception as e:
        logger.error(f"Error procesando webhook de Twilio: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
