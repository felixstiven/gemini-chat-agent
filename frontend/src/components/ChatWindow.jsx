/**
 * 💬 COMPONENTE: ChatWindow
 * ==========================
 * 
 * Ventana principal del chat que contiene:
 * - Lista de mensajes
 * - Input para escribir
 * - Lógica de comunicación con el backend
 * 
 * Este es el componente "inteligente" que maneja el estado.
 */

import { useState, useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { enviarMensaje, limpiarHistorial } from '../services/api';
import './ChatWindow.css';

export default function ChatWindow() {
    // ESTADO
    const [mensajes, setMensajes] = useState([]);
    const [sessionId, setSessionId] = useState(null);
    const [cargando, setCargando] = useState(false);
    const [error, setError] = useState(null);

    // Referencia para scroll automático
    const messagesEndRef = useRef(null);

    // Scroll automático al último mensaje
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [mensajes]);

    // Mensaje de bienvenida al cargar
    useEffect(() => {
        setMensajes([
            {
                id: 'welcome',
                message: '¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?',
                isUser: false,
                timestamp: new Date().toISOString()
            }
        ]);
    }, []);

    // Función para enviar mensaje
    const handleSendMessage = async (mensaje) => {
        try {
            setError(null);
            setCargando(true);

            // Agregar mensaje del usuario a la UI
            const mensajeUsuario = {
                id: Date.now(),
                message: mensaje,
                isUser: true,
                timestamp: new Date().toISOString()
            };
            setMensajes(prev => [...prev, mensajeUsuario]);

            // Enviar al backend
            const respuesta = await enviarMensaje(mensaje, sessionId);

            // Guardar session_id si es la primera vez
            if (!sessionId) {
                setSessionId(respuesta.session_id);
            }

            // Agregar respuesta del agente a la UI
            const mensajeAgente = {
                id: Date.now() + 1,
                message: respuesta.respuesta,
                isUser: false,
                timestamp: respuesta.timestamp
            };
            setMensajes(prev => [...prev, mensajeAgente]);

        } catch (err) {
            console.error('Error:', err);
            setError('Error al enviar el mensaje. Por favor, intenta de nuevo.');

            // Mostrar mensaje de error en el chat
            setMensajes(prev => [...prev, {
                id: Date.now() + 2,
                message: '❌ Lo siento, hubo un error. Por favor, intenta de nuevo.',
                isUser: false,
                timestamp: new Date().toISOString()
            }]);
        } finally {
            setCargando(false);
        }
    };

    // Función para limpiar el chat
    const handleClearChat = async () => {
        if (!sessionId) return;

        try {
            await limpiarHistorial(sessionId);
            setMensajes([{
                id: 'welcome-new',
                message: 'Historial limpiado. ¿En qué puedo ayudarte?',
                isUser: false,
                timestamp: new Date().toISOString()
            }]);
        } catch (err) {
            console.error('Error al limpiar:', err);
        }
    };

    return (
        <div className="chat-window">
            {/* Header */}
            <div className="chat-header">
                <div className="chat-title">
                    <span className="chat-icon">🤖</span>
                    <h1>Chat con Agente IA</h1>
                </div>
                <button
                    className="clear-button"
                    onClick={handleClearChat}
                    title="Limpiar conversación"
                >
                    🗑️
                </button>
            </div>

            {/* Mensajes */}
            <div className="chat-messages">
                {mensajes.map((msg) => (
                    <ChatMessage
                        key={msg.id}
                        message={msg.message}
                        isUser={msg.isUser}
                        timestamp={msg.timestamp}
                    />
                ))}
                {cargando && (
                    <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Error */}
            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            {/* Input */}
            <ChatInput
                onSendMessage={handleSendMessage}
                disabled={cargando}
            />
        </div>
    );
}
