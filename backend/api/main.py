"""
🚀 SERVIDOR PRINCIPAL - FASTAPI
================================
"""

# Cargar variables de entorno ANTES de todo
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat
from api.routes import leads
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importaciones
# Esto permite importar desde 'agentes' y 'config'
sys.path.append(str(Path(__file__).parent.parent))


# ============================================================================
# CREACIÓN DE LA APLICACIÓN
# ============================================================================

app = FastAPI(
    # Metadata que aparece en la documentación automática
    title="🤖 Asistente de Stiven Felix",
    description="""
    API REST para agente conversacional con Google Gemini.
    
    ## Características
    
    * **Chat inteligente** - Conversaciones con IA usando Gemini
    * **Sesiones persistentes** - Mantiene el contexto de la conversación
    * **Estadísticas** - Tracking de uso y métricas
    * **Documentación automática** - Swagger UI en /docs
    
    ## Endpoints Principales
    
    * `POST /api/chat/message` - Enviar mensaje al agente
    * `GET /api/chat/stats/{session_id}` - Obtener estadísticas
    * `DELETE /api/chat/clear/{session_id}` - Limpiar historial
    
    ## Tecnologías
    
    * FastAPI - Framework web
    * Google Gemini - Modelo de IA
    * Pydantic - Validación de datos
    """,
    version="1.0.0",
    docs_url="/docs",  # Documentación Swagger
    redoc_url="/redoc",  # Documentación alternativa
    openapi_url="/openapi.json"  # Schema OpenAPI
)    

# CONFIGURACIÓN DE CORS


app.add_middleware(
    CORSMiddleware,
    
    # ORÍGENES PERMITIDOS
    # -------------------
    # Lista de URLs desde donde se puede acceder a esta API
    allow_origins=[
        "http://localhost:5173",  # Vite (React dev server)
        "http://localhost:3000",  # Create React App
        "http://127.0.0.1:5173",  # Alternativa de localhost
        "https://perfilprofesional-production-2e21.up.railway.app"
        
    ],
    
    # CREDENCIALES
    # ------------
    # Permite enviar cookies y headers de autenticación
    allow_credentials=True,
    
    # MÉTODOS HTTP PERMITIDOS
    # -----------------------
    # ["*"] = todos (GET, POST, PUT, DELETE, etc.)
    # También puedes especificar: ["GET", "POST"]
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    
    # HEADERS PERMITIDOS
    # ------------------
    # ["*"] = todos los headers
    # Incluye: Content-Type, Authorization, etc.
    allow_headers=["Content-Type", "Authorization"], 
) 


# ============================================================================
# INCLUSIÓN DE RUTAS
# ============================================================================

"""
ORGANIZACIÓN DE RUTAS:
----------------------

En lugar de poner todos los endpoints aquí, los organizamos en módulos:

api/routes/chat.py → Endpoints del chat
api/routes/admin.py → Endpoints de administración (futuro)
api/routes/analytics.py → Endpoints de analytics (futuro)

Esto mantiene el código organizado y escalable.
"""

# Incluir las rutas del chat
app.include_router(
    chat.router,
    prefix="/api",
    tags=["Chat"]
)

# Incluir las rutas de leads
app.include_router(
    leads.router,
    tags=["Leads"]
)


# ============================================================================
# ENDPOINTS DE UTILIDAD
# ============================================================================

@app.get(
    "/",
    tags=["Utilidad"],
    summary="Endpoint raíz",
    description="Información básica de la API"
)
async def root():
    """
    🏠 ENDPOINT RAÍZ
    
    Retorna información básica cuando accedes a http://localhost:8000/
    
    EJEMPLO DE USO:
    ---------------
    ```bash
    curl http://localhost:8000/
    ```
    
    RETORNA:
    --------
    {
        "mensaje": "API del Agente WOG funcionando correctamente",
        "version": "1.0.0",
        "documentacion": "/docs",
        "endpoints": {...}
    }
    """
    return {
        "mensaje": "🤖 API del Agente WOG funcionando correctamente",
        "version": "1.0.0",
        "documentacion": "/docs",
        "documentacion_alternativa": "/redoc",
        "endpoints": {
            "chat": "/api/chat/message",
            "leads": "/api/leads",
            "estadisticas": "/api/chat/stats/{session_id}",
            "limpiar": "/api/chat/clear/{session_id}",
            "sesiones": "/api/chat/sessions"
        }
    }


@app.get(
    "/health",
    tags=["Utilidad"],
    summary="Health check",
    description="Verifica que el servidor esté funcionando"
)
async def health_check():
    """
    ❤️ HEALTH CHECK
    
    Endpoint simple para verificar que el servidor está vivo.
    Útil para:
    - Monitoreo automático
    - Load balancers
    - Sistemas de orquestación (Kubernetes, Docker Swarm)
    
    EJEMPLO DE USO:
    ---------------
    ```bash
    curl http://localhost:8000/health
    ```
    
    RETORNA:
    --------
    {
        "status": "ok",
        "service": "api-agente-wog"
    }
    """
    return {
        "status": "ok",
        "service": "api-agente-wog"
    }


