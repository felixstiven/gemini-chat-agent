"""
Endpoints para manejo de Leads

RESPONSABILIDAD:
- Recibir requests del frontend
- Validar datos con Pydantic
- Guardar en Google Sheets
- Retornar respuestas

SEGURIDAD:
- Validación automática con Pydantic
- Manejo de errores sin revelar información
- Logging seguro
"""

from fastapi import APIRouter, HTTPException, status
from models.lead import LeadCreate, LeadResponse
from services.sheets import sheets_service
from datetime import datetime
import uuid
import logging
import bleach

# Configurar logging
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(
    prefix="/api",
    tags=["leads"]
)


@router.post(
    "/leads",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo lead",
    description="Crea un nuevo lead con los datos proporcionados y lo guarda en Google Sheets"
)
async def crear_lead(lead: LeadCreate) -> LeadResponse:
    """
    Crear nuevo lead
    
    FLUJO:
    1. Recibir datos del frontend
    2. Pydantic valida automáticamente (tipos, formatos, sanitización)
    3. Generar UUID para el lead
    4. Agregar timestamp
    5. Guardar en Google Sheets
    6. Retornar LeadResponse
    
    Args:
        lead: Datos del lead (validados por Pydantic)
        
    Returns:
        LeadResponse: Lead creado con ID, fecha y estado
        
    Raises:
        HTTPException 422: Si los datos son inválidos (automático de Pydantic)
        HTTPException 500: Si hay error al guardar
        
    EJEMPLO DE REQUEST:
        POST /api/leads
        {
            "empresa": "Mi Empresa SAS",
            "nombre": "Juan Pérez",
            "email": "juan@empresa.com",
            "telefono": "3001234567",
            "mensaje": "Quiero más información"
        }
        
    EJEMPLO DE RESPONSE:
        201 Created
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "empresa": "Mi Empresa SAS",
            "nombre": "Juan Pérez",
            "email": "juan@empresa.com",
            "telefono": "3001234567",
            "mensaje": "Quiero más información",
            "fecha_creacion": "2026-01-28T12:30:00.123456",
            "estado": "nuevo"
        }
    """
    try:
        # Paso 1: Generar UUID único para el lead
        lead_id = str(uuid.uuid4())
        
        # Paso 2: Obtener timestamp actual
        fecha_creacion = datetime.now()
        
        # Paso 3: Preparar datos para guardar
        lead_data = {
            'id': lead_id,
            'empresa': lead.empresa,
            'nombre': lead.nombre,
            'email': lead.email,
            'telefono': lead.telefono,
            'mensaje': lead.mensaje,
            'fecha_creacion': fecha_creacion.isoformat(),
            'estado': 'nuevo'
        }
        
        # Paso 4: Guardar en Google Sheets
        sheets_service.guardar_lead(lead_data)
        
        # Paso 5: Logging seguro (solo ID, no datos personales)
        logger.info(f"Lead creado exitosamente: {lead_id}")
        
        # Paso 6: Crear respuesta
        response = LeadResponse(
            id=lead_id,
            empresa=lead.empresa,
            nombre=lead.nombre,
            email=lead.email,
            telefono=lead.telefono,
            mensaje=lead.mensaje,
            fecha_creacion=fecha_creacion,
            estado='nuevo'
        )
        
        return response
        
    except Exception as e:
        # Logging del error (con detalles para debugging)
        logger.error(f"Error al crear lead", exc_info=True)
        
        # Retornar error genérico al usuario (no revelar detalles internos)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar la solicitud. Por favor, intenta de nuevo."
        )


@router.get(
    "/leads",
    response_model=list[LeadResponse],
    summary="Obtener leads",
    description="Obtiene la lista de leads guardados (para futuro dashboard)"
)
async def obtener_leads(limit: int = 100):
    """
    Obtener lista de leads
    
    FUTURO: Para dashboard o CRM
    
    Args:
        limit: Número máximo de leads a retornar (default: 100)
        
    Returns:
        List[LeadResponse]: Lista de leads
    """
    try:
        # Obtener leads desde Sheets
        leads_data = sheets_service.obtener_leads(limit=limit)
        
        # Convertir a LeadResponse
        leads = []
        for data in leads_data:
            lead = LeadResponse(
                id=data['id'],
                empresa=data['empresa'],
                nombre=data['nombre'],
                email=data['email'],
                telefono=data.get('telefono'),
                mensaje=data.get('mensaje'),
                fecha_creacion=datetime.fromisoformat(data['fecha_creacion']),
                estado=data.get('estado', 'nuevo')
            )
            leads.append(lead)
        
        logger.info(f"Obtenidos {len(leads)} leads")
        return leads
        
    except Exception as e:
        logger.error(f"Error al obtener leads", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener leads"
        )
