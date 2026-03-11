import os
import re
import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from TTS.api import TTS
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.effects import normalize
from pydub.silence import split_on_silence
from pydub.effects import speedup



# --- PARCHE DE COMPATIBILIDAD (Añadir antes de cargar torch) ---
# Necesario para evitar errores de carga en modelos personalizados con PyTorch 2.6+
original_load = torch.load
torch.load = lambda *args, **kwargs: original_load(*args, **{**kwargs, 'weights_only': False})

# Cargamos variables de entorno por si quieres forzar la CPU
load_dotenv()

# --- 0. RUTAS DEL MODELO PERSONALIZADO ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Asumimos que pusiste tus archivos en xtts_service/assets/model/
MODEL_PATH = os.path.join(BASE_DIR, "assets", "model")
DEFAULT_SPEAKER = os.path.join(MODEL_PATH, "reference.wav")

app = FastAPI(title="Motor de Voz XTTS - AI")

# --- 1. CONFIGURACIÓN DE HARDWARE Y MODELO (Se ejecuta al iniciar el contenedor) ---

forzar_cpu = os.getenv("FORZAR_CPU", "False").lower() == "true"
device = "cuda" if torch.cuda.is_available() and not forzar_cpu else "cpu"

try:
    # Simplemente cargamos el modelo local. 
    # XTTS detectará automáticamente que es_core_news_sm ya está instalado.
    tts = TTS(
        model_path=MODEL_PATH, 
        config_path=os.path.join(MODEL_PATH, "config.json")
    ).to(device)
    print("✅ ¡Modelo cargado y listo para hablar!")
except Exception as e:
    print(f"❌ ERROR CRÍTICO AL CARGAR MODELO: {e}")

# --- 2. MODELO DE DATOS (Lo que esperamos recibir de tu backend principal) ---
class TTSRequest(BaseModel):
    text: str
    language: str = "es"  # Español por defecto
    # Esperamos que haya un archivo de referencia en una carpeta 'assets'
    speaker_wav: str = DEFAULT_SPEAKER

def cambiar_tono(audio, octavas):
    # octavas > 0 es más agudo, < 0 es más grave
    nueva_tasa_muestreo = int(audio.frame_rate * (2.0 ** octavas))
    audio_con_nuevo_tono = audio._spawn(audio.raw_data, overrides={'frame_rate': nueva_tasa_muestreo})
    return audio_con_nuevo_tono.set_frame_rate(audio.frame_rate)


# --- 3. ENDPOINT PRINCIPAL ---
@app.post("/api/tts")
async def generate_tts(request: TTSRequest):
    try:
        # Validación de archivo de referencia
        if not os.path.exists(request.speaker_wav):
            # Si no existe la personalizada, intentamos usar la de assets/model
            request.speaker_wav = DEFAULT_SPEAKER
            if not os.path.exists(request.speaker_wav):
                raise HTTPException(status_code=400, detail="No se encontró el audio de referencia (.wav)")

        print(f"\n🎙️ Procesando: '{request.text[:40]}...'")
        
        # 1. CHUNKING (Corte de texto)
        oraciones = [o.strip() for o in re.split(r'(?<=[!?;¡¿])\s+|\.\s*', request.text) if len(o.strip()) > 2]
        
        audio_final = AudioSegment.empty()
        silencio_respiracion = AudioSegment.silent(duration=300) 
        output_path = "audio_masterizado.wav"

        # 2. GENERACIÓN POR TOMAS
        for i, oracion in enumerate(oraciones):
            temp_wav = f"temp_chunk_{i}.wav"
            
            tts.tts_to_file(
                text=oracion,
                speaker_wav=request.speaker_wav,
                language=request.language,
                file_path=temp_wav
            )
            
            segmento = AudioSegment.from_wav(temp_wav)
            audio_final += segmento + silencio_respiracion
            os.remove(temp_wav)
            
        # 3. POST-PROCESAMIENTO (Limpieza y Cambio de Tono)
        audio_final = normalize(audio_final)

        # A) Filtro de claridad agresivo (Adiós a lo grave)
        # Subimos a 250Hz para limpiar bien el "retumbe"
        audio_limpio = audio_final.high_pass_filter(250)

        # B) HACERLA MÁS AGUDA (Pitch Shift)
        # Prueba con 0.15 (sutil) o 0.25 (más agudo)
        audio_agudo = cambiar_tono(audio_limpio, octavas=0.12)

        # C) VELOCIDAD (Para que fluya)
        # Como ya es más aguda, la velocidad 1.10 se sentirá muy natural
        audio_agil = speedup(audio_agudo, playback_speed=1.08, chunk_size=150, crossfade=25)

        # D) EXPORTACIÓN FINAL
        audio_masterizado = normalize(audio_agil)
        audio_masterizado.export(output_path, format="wav")
        
        print("✅ Audio masterizado con claridad y rapidez.")
        
        return FileResponse(
            path=output_path, 
            media_type="audio/wav", 
            filename="audio_generado.wav"
        )
        
    except Exception as e:
        print(f"❌ Error interno: {e}")
        raise HTTPException(status_code=500, detail=str(e))