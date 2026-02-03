import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    #Google Gemini (Gratis)
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "models/gemini-2.0-flash")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))

    AMBIENTE = os.getenv("AMBIENTE", "desarollo")
    DEBUG = os.getenv("DEBUG", "True") == "True"

    @classmethod 
    def validar(cls):
        if not cls.GOOGLE_API_KEY:
            raise ValueError(
                 "❌ ERROR: GOOGLE_API_KEY no está configurada.\n"
                "Ve a https://aistudio.google.com/ y obtén tu API key GRATIS"
            )   
        print("✅ Configuración validada correctamente")
        return True

if __name__ != "__main__":
    Settings.validar()