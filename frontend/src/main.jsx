/**
 * 🚀 PUNTO DE ENTRADA
 * ===================
 * 
 * Este archivo inicializa la aplicación React.
 */

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <App />
    </StrictMode>,
)
