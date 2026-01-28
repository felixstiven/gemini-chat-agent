import sys
sys.path.insert(0,"")

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv()

from services.sheets import sheets_service

#lead de prueba
lead_data = {
    'id': 'test-001',
    'empresa': 'Empresa de Prueba',
    'nombre': 'Usuario Test',
    'email': 'test@test.com',
    'telefono': '3001234567',
    'mensaje': 'Este es un mensaje de prueba',
    'fecha_creacion': '2026-01-28T15:00:00',
    'estado': 'nuevo'
}

#probar guardado
print("Guardando lead...")
try:
    sheets_service.guardar_lead(lead_data)
    print("✅ Lead guardado exitosamente")
except Exception as e:
    print(f"❌ Error al guardar lead: {e}")
