"""
ENDPOINTS DE ESTE ARCHIVO:
---------------------------
1. POST   /api/chat/message     → Enviar un mensaje al agente
2. GET    /api/chat/stats/{id}  → Obtener estadísticas de una sesión
3. DELETE /api/chat/clear/{id}  → Limpiar historial de una sesión
4. GET    /api/chat/sessions    → Listar todas las sesiones activas

FLUJO TÍPICO:
-------------
1. Usuario escribe "Hola" en el frontend
2. Frontend hace: POST /api/chat/message con {"mensaje": "Hola"}
3. Este código recibe el request
4. Llama a AgenteGemini.enviar_mensaje("Hola")
5. Retorna la respuesta al frontend
"""

from fastapi import APIRouter, HTTPException, status
from api.models.schemas import (
    MensajeRequest, 
    MensajeResponse, 
    EstadisticasResponse,
    ErrorResponse
)
from agentes.agente_gemini import AgenteGemini
from datetime import datetime
import uuid
from typing import Dict



# CONFIGURACIÓN DEL ROUTER
router = APIRouter(
    prefix="/chat",  # Todas las rutas empiezan con /chat
    tags=["Chat"],   # Agrupación en la documentación
)

# ALMACENAMIENTO DE SESIONES


# Diccionario para guardar las sesiones activas
# Estructura: { "session_id": AgenteGemini() }
#
# ⚠️ LIMITACIÓN ACTUAL: Esto se guarda en MEMORIA
# Si reinicias el servidor, se pierden todas las conversaciones.
#
# 💡 MEJORA FUTURA: Usar Redis o base de datos para persistencia
sesiones: Dict[str, AgenteGemini] = {}

# FUNCIONES AUXILIARES
def obtener_o_crear_sesion(session_id: str = None) -> tuple[str, AgenteGemini]:
    """
    Obtiene una sesión existente o crea una nueva.
    
    Parámetros:
    -----------
    session_id : str | None
        ID de sesión. Si es None, se genera uno nuevo.
    
    Retorna:
    --------
    tuple[str, AgenteGemini]
        (session_id, agente)
    
    Ejemplo:
    --------
    >>> session_id, agente = obtener_o_crear_sesion("abc-123")
    >>> agente.enviar_mensaje("Hola")
    """
    
    # Si no hay session_id, generar uno nuevo
    if not session_id:
        session_id = str(uuid.uuid4())
        print(f"🆕 Nueva sesión creada: {session_id}")
    
    # Si la sesión no existe, crear el agente
    if session_id not in sesiones:
        sesiones[session_id] = AgenteGemini()
        print(f"🤖 Agente creado para sesión: {session_id}")
    
    return session_id, sesiones[session_id]

