"""
Punto de entrada - Ahora usando Gemini GRATIS
"""


from agentes.agente_gemini import AgenteGemini
from config.setting import Settings
import json


def modo_interactivo():
    """Chat interativo con Gemini"""
    print("=" * 60)
    print("🤖 AGENTE WOG - POWERED BY GOOGLE GEMINI (GRATIS)")
    print("=" * 60)
    print("Comandos especiales:")
    print("  - 'salir': Terminar")
    print("  - 'stats': Ver estadísticas")
    print("  - 'limpiar': Borrar historial")
    print("=" * 60)
    print()

    #Crear el agente 
    agente = AgenteGemini()

    while True:
        try:
            entrada = input("👤 Tú: ").strip()
            
            if entrada.lower() in ["salir", "exit"]:
                print("\n👋 ¡Hasta pronto!")

                guardar = input("¿Guardar conversación? (s/n): ").lower()
                if guardar == "si":
                    agente.guardar_conversacion()

                #Estadisticas finales
                print("\n📊 ESTADÍSTICAS FINALES:")
                stats = agente.obtener_estadisticas()
                print(json.dumps(stats, indent=2, ensure_ascii=False)) 

                break
            elif entrada.lower() == "stats":
                stats = agente.obtener_estadisticas()
                print("\n📊 ESTADÍSTICAS:")
                print(json.dumps(stats, indent=2, ensure_ascii=False))
                print()
                continue
            
            elif entrada.lower() == "limpiar":
                agente.limpiar_historial()
                continue

            if entrada: 
                agente.enviar_mensaje(entrada)

        except KeyboardInterrupt:
             print("\n\n👋 Sesión interrumpida")
             break
        except Exception as e:
             print(f"\n❌ Error: {e}")
             continue
    
if __name__== "__main__":
    modo_interactivo()