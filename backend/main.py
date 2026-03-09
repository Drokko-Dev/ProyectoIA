from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

@app.get("/")
def read_root():
    return {"message": "Hola desde el Backend en FastAPI!"}

@app.get("/home")
def home():
    return {"message": "API Conectada"}