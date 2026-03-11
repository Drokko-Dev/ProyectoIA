import os
import torch
from TTS.api import TTS

# EL RADAR DE HARDWARE
# 'cuda' es el nombre del lenguaje que usan las tarjetas gráficas NVIDIA
forzar_cpu = os.getenv("FORZAR_CPU", "False") == "True"

if torch.cuda.is_available() and not forzar_cpu:
    device = "cuda"
    print("🚀 GPU detectada. XTTS volará.")
else:
    device = "cpu"
    print("🐌 No se detectó GPU. XTTS usará CPU (tomará más tiempo).")

print(f"Cargando el modelo XTTS v2 en {device}...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# 3. Le decimos que genere el audio
tts.tts_to_file(
    text="Hola Jaime, estoy hablando con tu voz clonada.",
    speaker_wav="mi_voz_de_prueba.wav", # El audio de 5 segundos que grabaste
    language="es",
    file_path="resultado.wav" # Dónde queremos guardar el audio final
)