/**
 * 🌐 SERVICIO API - Comunicación con el Backend
 * ============================================
 * 
 * Este archivo centraliza TODAS las llamadas al backend FastAPI.
 
// URL base del backend
// En desarrollo: http://localhost:8000
// En producción: cambiar a tu dominio
const API_BASE_URL = 'http://localhost:8000';

/**
 * Envía un mensaje al agente y recibe la respuesta
 * 
 * @param {string} mensaje - El mensaje del usuario
 * @param {string|null} sessionId - ID de sesión (null para nueva sesión)
 * @returns {Promise<Object>} Respuesta del agente
 * 
 * Ejemplo de uso:
 * ```javascript
 * const response = await enviarMensaje("Hola", null);
 * console.log(response.respuesta);
 * console.log(response.session_id);
 * ```
 */

const API_BASE_URL = 'http://localhost:8000';

export async function enviarMensaje(mensaje, sessionId = null) {
    try {
        // Hacer petición POST al backend
        const response = await fetch(`${API_BASE_URL}/api/chat/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                mensaje: mensaje,
                session_id: sessionId
            })
        });

        // Verificar si la respuesta es exitosa
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        // Parsear y retornar el JSON
        const data = await response.json();
        return data;

    } catch (error) {
        console.error('Error al enviar mensaje:', error);
        throw error;
    }
}

/**
 * Obtiene las estadísticas de una sesión
 * 
 * @param {string} sessionId - ID de la sesión
 * @returns {Promise<Object>} Estadísticas de la sesión
 */
export async function obtenerEstadisticas(sessionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/chat/stats/${sessionId}`);

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        console.error('Error al obtener estadísticas:', error);
        throw error;
    }
}

/**
 * Limpia el historial de una sesión
 * 
 * @param {string} sessionId - ID de la sesión
 * @returns {Promise<Object>} Confirmación
 */
export async function limpiarHistorial(sessionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/chat/clear/${sessionId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        console.error('Error al limpiar historial:', error);
        throw error;
    }
}

/**
 * Verifica que el backend esté funcionando
 * 
 * @returns {Promise<boolean>} true si el backend responde
 */
export async function verificarConexion() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return response.ok;
    } catch (error) {
        console.error('Backend no disponible:', error);
        return false;
    }
}
