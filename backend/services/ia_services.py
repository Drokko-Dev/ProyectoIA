import os
from openai import OpenAI
from dotenv import load_dotenv

from services.FileService import FileService

# Cargamos el .env por si acaso corremos el script fuera de Docker
load_dotenv()

class IAService:
    def __init__(self):
        # Inicializamos el cliente usando la variable de entorno
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # Asegúrate de que esta variable esté en tu .env y en Docker
        self.model = "gpt-4o" # Puedes centralizar el modelo aquí
        self.file_manager = FileService()

    async def generate_script_voice(self, user_prompt: str):
        full_prompt = f"""
        Actúa como un asistente de IA profesional para dentistas que crea contenido para pacientes.
        Descripción Técnica: {user_prompt}
        Prompt: Escribe un guion corto de 15-20 segundos con voz en off que traduzca esta descripción técnica en una explicación atractiva y fácil de entender para el paciente.
        Mantenlo profesional pero accesible. SACA SÓLO el texto hablado, sin acciones, sin títulos, sin emojis o hashtags.
        IMPORTANTE: El guion DEBE estar SIEMPRE en español de Chile (chilenismos moderados, tono cercano pero profesional).
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional dentist AI assistant creating content for patients."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.7, # Un poco de creatividad pero sin volverse loco
                max_tokens=150 # Limitar la respuesta para que sea un guion corto

            )
            script= response.choices[0].message.content
            ruta_final = self.file_manager.save_file(script, file_type="text")
            print(f"Script Generado - Archivo guardado en: {ruta_final}")
            return script
        
        except Exception as e:
            # Aquí podrías manejar errores específicos (falta de crédito, etc.)
            print(f"Error en OpenAI Service: {e}")
            raise e