# ENDPOINTS
@router.post(
    "/message",
    response_model=MensajeResponse,
    status_code=status.HTTP_200_OK,
    summary="Enviar mensaje al agente",
    description="Envía un mensaje al agente y recibe una respuesta",
    responses={
        200: {"description": "Respuesta exitosa"},
        500: {"model": ErrorResponse, "description": "Error del servidor"}
    }
)
async def enviar_mensaje(request: MensajeRequest) -> MensajeResponse:
    """
    🔵 ENDPOINT PRINCIPAL: Enviar mensaje al agente
    
    Este es el endpoint más importante.
    
    FLUJO PASO A PASO:
    ------------------
    1. FastAPI recibe el JSON del frontend
    2. Pydantic valida que tenga la estructura correcta (MensajeRequest)
    3. Obtenemos o creamos la sesión del usuario
    4. Enviamos el mensaje al agente Gemini
    5. Retornamos la respuesta estructurada (MensajeResponse)
    
    EJEMPLO DE USO (desde el frontend):
    -----------------------------------
    ```javascript
    const response = await fetch('http://localhost:8000/api/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            mensaje: "¿Cuál es el horario?",
            session_id: "abc-123"  // Opcional
        })
    });
    const data = await response.json();
    console.log(data.respuesta);  // "Nuestro horario es..."
    ```
    
    PARÁMETROS:
    -----------
    request : MensajeRequest
        Objeto validado con el mensaje del usuario
    
    RETORNA:
    --------
    MensajeResponse
        Objeto con la respuesta del agente
    
    ERRORES:
    --------
    - 422: Datos inválidos (Pydantic lo maneja automáticamente)
    - 500: Error al procesar el mensaje
    """
    
    try:
        # PASO 1: Obtener o crear sesión
        # --------------------------------
        # Si el usuario envía un session_id, usamos ese.
        # Si no, generamos uno nuevo (primera vez que habla)
        session_id, agente = obtener_o_crear_sesion(request.session_id)
        
        # PASO 2: Enviar mensaje al agente
        # ---------------------------------
        # Aquí llamamos a tu clase AgenteGemini que ya funciona
        respuesta_texto = agente.enviar_mensaje(request.mensaje)
        
        # PASO 3: Preparar respuesta estructurada
        # ----------------------------------------
        # Creamos un objeto MensajeResponse con todos los datos
        respuesta = MensajeResponse(
            respuesta=respuesta_texto,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            tokens_usados=None  # Gemini no expone esto fácilmente
        )
        
        # PASO 4: Retornar
        # ----------------
        # FastAPI automáticamente convierte esto a JSON
        return respuesta
        
    except Exception as e:
        # Si algo sale mal, retornar error HTTP 500
        print(f"❌ Error en enviar_mensaje: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el mensaje: {str(e)}"
        )


@router.get(
    "/stats/{session_id}",
    response_model=EstadisticasResponse,
    summary="Obtener estadísticas de una sesión",
    responses={
        200: {"description": "Estadísticas obtenidas"},
        404: {"model": ErrorResponse, "description": "Sesión no encontrada"}
    }
)
async def obtener_estadisticas(session_id: str) -> EstadisticasResponse:
    """
    📊 ENDPOINT: Obtener estadísticas
    
    Retorna información sobre una sesión específica:
    - Total de mensajes
    - Mensajes en historial
    - Fecha de creación
    - Costo (siempre 0.00 con Gemini gratis)

    PARÁMETROS:
    -----------
    session_id : str
        ID de la sesión (viene en la URL)
    
    RETORNA:
    --------
    EstadisticasResponse
        Objeto con las estadísticas
    
    ERRORES:
    --------
    - 404: Sesión no encontrada
    """
    
    # Verificar que la sesión existe
    if session_id not in sesiones:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sesión '{session_id}' no encontrada"
        )
    
    # Obtener estadísticas del agente
    agente = sesiones[session_id]
    stats = agente.obtener_estadisticas()
    
    # Retornar como objeto estructurado
    return EstadisticasResponse(**stats)


@router.delete(
    "/clear/{session_id}",
    summary="Limpiar historial de una sesión",
    responses={
        200: {"description": "Historial limpiado"},
        404: {"model": ErrorResponse, "description": "Sesión no encontrada"}
    }
)
async def limpiar_historial(session_id: str) -> dict:
    """
    🗑️ ENDPOINT: Limpiar historial
    
    Borra el historial de conversación de una sesión.
    La sesión sigue existiendo, pero el agente "olvida" todo.
    
    PARÁMETROS:
    -----------
    session_id : str
        ID de la sesión
    
    RETORNA:
    --------
    dict
        Mensaje de confirmación
    
    ERRORES:
    --------
    - 404: Sesión no encontrada
    """
    
    if session_id not in sesiones:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sesión '{session_id}' no encontrada"
        )
    
    # Limpiar el historial del agente
    sesiones[session_id].limpiar_historial()
    
    return {
        "mensaje": "Historial limpiado exitosamente",
        "session_id": session_id
    }


