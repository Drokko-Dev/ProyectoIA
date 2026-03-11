import os
from datetime import datetime

class FileService:
    def __init__(self):
        self.base_path = "/data_storage"
        # Definimos los subdirectorios
        self.folders = {
            "text": "texts",
            "image": "images",
            "audio": "audio",
            "video": "video"
        }
        self._create_folders()

    def _create_folders(self):
        """Crea la estructura de carpetas si no existe"""
        for folder in self.folders.values():
            path = os.path.join(self.base_path, folder)
            os.makedirs(path, exist_ok=True)

    def save_file(self, content, file_type="text", extension="txt", prefix: str = "gen"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.{extension}"

        # Elegimos la subcarpeta correcta
        subfolder = self.folders.get(file_type, "texts")
        filepath = os.path.join(self.base_path, subfolder, filename)

        # Si es texto
        if file_type == "text":
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        # Si es binario (imagen, audio, video)
        else:
            with open(filepath, "wb") as f:
                f.write(content)
        
        return filepath