/**
 * ═══════════════════════════════════════════════════════════════
 * COMPONENTE: LeadForm
 * ═══════════════════════════════════════════════════════════════
 * 
 * RESPONSABILIDAD:
 * Capturar información de contacto de leads interesados en WOG
 * 
 * CARACTERÍSTICAS:
 * - Validación en tiempo real
 * - Feedback visual inmediato
 * - Accesibilidad (a11y)
 * - No interrumpe la conversación del chat
 * 
 * PROPS:
 * @param {Function} onSubmit - Callback cuando se envían datos
 * @param {Function} onClose - Callback para cerrar el formulario
 * 
 * EJEMPLO DE USO:
 * <LeadForm 
 *   onSubmit={(data) => enviarABackend(data)}
 *   onClose={() => setShowForm(false)}
 * />
 */

import { useState } from 'react';
import './LeadForm.css';

export default function LeadForm({ onSubmit, onClose }) {

    // ESTADO DEL COMPONENTE

    const [formData, setFormData] = useState({
        empresa: '',
        nombre: '',
        email: '',
        telefono: '',
        mensaje: ''
    });
    // Errores: Almacena mensajes de error por campo
    const [errors, setErrors] = useState({});

    // isSubmitting: Indica si el formulario se esta enviando
    const [isSubmitting, setIsSubmitting] = useState(false);

    // FUNCIONES DE VALIDACIÓN
    const validarEmail = (email) => {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    };

    const validarTelefono = (telefono) => {
        const regex = /^[0-9]{10}$/;
        return regex.test(telefono);
    };

    const validarFormulario = () => {
        const nuevosErrores = {};

        // Validar empresa (requerido, no vacío)
        if (!formData.empresa.trim()) {
            nuevosErrores.empresa = 'El nombre de la empresa es requerido';
        } else if (formData.empresa.trim().length < 2) {
            nuevosErrores.empresa = 'Debe tener al menos 2 caracteres';
        }

        // Validar nombre (requerido, no vacío)
        if (!formData.nombre.trim()) {
            nuevosErrores.nombre = 'Tu nombre es requerido';
        } else if (formData.nombre.trim().length < 2) {
            nuevosErrores.nombre = 'Debe tener al menos 2 caracteres';
        }

        // Validar email (requerido, formato válido)
        if (!formData.email.trim()) {
            nuevosErrores.email = 'El email es requerido';
        } else if (!validarEmail(formData.email)) {
            nuevosErrores.email = 'Email inválido';
        }

        // Validar teléfono (opcional, pero si se proporciona debe ser válido)
        if (formData.telefono && !validarTelefono(formData.telefono)) {
            nuevosErrores.telefono = 'Teléfono debe tener 10 dígitos';
        }

        // Actualizar estado de errores
        setErrors(nuevosErrores);

        // Retornar true si no hay errores
        return Object.keys(nuevosErrores).length === 0;
    };

    // EVENT HANDLERS
    const handleChange = (e) => {
        const { name, value } = e.target;

        // Actualizar formData
        setFormData(prev => ({
            ...prev,        // Copiar todas las propiedades existentes
            [name]: value   // Sobrescribir solo la que cambió
        }));

        // Limpiar error del campo cuando el usuario empieza a escribir
        // UX: Feedback inmediato de que está corrigiendo
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''  // Limpiar solo el error de este campo
            }));
        }
    };

    // Manejar envio del formulario
    const handleSubmit = async (e) => {
        // CRÍTICO: Prevenir comportamiento por defecto
        e.preventDefault();

        // Validar formulario
        if (!validarFormulario()) {
            return;
        }

        setIsSubmitting(true);

        try {
            // Llamar a la función onSubmit del padre
            // El padre decide qué hacer con los datos
            await onSubmit(formData);

        } catch (error) {
            // Si hay error al enviar
            console.error('Error al enviar formulario:', error);

            // Mostrar error al usuario
            setErrors(prev => ({
                ...prev,
                submit: 'Error al enviar. Por favor, intenta de nuevo.'
            }));

        } finally {

            setIsSubmitting(false);
        }
    };

    // RENDER

    return (
        <div className="lead-form-overlay">
            {/* 
                OVERLAY: Fondo semi-transparente
                - Cubre toda la pantalla
                - Click fuera del formulario lo cierra
            */}
            <div
                className="lead-form-backdrop"
                onClick={onClose}
                aria-label="Cerrar formulario"
            />

            <div className="lead-form-container">
                {/* HEADER */}
                <div className="lead-form-header">
                    <h3>📋 Datos de Contacto</h3>
                    <button
                        className="close-button"
                        onClick={onClose}
                        aria-label="Cerrar formulario"
                        type="button"
                    >
                        ✕
                    </button>
                </div>

                {/* FORMULARIO */}
                <form onSubmit={handleSubmit} className="lead-form" noValidate>
                    {/* 
                        noValidate: Desactiva validación HTML5 nativa
                        Usamos nuestra propia validación en JavaScript
                    */}

                    {/* CAMPO: Empresa */}
                    <div className="form-group">
                        <label htmlFor="empresa">
                            Nombre de la Empresa *
                        </label>
                        <input
                            type="text"
                            id="empresa"
                            name="empresa"
                            value={formData.empresa}
                            onChange={handleChange}
                            className={errors.empresa ? 'error' : ''}
                            placeholder="Ej: Mi Empresa SAS"
                            aria-invalid={errors.empresa ? 'true' : 'false'}
                            aria-describedby={errors.empresa ? 'empresa-error' : undefined}
                            disabled={isSubmitting}
                        />
                        {errors.empresa && (
                            <span
                                id="empresa-error"
                                className="error-message"
                                role="alert"
                            >
                                {errors.empresa}
                            </span>
                        )}
                    </div>

                    {/* CAMPO: Nombre */}
                    <div className="form-group">
                        <label htmlFor="nombre">
                            Tu Nombre *
                        </label>
                        <input
                            type="text"
                            id="nombre"
                            name="nombre"
                            value={formData.nombre}
                            onChange={handleChange}
                            className={errors.nombre ? 'error' : ''}
                            placeholder="Ej: Juan Pérez"
                            aria-invalid={errors.nombre ? 'true' : 'false'}
                            aria-describedby={errors.nombre ? 'nombre-error' : undefined}
                            disabled={isSubmitting}
                        />
                        {errors.nombre && (
                            <span
                                id="nombre-error"
                                className="error-message"
                                role="alert"
                            >
                                {errors.nombre}
                            </span>
                        )}
                    </div>

                    {/* CAMPO: Email */}
                    <div className="form-group">
                        <label htmlFor="email">
                            Email *
                        </label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            className={errors.email ? 'error' : ''}
                            placeholder="Ej: juan@empresa.com"
                            aria-invalid={errors.email ? 'true' : 'false'}
                            aria-describedby={errors.email ? 'email-error' : undefined}
                            disabled={isSubmitting}
                        />
                        {errors.email && (
                            <span
                                id="email-error"
                                className="error-message"
                                role="alert"
                            >
                                {errors.email}
                            </span>
                        )}
                    </div>

                    {/* CAMPO: Teléfono */}
                    <div className="form-group">
                        <label htmlFor="telefono">
                            Teléfono (Opcional)
                        </label>
                        <input
                            type="tel"
                            id="telefono"
                            name="telefono"
                            value={formData.telefono}
                            onChange={handleChange}
                            className={errors.telefono ? 'error' : ''}
                            placeholder="Ej: 3001234567"
                            aria-invalid={errors.telefono ? 'true' : 'false'}
                            aria-describedby={errors.telefono ? 'telefono-error' : undefined}
                            disabled={isSubmitting}
                        />
                        {errors.telefono && (
                            <span
                                id="telefono-error"
                                className="error-message"
                                role="alert"
                            >
                                {errors.telefono}
                            </span>
                        )}
                    </div>

                    {/* CAMPO: Mensaje */}
                    <div className="form-group">
                        <label htmlFor="mensaje">
                            Mensaje (Opcional)
                        </label>
                        <textarea
                            id="mensaje"
                            name="mensaje"
                            value={formData.mensaje}
                            onChange={handleChange}
                            rows="3"
                            placeholder="Cuéntanos brevemente qué necesitas..."
                            disabled={isSubmitting}
                        />
                    </div>

                    {/* ERROR GENERAL */}
                    {errors.submit && (
                        <div className="error-message submit-error" role="alert">
                            {errors.submit}
                        </div>
                    )}

                    {/* BOTONES */}
                    <div className="form-actions">
                        <button
                            type="button"
                            onClick={onClose}
                            className="btn-secondary"
                            disabled={isSubmitting}
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            className="btn-primary"
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? 'Enviando...' : 'Enviar'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
