from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.ia_services import IAService 
from pydantic import BaseModel

app = FastAPI()
ia_service = IAService()

# 2. Definimos quiénes pueden entrar (Lista de invitados)
origins = [
    "http://localhost:5173", # Tu React en desarrollo
    "http://127.0.0.1:5173",
    # "https://mi-dominio-pro.com", # Aquí iría tu web en el futuro
]

# 3. Aplicamos el middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Solo estos sitios entran
    allow_credentials=True,           # ¿Permitir cookies/sesiones?
    allow_methods=["*"],              # ¿Pueden hacer GET, POST, DELETE? (Todos)
    allow_headers=["*"],              # ¿Pueden enviar cualquier cabecera? (Sí)
)

# 4. Definimos el modelo de datos para la solicitud (opcional pero recomendado)
class ScriptRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "Hola desde el Backend en FastAPI!"}

@app.get("/home")
def home():
    return {"message": "API Conectada"}

@app.post("/api/generate-script")
async def generate_script(request: ScriptRequest):
    try:
        # Usamos el servicio en lugar de escribir toda la lógica aquí
        answer = await ia_service.get_chat_response(request.prompt)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error procesando la IA")