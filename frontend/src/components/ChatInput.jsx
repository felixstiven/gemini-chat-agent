/**
 * ⌨️ COMPONENTE: ChatInput
 * =========================
 * 
 * Input para que el usuario escriba mensajes.
 * Incluye botón de envío y manejo de Enter.
 * 
 * PROPS:
 * - onSendMessage: function - Callback cuando se envía un mensaje
 * - disabled: boolean - Si está deshabilitado (esperando respuesta)
 */

import { useState } from 'react';
import './ChatInput.css';

export default function ChatInput({ onSendMessage, disabled }) {
    const [mensaje, setMensaje] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        // No enviar si está vacío o deshabilitado
        if (!mensaje.trim() || disabled) return;

        // Llamar al callback con el mensaje
        onSendMessage(mensaje);

        // Limpiar el input
        setMensaje('');
    };

    const handleKeyPress = (e) => {
        // Enviar con Enter (sin Shift)
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    return (
        <form className="chat-input-container" onSubmit={handleSubmit}>
            <input
                type="text"
                className="chat-input"
                placeholder="Escribe tu mensaje..."
                value={mensaje}
                onChange={(e) => setMensaje(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={disabled}
                autoFocus
            />
            <button
                type="submit"
                className="chat-send-button"
                disabled={disabled || !mensaje.trim()}
            >
                {disabled ? '⏳' : '→'}
            </button>
        </form>
    );
}
