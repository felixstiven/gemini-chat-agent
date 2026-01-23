# 🤖 Agente Conversacional WOG

> Sistema de chat inteligente con Google Gemini y FastAPI

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-orange.svg)](https://ai.google.dev/)

---

## 📋 Descripción

Agente conversacional inteligente desarrollado con **Google Gemini** y **FastAPI**. Incluye:

- ✅ **API REST** completa con FastAPI
- ✅ **Agente IA** usando Google Gemini 1.5 Flash (100% gratis)
- ✅ **Gestión de sesiones** para múltiples usuarios
- ✅ **Documentación automática** con Swagger UI
- ✅ **Código limpio** con mejores prácticas

---

## 🏗️ Arquitectura

```
┌─────────────┐      HTTP      ┌──────────────┐      API      ┌────────────┐
│   Cliente   │ ◄────────────► │   FastAPI    │ ◄───────────► │   Gemini   │
│  (Frontend) │                │   Backend    │               │     AI     │
└─────────────┘                └──────────────┘               └────────────┘
```

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.10 o superior
- Cuenta de Google (para obtener API Key de Gemini)

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/NOMBRE_REPO.git
cd NOMBRE_REPO
```

### Paso 2: Crear entorno virtual

```bash
python -m venv venv
```

### Paso 3: Activar entorno virtual

**Windows:**
```bash
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Paso 4: Instalar dependencias

```bash
pip install -r requirements/requirements.txt
```

### Paso 5: Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
GOOGLE_API_KEY=tu_api_key_aqui
MODEL_NAME=gemini-1.5-flash
MAX_TOKENS=1024
AMBIENTE=desarrollo
DEBUG=True
```

**Obtener API Key:** https://aistudio.google.com/

---

## 🎮 Uso

### Modo Consola (Interactivo)

```bash
python main.py
```

### Modo API (Servidor Web)

```bash
python -m uvicorn api.main:app --reload --port 8000
```

Luego abre en tu navegador:
- **Documentación interactiva:** http://localhost:8000/docs
- **API Base:** http://localhost:8000/api

---

## 📡 Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/chat/message` | Enviar mensaje al agente |
| `GET` | `/api/chat/stats/{session_id}` | Obtener estadísticas de sesión |
| `DELETE` | `/api/chat/clear/{session_id}` | Limpiar historial |
| `GET` | `/api/chat/sessions` | Listar sesiones activas |
| `GET` | `/health` | Health check del servidor |

### Ejemplo de Uso

```bash
curl -X POST "http://localhost:8000/api/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "mensaje": "Hola, ¿cómo estás?",
    "session_id": null
  }'
```

**Respuesta:**
```json
{
  "respuesta": "¡Hola! Muy bien, ¿en qué puedo ayudarte hoy?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-01-23T15:30:00.123456",
  "tokens_usados": null
}
```

---

## 📁 Estructura del Proyecto

```
.
├── api/                      # API REST con FastAPI
│   ├── main.py              # Servidor principal
│   ├── models/
│   │   └── schemas.py       # Modelos de datos (Pydantic)
│   └── routes/
│       └── chat.py          # Endpoints del chat
├── agentes/
│   └── agente_gemini.py     # Lógica del agente IA
├── config/
│   └── setting.py           # Configuración y variables de entorno
├── requirements/
│   └── requirements.txt     # Dependencias del proyecto
├── main.py                  # Modo consola interactivo
├── .env                     # Variables de entorno (NO SUBIR A GIT)
├── .gitignore
└── README.md
```

---

## 🛠️ Tecnologías Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno y rápido
- **[Google Gemini](https://ai.google.dev/)** - Modelo de IA generativa
- **[Pydantic](https://docs.pydantic.dev/)** - Validación de datos
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI
- **[Python-dotenv](https://pypi.org/project/python-dotenv/)** - Gestión de variables de entorno

---

## 🎯 Características

### ✅ Implementadas

- [x] Agente conversacional con Gemini
- [x] API REST con FastAPI
- [x] Gestión de sesiones
- [x] Documentación automática
- [x] Validación de datos con Pydantic
- [x] Manejo de errores robusto
- [x] CORS configurado

### 🔜 Próximas Mejoras

- [ ] Frontend con React
- [ ] Autenticación con JWT
- [ ] Persistencia con base de datos
- [ ] Rate limiting
- [ ] WebSockets para streaming
- [ ] Tests unitarios
- [ ] Dockerización
- [ ] Deploy en producción

---

## 📚 Documentación

La documentación interactiva está disponible en:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👤 Autor

**Tu Nombre**
- GitHub: [@TU_USUARIO](https://github.com/TU_USUARIO)
- LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)

---

## 🙏 Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/) por el excelente framework
- [Google](https://ai.google.dev/) por Gemini API gratuita
- Comunidad de Python por las librerías increíbles

---

## 📞 Contacto

¿Preguntas o sugerencias? Abre un [issue](https://github.com/TU_USUARIO/NOMBRE_REPO/issues) o contáctame directamente.

---

<div align="center">
  <strong>⭐ Si te gustó este proyecto, dale una estrella en GitHub ⭐</strong>
</div>
