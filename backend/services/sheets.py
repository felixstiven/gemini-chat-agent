"""
Servicio para interactuar con Google Sheets

RESPONSABILIDAD:
- Conectar con Google Sheets API
- Guardar leads en la hoja de cálculo
- Leer leads (para futuras funcionalidades)

CONFIGURACIÓN NECESARIA:
1. Crear proyecto en Google Cloud Console
2. Habilitar Google Sheets API
3. Crear Service Account
4. Descargar credentials.json
5. Compartir hoja de cálculo con el email del Service Account

SEGURIDAD:
- credentials.json NUNCA en Git (.gitignore)
- Usar variables de entorno para rutas
"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from typing import Dict, List, Optional
import os
import logging

logger = logging.getLogger(__name__)


class SheetsService:
    """
    Servicio para manejar Google Sheets
    
    PATRÓN: Singleton
    - Una sola instancia de la conexión
    - Reutilizar cliente autenticado
    
    USO:
        sheets = SheetsService()
        sheets.guardar_lead(lead_data)
    """
    
    def __init__(self):
        """
        Inicializar servicio de Google Sheets
        
        PROCESO:
        1. Cargar credenciales desde archivo
        2. Autenticar con Google
        3. Abrir hoja de cálculo
        
        VARIABLES DE ENTORNO:
        - GOOGLE_CREDENTIALS_PATH: Ruta al archivo credentials.json
        - GOOGLE_SHEET_NAME: Nombre de la hoja de cálculo
        """
        self.client = None
        self.sheet = None
        self._inicializar()
    
    def _inicializar(self):
        """
        Inicializar conexión con Google Sheets
        
        SCOPES:
        - spreadsheets: Leer y escribir en hojas de cálculo
        """
        try:
            # Ruta al archivo de credenciales
            creds_path = os.getenv(
                'GOOGLE_CREDENTIALS_PATH',
                'credentials.json'  # Default
            )
            
            # Verificar si el archivo existe
            if not os.path.exists(creds_path):
                logger.warning(f"⚠️ Archivo de credenciales no encontrado: {creds_path}")
                logger.warning("⚠️ Google Sheets NO está configurado. El endpoint /api/leads no funcionará.")
                logger.warning("⚠️ Sigue la guía de configuración para habilitar Google Sheets.")
                self.client = None
                self.sheet = None
                return
            
            # Nombre de la hoja de cálculo
            sheet_name = os.getenv(
                'GOOGLE_SHEET_NAME',
                'LeadsAgenteIA'  # Default
            )
            
            # DEBUG: Verificar que se carga correctamente
            print(f"🔍 DEBUG: GOOGLE_SHEET_NAME = {sheet_name}")
            print(f"🔍 DEBUG: credentials path = {creds_path}")
            
            # Scopes necesarios
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            print("🔍 DEBUG: Autenticando con Google...")
            # Autenticar
            creds = Credentials.from_service_account_file(
                creds_path,
                scopes=scopes
            )
            
            print("🔍 DEBUG: Creando cliente gspread...")
            # Crear cliente
            self.client = gspread.authorize(creds)
            
            print(f"🔍 DEBUG: Abriendo hoja: {sheet_name}...")
            # Abrir hoja de cálculo
            self.sheet = self.client.open(sheet_name).sheet1
            
            logger.info(f"✅ Conectado a Google Sheets: {sheet_name}")
            print(f"✅ DEBUG: Conectado exitosamente a: {sheet_name}")
            
        except gspread.exceptions.SpreadsheetNotFound as e:
            print(f"❌ DEBUG: SpreadsheetNotFound - {e}")
            logger.error(f"❌ Hoja de cálculo no encontrada: {sheet_name}")
            logger.error("❌ Asegúrate de compartir la hoja con el Service Account email")
            self.client = None
            self.sheet = None
        
        except Exception as e:
            print(f"❌ DEBUG: Exception - {type(e).__name__}: {e}")
            logger.error(f"❌ Error al conectar con Google Sheets: {str(e)}")
            logger.error("❌ Google Sheets NO está disponible")
            self.client = None
            self.sheet = None
    
    def guardar_lead(self, lead_data: Dict) -> bool:
        """
        Guardar lead en Google Sheets
        
        FORMATO DE FILA:
        [ID, Empresa, Nombre, Email, Teléfono, Mensaje, Fecha, Estado]
        
        Args:
            lead_data: Diccionario con datos del lead
            
        Returns:
            bool: True si se guardó correctamente
            
        Raises:
            Exception: Si hay error al guardar
        """
        # Verificar si Google Sheets está configurado
        if self.sheet is None:
            logger.error("❌ Google Sheets no está configurado. No se puede guardar el lead.")
            raise Exception("Google Sheets no está configurado. Por favor, configura credentials.json")
        
        try:
            # Preparar fila
            fila = [
                lead_data.get('id', ''),
                lead_data.get('empresa', ''),
                lead_data.get('nombre', ''),
                lead_data.get('email', ''),
                lead_data.get('telefono', ''),
                lead_data.get('mensaje', ''),
                lead_data.get('fecha_creacion', datetime.now().isoformat()),
                lead_data.get('estado', 'nuevo')
            ]
            
            # Agregar fila a la hoja
            self.sheet.append_row(fila)
            
            # Logging seguro (solo ID, no datos personales)
            logger.info(f"✅ Lead guardado en Sheets: {lead_data.get('id')}")
            
            return True
            
        except Exception as e:
            # Logging del error (sin datos sensibles)
            logger.error(f"❌ Error al guardar lead en Sheets", exc_info=True)
            raise
    
    def obtener_leads(self, limit: int = 100) -> List[Dict]:
        """
        Obtener leads desde Google Sheets
        
        FUTURO: Para dashboard o CRM
        
        Args:
            limit: Número máximo de leads a retornar
            
        Returns:
            List[Dict]: Lista de leads
        """
        try:
            # Obtener todas las filas
            rows = self.sheet.get_all_values()
            
            # Primera fila son los headers
            headers = rows[0] if rows else []
            data_rows = rows[1:limit+1] if len(rows) > 1 else []
            
            # Convertir a lista de diccionarios
            leads = []
            for row in data_rows:
                lead = {
                    'id': row[0] if len(row) > 0 else '',
                    'empresa': row[1] if len(row) > 1 else '',
                    'nombre': row[2] if len(row) > 2 else '',
                    'email': row[3] if len(row) > 3 else '',
                    'telefono': row[4] if len(row) > 4 else '',
                    'mensaje': row[5] if len(row) > 5 else '',
                    'fecha_creacion': row[6] if len(row) > 6 else '',
                    'estado': row[7] if len(row) > 7 else 'nuevo'
                }
                leads.append(lead)
            
            logger.info(f"Obtenidos {len(leads)} leads desde Sheets")
            return leads
            
        except Exception as e:
            logger.error(f"Error al obtener leads desde Sheets", exc_info=True)
            raise


# Instancia global (Singleton)
# NOTA: Se inicializa al importar, asegúrate de que .env esté cargado antes
sheets_service = SheetsService()
