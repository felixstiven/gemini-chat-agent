"""
📦 MODELOS DE DATOS (SCHEMAS)
==============================

Este archivo define la ESTRUCTURA de los datos que viajan entre frontend y backend.

CONCEPTO CLAVE: Pydantic
-------------------------
Pydantic es una librería que:
1. Valida automáticamente los datos
2. Convierte tipos (ej: "123" → 123)
3. Genera documentación automática
4. Lanza errores claros si falta algo

Piensa en esto como un "contrato" entre frontend y backend.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MensajeRequest(BaseModel):
    """
    🔵 DATOS QUE RECIBIMOS DEL FRONTEND
    
    Cuando el usuario escribe un mensaje en el chat, el frontend envía:
    {
        "mensaje": "¿Cuál es el horario de atención?",
        "session_id": "abc-123-def"  // Opcional en el primer mensaje
    }
    
    Campos:
    -------
    mensaje : str
        El texto que escribió el usuario (OBLIGATORIO)
    
    session_id : str | None
        ID único para identificar la conversación (OPCIONAL)
        Si no viene, el backend genera uno nuevo
    """
    
    mensaje: str = Field(
        ...,  # Los tres puntos significan "obligatorio"
        min_length=1,  # Mínimo 1 carácter
        max_length=2000,  # Máximo 2000 caracteres
        description="Mensaje del usuario",
        example="¿Cuál es el horario de atención?"
    )
    
    session_id: Optional[str] = Field(
        None,  # None = opcional
        description="ID de sesión para mantener el contexto",
        example="550e8400-e29b-41d4-a716-446655440000"
    )
    
    class Config:
        # Configuración adicional
        json_schema_extra = {
            "example": {
                "mensaje": "Hola, necesito ayuda con mi pedido",
                "session_id": "abc-123"
            }
        }


class MensajeResponse(BaseModel):
    """
    🟢 DATOS QUE ENVIAMOS AL FRONTEND
    
    Después de procesar el mensaje, el backend responde:
    {
        "respuesta": "Nuestro horario es de 8am a 6pm",
        "session_id": "abc-123-def",
        "timestamp": "2026-01-23T13:30:00.123456",
        "tokens_usados": 45
    }
    
    Campos:
    -------
    respuesta : str
        La respuesta generada por el agente Gemini
    
    session_id : str
        El mismo ID de sesión (para que el frontend lo guarde)
    
    timestamp : str
        Fecha y hora exacta de la respuesta (formato ISO)
    
    tokens_usados : int
        Cantidad de tokens consumidos (para estadísticas)
    """
    
    respuesta: str = Field(
        ...,
        description="Respuesta generada por el agente",
        example="¡Hola! Estoy aquí para ayudarte. ¿En qué puedo asistirte hoy?"
    )
    
    session_id: str = Field(
        ...,
        description="ID de la sesión activa",
        example="550e8400-e29b-41d4-a716-446655440000"
    )
    
    timestamp: str = Field(
        ...,
        description="Fecha y hora de la respuesta (ISO 8601)",
        example="2026-01-23T13:30:00.123456"
    )
    
    tokens_usados: Optional[int] = Field(
        None,
        description="Tokens consumidos en esta interacción",
        example=45
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "respuesta": "Claro, con gusto te ayudo con tu pedido",
                "session_id": "abc-123",
                "timestamp": "2026-01-23T13:30:00",
                "tokens_usados": 32
            }
        }


class EstadisticasResponse(BaseModel):
    """
    📊 ESTADÍSTICAS DE UNA SESIÓN
    
    Respuesta para el endpoint GET /api/chat/stats/{session_id}
    """
    
    total_mensajes: int = Field(
        ...,
        description="Total de mensajes en esta sesión"
    )
    
    mensajes_en_historial: int = Field(
        ...,
        description="Mensajes guardados en memoria"
    )
    
    creado_en: str = Field(
        ...,
        description="Fecha de creación de la sesión"
    )
    
    costo_total: float = Field(
        ...,
        description="Costo acumulado (siempre 0.00 con Gemini gratis)"
    )


class ErrorResponse(BaseModel):
    """
    ❌ RESPUESTA DE ERROR
    
    Cuando algo sale mal, enviamos:
    {
        "detail": "Sesión no encontrada",
        "error_code": "SESSION_NOT_FOUND"
    }
    """
    
    detail: str = Field(
        ...,
        description="Descripción del error"
    )
    
    error_code: Optional[str] = Field(
        None,
        description="Código de error para manejo programático"
    )


# ============================================================================
# 💡 NOTAS EDUCATIVAS
# ============================================================================
"""
¿POR QUÉ USAR PYDANTIC?
-----------------------

SIN Pydantic (código manual):
```python
def enviar_mensaje(data: dict):
    # Validación manual (propenso a errores)
    if "mensaje" not in data:
        raise ValueError("Falta el campo 'mensaje'")
    if not isinstance(data["mensaje"], str):
        raise ValueError("'mensaje' debe ser string")
    if len(data["mensaje"]) == 0:
        raise ValueError("'mensaje' no puede estar vacío")
    # ... más validaciones ...
```

CON Pydantic (automático):
```python
def enviar_mensaje(request: MensajeRequest):
    # ¡Pydantic ya validó todo!
    # Si llegamos aquí, los datos son correctos
    mensaje = request.mensaje  # Garantizado que existe y es string
```

BENEFICIOS:
1. ✅ Menos código
2. ✅ Menos bugs
3. ✅ Documentación automática en /docs
4. ✅ Autocompletado en el IDE
5. ✅ Errores claros para el frontend

¿CÓMO SE USA EN FASTAPI?
-------------------------

En el endpoint:
```python
@router.post("/message")
async def enviar_mensaje(request: MensajeRequest) -> MensajeResponse:
    # FastAPI automáticamente:
    # 1. Lee el JSON del request
    # 2. Lo valida contra MensajeRequest
    # 3. Si es válido, crea el objeto 'request'
    # 4. Si es inválido, retorna error 422 automáticamente
    
    # Tu código solo trabaja con datos válidos
    print(request.mensaje)  # Siempre es un string válido
```

EJEMPLO DE VALIDACIÓN AUTOMÁTICA:
----------------------------------

Request VÁLIDO:
POST /api/chat/message
{
    "mensaje": "Hola"
}
→ ✅ Funciona

Request INVÁLIDO (mensaje vacío):
POST /api/chat/message
{
    "mensaje": ""
}
→ ❌ Error 422: "mensaje debe tener al menos 1 carácter"

Request INVÁLIDO (falta campo):
POST /api/chat/message
{
    "session_id": "abc"
}
→ ❌ Error 422: "campo 'mensaje' es requerido"
"""
