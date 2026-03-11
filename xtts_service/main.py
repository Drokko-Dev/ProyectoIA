import os
import re # Para cortar el texto con expresiones regulares
import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from TTS.api import TTS
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.effects import normalize
from pydub.silence import split_on_silence

# Cargamos variables de entorno por si quieres forzar la CPU
load_dotenv()

app = FastAPI(title="Motor de Voz XTTS - AI")

# --- 1. CONFIGURACIÓN DE HARDWARE Y MODELO (Se ejecuta al iniciar el contenedor) ---

# Buscamos el interruptor manual en el .env
forzar_cpu = os.getenv("FORZAR_CPU", "False").lower() == "true"

if torch.cuda.is_available() and not forzar_cpu:
    device = "cuda"
    print("🚀 Hardware: GPU NVIDIA detectada. XTTS volará.")
else:
    device = "cpu"
    print("🐌 Hardware: Usando CPU. La generación tomará más tiempo.")

print("⏳ Cargando modelo XTTS v2 en memoria (Esto puede tardar unos minutos la primera vez)...")
# Aquí se descarga el modelo de ~3GB si no existe, y se sube a la RAM/VRAM
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
print("✅ ¡Modelo cargado y listo para hablar!")

# --- 2. MODELO DE DATOS (Lo que esperamos recibir de tu backend principal) ---
class TTSRequest(BaseModel):
    text: str
    language: str = "es"  # Español por defecto
    # Esperamos que haya un archivo de referencia en una carpeta 'assets'
    speaker_wav: str = "assets/referencia.wav" 

# --- 3. EL ENDPOINT PRINCIPAL ---
@app.post("/api/tts")
async def generate_tts(request: TTSRequest):
    try:
        if not os.path.exists(request.speaker_wav):
            raise HTTPException(status_code=400, detail=f"Falta audio de referencia: {request.speaker_wav}")

        print(f"\n🎙️ Iniciando Pipeline de Estudio para: '{request.text[:40]}...'")
        
        # 1. CHUNKING: Cortamos el texto por puntos, signos de exclamación o interrogación
        # Esto evita que la IA lea párrafos largos, se quede sin aire y balbucee.
        oraciones = [o.strip() for o in re.split(r'[.;]+\s*', request.text) if len(o.strip()) > 2]
        
        # Preparamos nuestra "cinta de grabación" vacía y un silencio perfecto de 450ms
        audio_final = AudioSegment.empty()
        silencio_respiracion = AudioSegment.silent(duration=450) 
        
        output_path = "audio_masterizado.wav"

        # 2. GRABACIÓN POR TOMAS
        for i, oracion in enumerate(oraciones):
            print(f"   -> Grabando toma {i+1}/{len(oraciones)}: '{oracion}'")
            temp_wav = f"temp_chunk_{i}.wav"
            
            # Generamos solo esta oración cortita (Cero alucinaciones)
            tts.tts_to_file(
                text=oracion,
                speaker_wav=request.speaker_wav,
                language=request.language,
                file_path=temp_wav
            )
            
            # 3. COSTURA: Leemos el audio temporal, lo pegamos a la cinta principal y añadimos la pausa
            segmento = AudioSegment.from_wav(temp_wav)
            audio_final += segmento + silencio_respiracion
            
            # Limpiamos el archivo temporal para no llenar el disco duro
            os.remove(temp_wav)
            
        # 4. POST-PROCESAMIENTO: Masterización de volumen
        print("🎛️ Aplicando EQ y normalizando el volumen de estudio...")
        audio_final = normalize(audio_final)

        print("🎛️ Aplicando Masterización DSP de nivel comercial...")

        # 5. SUPRESIÓN DE SILENCIOS: Cortamos los espacios muertos largos o respiraciones robóticas
        # Buscamos silencios de más de 350ms que estén por debajo de -40 decibelios
        fragmentos_limpios = split_on_silence(audio_final, min_silence_len=350, silence_thresh=-40)
        
        audio_sin_baches = AudioSegment.empty()
        for chunk in fragmentos_limpios:
            # Pegamos los pedazos limpios con una pausa microscópica y perfecta de 150ms
            audio_sin_baches += chunk + AudioSegment.silent(duration=150)

        # 5.1. ECUALIZACIÓN (EQ de Locutor Comercial): 
        # Aislamos las frecuencias graves de la voz (debajo de 250Hz) y les subimos 4 decibelios 
        # para darle ese tono de "autoridad médica" y presencia de radio.
        bajos = audio_sin_baches.low_pass_filter(250) 
        audio_con_cuerpo = audio_sin_baches.overlay(bajos + 4) 

        # 5.2. NORMALIZACIÓN (El toque final que ya tenías)
        audio_masterizado = normalize(audio_con_cuerpo)
        
        # Exportamos la joya final
        audio_masterizado.export(output_path, format="wav")
        
        print("✅ ¡Audio renderizado con éxito!")
        
        return FileResponse(
            path=output_path, 
            media_type="audio/wav", 
            filename="audio_generado.wav"
        )
        
    except Exception as e:
        print(f"❌ Error interno en XTTS: {e}")
        raise HTTPException(status_code=500, detail=str(e))