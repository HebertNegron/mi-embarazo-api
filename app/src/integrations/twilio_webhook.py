from bson import ObjectId
from fastapi import APIRouter, Request, HTTPException, Response
from twilio.twiml.messaging_response import MessagingResponse
from pydantic import BaseModel
import logging
import unicodedata  # Para normalizar acentos
from utils.mongo_conn import MongoConnection
from services.doctors_service import DoctorsService
from services.patients_service import PatientsService  # Importar el servicio de pacientes
from datetime import datetime

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


        with MongoConnection() as db:
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
                    db.patients.insert_one({"personalData": {"name": user_message.title()}, "current_phone": form_data["From"]})
                    conversation_state[user_number]["step"] = "registrar_telefono"
                    reply = "Gracias. Ahora, por favor envía tu número de celular."
                elif current_step == "registrar_telefono":
                    # Guardar el número de celular proporcionado
                    conversation_state[user_number]["telefono"] = user_message
                    db.patients.update_one({"current_phone": form_data["From"]},{"$set": {"personalData.phone": user_message}})
                    conversation_state[user_number]["step"] = "seleccionar_doctor"
                    doctors = list(db.users.find({"role": "doctor"}))
                    doctor_options = [f"{idx}. {x['name']}" for idx, x in enumerate(doctors, start=1)]
                    reply = ("Perfecto, ya estás registrado. Ahora continuemos con el agendado de tu cita.\n"
                            "Estos son los doctores disponibles:\n"
                            f"{', '.join(doctor_options)}\n"
                            "Por favor, responde con el número del doctor que deseas.")
                    doctor_options_with_id = [f"{idx}. {x['_id']}" for idx, x in enumerate(doctors, start=1)]
                    db.patients.update_one({"current_phone": form_data["From"]},{"$set": {"doctors_options": doctor_options_with_id}})
                elif current_step == "pedir_numero":
                    try:
                        # Buscar al paciente en la base de datos usando el servicio
                        patient = patients_service.get_patient_by_phone(user_message)
                        db.patients.update_one({"personalData.phone": user_message},{"$set": {"current_phone": form_data["From"]}})
                        if patient:
                            conversation_state[user_number]["patient"] = patient  # Guardar el paciente en el estado
                            conversation_state[user_number]["step"] = "seleccionar_doctor"  # Avanzar al siguiente paso
                            doctors = list(db.users.find({"role": "doctor"}, {"_id": 1, "name": 1}))
                            doctor_options = [f"{idx}. {x['name']}" for idx, x in enumerate(doctors, start=1)]
                            reply = (f"Gracias {patient['personalData']['name']}. Ahora podemos continuar con el agendado de tu cita.\n"
                                    "Estos son los doctores disponibles:\n"
                                    f"{'\n'.join(doctor_options)}\n"
                                    "Por favor, responde con el número del doctor que deseas.")
                            doctor_options_with_id = [f"{idx}. {x['_id']}" for idx, x in enumerate(doctors, start=1)]
                            db.patients.update_one({"current_phone": form_data["From"]},{"$set": {"doctors_options": doctor_options_with_id}})
                        else:
                            reply = "No encontramos tu registro. Por favor, verifica el número o ID enviado."
                    except Exception as e:
                        logger.error(f"Error buscando al paciente: {e}")
                        reply = "Hubo un error al buscar tu registro. Intenta nuevamente más tarde."
                elif current_step == "seleccionar_doctor":
                    if user_message.isdigit():
                        try:
                            doctor = list(db.patients.aggregate([
                                {"$match": {"current_phone": form_data["From"]}},
                                {"$project": {"_id": 0, "doctors_options": 1}},
                                {"$unwind": "$doctors_options"},
                                {"$match": {"doctors_options": {"$regex": f"^{user_message}"}}},
                                {"$project": {"_id": 0, "doctors_options": 1}},
                                {"$unwind": "$doctors_options"},
                                {"$limit": 1}
                            ]))
                            doctor = doctor[0]['doctors_options'][3:]
                            db.patients.update_one({"current_phone": form_data["From"]},{"$set": {"doctor": doctor}})
                        except Exception as e:
                            logger.error(f"Error buscando al paciente: {e}")
                            reply = "Opción no encontrada."
                        doctor = user_message
                        conversation_state[user_number]["doctor"] = doctor
                        conversation_state[user_number]["step"] = "seleccionar_fecha"
                        reply = f"Has seleccionado al {doctor}. Por favor, envía la fecha deseada en formato DD-MM-AAAA."
                    else:
                        reply = "Por favor, responde con el número del doctor."
                elif current_step == "seleccionar_fecha":
                    try:
                        parsed_date = datetime.strptime(user_message, "%d-%m-%Y")
                        if parsed_date < datetime.now():
                            raise ValueError
                        db.patients.update_one({"current_phone": form_data["From"]},{"$set": {"date": parsed_date}})
                    except ValueError:
                        reply = "Por favor, envía la fecha deseada en formato DD-MM-AAAA."
                    conversation_state[user_number]["fecha"] = user_message
                    conversation_state[user_number]["step"] = "seleccionar_horario"
                    appointment_chat = db.patients.find_one({"current_phone": form_data["From"]})
                    if appointment_chat:
                        doctor_schedule = DoctorsService().get_schedule(appointment_chat["doctor"], user_message)
                        reply = ("Gracias. Estos son los horarios disponibles:\n"
                            f"{'\n'.join([f"{idx}. {x}" for idx, x in enumerate(doctor_schedule, start=1)])}\n"
                            "Por favor, responde con el número del horario que prefieres.")
                        db.patients.update_one({"current_phone": form_data["From"]},{"$set": {"horarios_options": [
                            f"{idx}. {x}" for idx, x in enumerate(doctor_schedule, start=1)
                        ]}})
                    else:
                        reply = "No encontramos tu registro. Por favor, verifica el número o ID enviado."
                elif current_step == "seleccionar_horario":
                    if user_message.isdigit():
                        horario = list(db.patients.aggregate([
                            {"$match": {"current_phone": form_data["From"]}},
                            {"$project": {"_id": 0, "horarios_options": 1}},
                            {"$unwind": "$horarios_options"},
                            {"$match": {"horarios_options": {"$regex": f"^{user_message}"}}},
                            {"$project": {"_id": 0, "horarios_options": 1}},
                            {"$unwind": "$horarios_options"}
                        ]))
                        horario = horario[0]['horarios_options'][3:]
                        patient = db.patients.find_one({"current_phone": form_data["From"]})
                        conversation_state[user_number]["horario"] = horario
                        if patient:
                            db.appointments.insert_one({
                                "patient": ObjectId(patient["_id"]),
                                "file": None,
                                "doctor": ObjectId(patient["doctor"]),
                                "date": patient["date"],
                                "time": horario,
                                "date_type": "presencial",
                                "status": "pending"
                            })
                            db.patients.update_one({"current_phone": form_data["From"]},{"$set": {'doctors_options': [], 'horarios_options': [], 'current_phone': None, 'doctor': None, 'date': None}})
                            reply = f"Tu cita ha sido registrada para el {conversation_state[user_number]['fecha']} a las {horario} con {conversation_state[user_number]['doctor']}. ¡Gracias!"
                            del conversation_state[user_number]
                        else:
                            reply = "No pudimos agendar tu cita. Por favor, verifica el número o ID enviado."
                    else:
                        reply = "Por favor, responde con el número del horario."
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