@app.get(
    "/info",
    tags=["Utilidad"],
    summary="Información del sistema",
    description="Retorna información sobre el servidor y configuración"
)
async def info():
    """
    ℹ️ INFORMACIÓN DEL SISTEMA
    
    Retorna información útil sobre el servidor.
    
    RETORNA:
    --------
    Información sobre:
    - Versión de Python
    - Sesiones activas
    - Configuración
    """
    import platform
    from api.routes.chat import sesiones
    
    return {
        "python_version": platform.python_version(),
        "sistema_operativo": platform.system(),
        "sesiones_activas": len(sesiones),
        "modelo_ia": "Google Gemini 1.5 Flash",
        "costo": "Gratis 🎉"
    }


# ============================================================================
# EVENTO DE INICIO
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    🚀 EVENTO DE INICIO
    
    Se ejecuta UNA VEZ cuando el servidor arranca.
    Útil para:
    - Inicializar conexiones a bases de datos
    - Cargar configuraciones
    - Validar variables de entorno
    - Logging inicial
    """
    print("=" * 60)
    print("🚀 SERVIDOR FASTAPI INICIADO")
    print("=" * 60)
    print("📚 Documentación: http://localhost:8000/docs")
    print("🔗 API Base: http://localhost:8000/api")
    print("❤️ Health Check: http://localhost:8000/health")
    print("=" * 60)
    
    # Validar configuración
    from config.setting import Settings
    try:
        Settings.validar()
    except ValueError as e:
        print(f"❌ ERROR DE CONFIGURACIÓN: {e}")
        print("⚠️ El servidor arrancó pero puede fallar en runtime")


@app.on_event("shutdown")
async def shutdown_event():
    """
    🛑 EVENTO DE CIERRE
    
    Se ejecuta cuando el servidor se detiene.
    Útil para:
    - Cerrar conexiones a bases de datos
    - Guardar estado
    - Cleanup de recursos
    """
    print("\n" + "=" * 60)
    print("🛑 SERVIDOR DETENIDO")
    print("=" * 60)
    
    # Guardar todas las conversaciones antes de cerrar
    from api.routes.chat import sesiones
    print(f"📊 Total de sesiones activas: {len(sesiones)}")
    
    # Aquí podrías guardar las sesiones en disco
    # for session_id, agente in sesiones.items():
    #     agente.guardar_conversacion(f"session_{session_id}.json")


# ============================================================================
# 💡 NOTAS EDUCATIVAS
# ============================================================================
"""
CÓMO FUNCIONA TODO JUNTO:
-------------------------

1. INICIO DEL SERVIDOR:
   $ uvicorn api.main:app --reload
   
   - Uvicorn carga este archivo
   - Ejecuta startup_event()
   - El servidor empieza a escuchar en puerto 8000

2. LLEGA UNA PETICIÓN:
   POST http://localhost:8000/api/chat/message
   
   - FastAPI recibe la petición
   - Verifica CORS (¿origen permitido?)
   - Busca el endpoint que coincida (chat.enviar_mensaje)
   - Valida el body con Pydantic (MensajeRequest)
   - Ejecuta la función
   - Retorna la respuesta (MensajeResponse)

3. DOCUMENTACIÓN AUTOMÁTICA:
   http://localhost:8000/docs
   
   - FastAPI genera Swagger UI automáticamente
   - Puedes probar todos los endpoints desde el navegador
   - No necesitas Postman para testing básico

ESTRUCTURA DE ARCHIVOS:
------------------------

api/
├── main.py              ← ESTE ARCHIVO (servidor principal)
├── routes/
│   └── chat.py          ← Endpoints del chat
└── models/
    └── schemas.py       ← Modelos de datos

FLUJO DE DATOS:
---------------

Frontend (React)
    ↓ HTTP Request
CORS Middleware
    ↓ Validación de origen
Router (/api/chat/message)
    ↓ Enrutamiento
Pydantic Validation
    ↓ Validación de datos
Endpoint Function (chat.enviar_mensaje)
    ↓ Lógica de negocio
AgenteGemini
    ↓ Llamada a IA
Google Gemini API
    ↓ Respuesta
Endpoint Function
    ↓ Formateo de respuesta
FastAPI
    ↓ HTTP Response
Frontend (React)

COMANDOS ÚTILES:
----------------

# Iniciar servidor (modo desarrollo con auto-reload)
uvicorn api.main:app --reload

# Iniciar en puerto específico
uvicorn api.main:app --reload --port 8080

# Iniciar accesible desde red local
uvicorn api.main:app --reload --host 0.0.0.0

# Ver logs detallados
uvicorn api.main:app --reload --log-level debug

PRÓXIMOS PASOS:
---------------

1. ✅ Crear el frontend React (Fase 2)
2. ⬜ Agregar autenticación (JWT)
3. ⬜ Implementar WebSockets para streaming
4. ⬜ Agregar base de datos (PostgreSQL/MongoDB)
5. ⬜ Implementar caché (Redis)
6. ⬜ Agregar rate limiting
7. ⬜ Configurar logging profesional
8. ⬜ Dockerizar la aplicación
9. ⬜ Deploy en producción (Railway/Render)
"""


# ============================================================================
# PUNTO DE ENTRADA (para desarrollo)
# ============================================================================

if __name__ == "__main__":
    """
    Permite ejecutar directamente: python api/main.py
    
    En producción, usar: uvicorn api.main:app
    """
    import uvicorn
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",  # Accesible desde cualquier IP
        port=8000,
        reload=True,  # Auto-reload en cambios de código
        log_level="info"
    )
