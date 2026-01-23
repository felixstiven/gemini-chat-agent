/**
 * 💬 COMPONENTE: ChatMessage
 * ===========================
 * 
 * Muestra un mensaje individual en el chat.
 * Puede ser del usuario o del agente.
 * 
 * PROPS:
 * - message: string - El texto del mensaje
 * - isUser: boolean - true si es del usuario, false si es del agente
 * - timestamp: string - Hora del mensaje (opcional)
 */

import './ChatMessage.css';

export default function ChatMessage({ message, isUser, timestamp }) {
    return (
        <div className={`message ${isUser ? 'message-user' : 'message-agent'}`}>
            <div className="message-avatar">
                {isUser ? '👤' : '🤖'}
            </div>
            <div className="message-content">
                <div className="message-text">{message}</div>
                {timestamp && (
                    <div className="message-timestamp">
                        {new Date(timestamp).toLocaleTimeString('es-CO', {
                            hour: '2-digit',
                            minute: '2-digit'
                        })}
                    </div>
                )}
            </div>
        </div>
    );
}