@router.get(
    "/sessions",
    summary="Listar sesiones activas",
    description="Retorna todas las sesiones activas en el servidor"
)
async def listar_sesiones() -> dict:
    """
    📋 ENDPOINT: Listar sesiones
    
    Retorna información sobre todas las sesiones activas.
    Útil para debugging o panel de administración.
    
    EJEMPLO DE USO:
    ---------------
    ```javascript
    const sessions = await fetch('http://localhost:8000/api/chat/sessions');
    const data = await sessions.json();
    console.log(`Sesiones activas: ${data.total}`);
    ```
    
    RETORNA:
    --------
    dict
        {
            "total": 3,
            "sesiones": ["abc-123", "def-456", "ghi-789"]
        }
    """
    
    return {
        "total": len(sesiones),
        "sesiones": list(sesiones.keys())
    }


@router.delete(
    "/sessions/{session_id}",
    summary="Eliminar una sesión completamente",
    responses={
        200: {"description": "Sesión eliminada"},
        404: {"model": ErrorResponse, "description": "Sesión no encontrada"}
    }
)
async def eliminar_sesion(session_id: str) -> dict:
    """
    🗑️ ENDPOINT: Eliminar sesión
    
    Elimina completamente una sesión (no solo el historial).
    Libera memoria del servidor.
    
    DIFERENCIA con /clear:
    ----------------------
    - /clear: Borra historial, sesión sigue existiendo
    - /sessions/{id}: Elimina todo, sesión desaparece
    
    PARÁMETROS:
    -----------
    session_id : str
        ID de la sesión a eliminar
    
    RETORNA:
    --------
    dict
        Mensaje de confirmación
    """
    
    if session_id not in sesiones:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sesión '{session_id}' no encontrada"
        )
    
    # Eliminar la sesión del diccionario
    del sesiones[session_id]
    
    return {
        "mensaje": "Sesión eliminada exitosamente",
        "session_id": session_id
    }


# ============================================================================
# 💡 NOTAS EDUCATIVAS
# ============================================================================
"""
CONCEPTOS IMPORTANTES:
----------------------

1. MÉTODOS HTTP:
   - GET: Obtener datos (no modifica nada)
   - POST: Crear/enviar datos
   - DELETE: Eliminar datos
   - PUT/PATCH: Actualizar datos

2. CÓDIGOS DE ESTADO HTTP:
   - 200: OK (todo bien)
   - 404: Not Found (no existe)
   - 422: Unprocessable Entity (datos inválidos)
   - 500: Internal Server Error (error del servidor)

3. PATH PARAMETERS vs QUERY PARAMETERS:
   
   Path parameter (en la URL):
   /api/chat/stats/abc-123
                    ^^^^^^^ session_id
   
   Query parameter (después de ?):
   /api/chat/message?limit=10&offset=0
                     ^^^^^^^^^^^^^^^^^ parámetros opcionales

4. ASYNC/AWAIT:
   - `async def`: Función asíncrona
   - Permite manejar múltiples requests simultáneamente
   - FastAPI lo maneja automáticamente

5. TYPE HINTS:
   - `session_id: str` → session_id debe ser string
   - `-> MensajeResponse` → la función retorna MensajeResponse
   - Ayuda al IDE y a FastAPI a validar

MEJORES PRÁCTICAS APLICADAS:
-----------------------------

✅ Separación de responsabilidades
   - Este archivo solo maneja HTTP
   - La lógica del agente está en agente_gemini.py

✅ Validación automática
   - Pydantic valida todos los inputs

✅ Manejo de errores
   - HTTPException para errores claros

✅ Documentación
   - Docstrings detallados
   - FastAPI genera docs automáticas en /docs

✅ Código limpio
   - Nombres descriptivos
   - Comentarios explicativos
   - Estructura clara

PRÓXIMOS PASOS PARA MEJORAR:
-----------------------------

1. Persistencia: Guardar sesiones en Redis/DB
2. Rate limiting: Limitar requests por usuario
3. Autenticación: JWT tokens
4. Logging: Registrar todas las interacciones
5. Caché: Cachear respuestas comunes
6. WebSockets: Respuestas en tiempo real
7. Streaming: Respuestas palabra por palabra
"""
