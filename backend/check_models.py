import google.generativeai as genai
from config.setting import Settings

genai.configure(api_key=Settings.GOOGLE_API_KEY)

with open("modelos_disponibles.txt", "w", encoding="utf-8") as f:
    f.write("MODELOS DISPONIBLES:\n\n")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            f.write(f"{model.name}\n")

print("✅ Lista guardada en modelos_disponibles.txt")
