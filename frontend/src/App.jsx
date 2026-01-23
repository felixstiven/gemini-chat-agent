/**
 * 🎨 APP PRINCIPAL
 * ================
 * 
 * Componente raíz de la aplicación.
 * Simplemente renderiza el ChatWindow.
 */

import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
    return (
        <div className="app">
            <ChatWindow />
        </div>
    );
}

export default App;
