"""
Agente usando Google Gemini (100% GRATIS)
"""

import google.generativeai as genai 
from config.setting import Settings
from typing import List, Dict
import json
from datetime import datetime


class AgenteGemini:
    """
    Agente conversacional usando Google Gemini.
    
    VENTAJAS:
    - 100% gratuito
    - No requiere tarjeta de crédito
    - Límites generosos (1500 peticiones/día)

    """
    def __init__(self, system_prompt: str = None):
        """ Inicializa el agente con Gemini """
        #Configurar Gemini 
        genai.configure(api_key=Settings.GOOGLE_API_KEY)

        #Crear el modelo
        self.model = genai.GenerativeModel(
            model_name=Settings.MODEL_NAME,
            system_instruction=system_prompt or self._get_default_system_prompt()
        )

        # Iniciar sesión de chat (esto mantiene la memoria)
        self.chat = self.model.start_chat(history=[])

        # Metadatos
        self.metadatos = {
            "total_mensajes": 0,
            "creado_en": datetime.now().isoformat()
        }

        print(f"✅ Agente Gemini inicializado (GRATIS)")

    def _get_default_system_prompt(self) -> str:
        """ Personalidad del agente """
        return """
        Eres un asistente inteligente de atención al cliente para WOG sas.
        
        CARACTERÍSTICAS:
        - Profesional pero cercano
        - Hablas español colombiano de forma natural
        - Eres resolutivo y eficiente
        - Si no sabes algo, lo admites honestamente
        
        REGLAS:
        - Respuestas concisas (máximo 3 párrafos)
        - Usa ejemplos cuando sea útil
        - Prioriza la satisfacción del cliente
        """

    def enviar_mensaje(self, mensaje_usuario: str) -> str:
        """
        Envía un mensaje al agente.
        
        Args:
            mensaje_usuario: El mensaje del usuario
            
        Returns:
            La respuesta del agente
        """
        print(f"\n 👤 Usuario: {mensaje_usuario}")  

        try: 
            # Enviar el mensaje (Gemini mantiene el historial automaticamente)
            response = self.chat.send_message(mensaje_usuario)  

            respuesta_texto = response.text

            #Actualizar estadisticas 
            self.metadatos["total_mensajes"] += 1

            print(f"🤖 Agente: {respuesta_texto}")

            return respuesta_texto

        except Exception as e:
            error_msg = f" ❌ Error: {str(e)}" 
            print(error_msg)   
            return(error_msg)

    def obtener_estadisticas(self) -> Dict:
        """Retorna estadisticas del agente """
        return {
            **self.metadatos,
            "mensajes_en_historial": len(self.chat.history),
            "costo_total": 0.00 #Gratis
        }        

    def limpiar_historial(self):
        """Reinicia la conversacion """
        self.chat = self.model.start_chat(history=[])
        print("🗑️ Historial limpiado")

    def guardar_conversacion(self, archivo: str = "conversacion_gemini.json"):
        """Guardar el historial en un archivo"""
        historial = []

        for message in self.chat.history:
            historial.append({
                "role": message.role,
                "content": message.parts[0].text
            })        

        with open(archivo, "w", encoding="utf-8") as f:
            json.dump({
                "historial": historial,
                "metadatos": self.metadatos
            }, f, indent=2, ensure_ascii=False)

        print(f"💾 Conversación guardada en: {archivo}")        