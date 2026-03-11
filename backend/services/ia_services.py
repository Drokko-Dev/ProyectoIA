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
        self.model_text = "gpt-4o" # Puedes centralizar el modelo aquí
        self.model_audio = "tts-1-hd"
        self.file_manager = FileService()
        self.backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

    async def generate_script_voice(self, user_prompt: str):
        full_prompt = f"""
        Actúa como un asistente de IA profesional para dentistas que crea contenido para pacientes.
        Descripción Técnica: {user_prompt}
        
        Prompt: Escribe un guion corto de 15-20 segundos con voz en off que traduzca esta descripción técnica en una explicación atractiva y fácil de entender.
        
        REGLAS DE ACTUACIÓN Y EXPRESIÓN (¡MUY IMPORTANTE!):
        1. Usa puntos suspensivos (...) para forzar pausas naturales o dramáticas.
        2. Usa signos de interrogación y exclamación para darle dinamismo y energía.
        3. Escribe en MAYÚSCULAS las palabras más importantes para que la voz les dé más énfasis y fuerza.
        4. Usa comas (,) frecuentemente para que la voz respire.
        
        IMPORTANTE: El guion DEBE estar SIEMPRE en español de Chile (chilenismos moderados, tono cercano pero profesional).
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_text,
                messages=[
                    {"role": "system", "content": "You are a professional dentist AI assistant creating content for patients."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.7, # Un poco de creatividad pero sin volverse loco
                max_tokens=150 # Limitar la respuesta para que sea un guion corto

            )
            script= response.choices[0].message.content
            ruta_final = self.file_manager.save_file(
                script, 
                file_type="text"
                )
            print(f"Script Generado - Archivo guardado en: {ruta_final}")
            return script
        
        except Exception as e:
            # Aquí podrías manejar errores específicos (falta de crédito, etc.)
            print(f"Error en OpenAI Service: {e}")
            raise e
    
    async def generate_voice(self, script_voice: str):        
        try:          
            # Elegimos la voz. OpenAI tiene:
            response_audio = self.client.audio.speech.create(
                model=self.model_audio,
                voice="nova",  # alloy, echo, fable, onyx, nova, y shimmer.
                input=script_voice
            )
            
            # Guardamos el audio. 
            # response_audio.content trae los "bytes" del mp3 listos para guardar
            ruta_audio = self.file_manager.save_file(
                response_audio.content, 
                file_type="audio", 
                extension="mp3"
            )
            
            # Extraemos solo el nombre del archivo (ej: gen_20260310_120000.mp3)
            nombre_archivo_audio = os.path.basename(ruta_audio)
            
            # Retornamos un diccionario con el texto y la URL pública del audio
            return {
                "texto": script_voice,
                "audio_url": f"{self.backend_url}/archivos/audio/{nombre_archivo_audio}"
            }
            
        except Exception as e:
            print(f"Error en el servicio: {e}")
            raise e