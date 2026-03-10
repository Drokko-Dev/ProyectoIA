from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

from services.ia_services import IAService # Importamos el servicio de IA (nuestro)

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


app.mount("/archivos", StaticFiles(directory="/data_storage"), name="archivos")


@app.get("/")
def read_root():
    return {"message": "Hola desde el Backend en FastAPI!"}

@app.get("/home")
def home():
    return {"message": "API Conectada"}

class ScriptRequest(BaseModel):
    prompt: str

@app.post("/api/generate-script-voice")
async def generate_script_voice(request: ScriptRequest):
    try:
        answer = await ia_service.generate_script_voice(request.prompt)
        return {"response": answer}
    except Exception as e:
        print(f"Error detectado: {e}")
        raise HTTPException(status_code=500, detail="Error procesando la IA")

@app.post("/api/generate-voice")
async def generate_voice(request: ScriptRequest):
    try:        
        # 2. La IA lee ese texto y genera el MP3
        resultado_final = await ia_service.generate_voice(request.prompt)
        
        # 3. Devolvemos el diccionario con ambas cosas
        return {"response": resultado_final}
    except Exception as e:
        print(f"Error detectado: {e}")
        raise HTTPException(status_code=500, detail="Error procesando la IA")