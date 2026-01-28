"""
Modelos Pydantic para Leads

RESPONSABILIDAD:
- Definir estructura de datos de leads
- Validar tipos y formatos
- Sanitizar inputs del usuario
- Prevenir inyecciones y ataques

SEGURIDAD:
- Validación automática con Pydantic
- Sanitización de todos los campos de texto
- Límites de longitud para prevenir ataques
- Validación de formato de email y teléfono
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from utils.sanitize import sanitizar_texto, sanitizar_email, sanitizar_telefono


class LeadCreate(BaseModel):
    """
    Modelo para CREAR un lead (datos del frontend)
    
    CAMPOS REQUERIDOS:
    - empresa: Nombre de la empresa
    - nombre: Nombre del contacto
    - email: Email válido
    
    CAMPOS OPCIONALES:
    - telefono: Teléfono de 10 dígitos
    - mensaje: Mensaje adicional
    
    VALIDACIÓN:
    - Tipos correctos (str, EmailStr)
    - Longitud mínima y máxima
    - Formato de email
    - Formato de teléfono
    - Sanitización automática
    
    EJEMPLO:
        lead = LeadCreate(
            empresa="Mi Empresa SAS",
            nombre="Juan Pérez",
            email="juan@empresa.com",
            telefono="3001234567",
            mensaje="Quiero más información"
        )
    """
    
    # CAMPO: Empresa
    empresa: str = Field(
        ...,  # ... significa requerido
        min_length=2,
        max_length=100,
        description="Nombre de la empresa",
        example="Mi Empresa SAS"
    )
    
    # CAMPO: Nombre
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre completo del contacto",
        example="Juan Pérez"
    )
    
    # CAMPO: Email
    email: EmailStr = Field(
        ...,
        description="Email válido del contacto",
        example="juan@empresa.com"
    )
    
    # CAMPO: Teléfono (opcional)
    telefono: Optional[str] = Field(
        None,
        min_length=10,
        max_length=10,
        description="Teléfono de 10 dígitos",
        example="3001234567"
    )
    
    # CAMPO: Mensaje (opcional)
    mensaje: Optional[str] = Field(
        None,
        max_length=500,
        description="Mensaje adicional del contacto",
        example="Quiero más información sobre sus servicios"
    )
    
    # VALIDADOR: Empresa
    @validator('empresa')
    def validar_empresa(cls, v):
        """
        Validar y sanitizar nombre de empresa
        
        VALIDACIONES:
        1. No puede ser solo espacios
        2. Sanitizar (eliminar código malicioso)
        3. Limpiar espacios extra
        
        Args:
            v: Valor del campo empresa
            
        Returns:
            str: Empresa validada y sanitizada
            
        Raises:
            ValueError: Si la empresa es inválida
        """
        # Validar que no sea solo espacios
        if not v.strip():
            raise ValueError('El nombre de la empresa no puede estar vacío')
        
        # Sanitizar (eliminar HTML, scripts, SQL peligroso)
        sanitizado = sanitizar_texto(v)
        
        # Validar que después de sanitizar sigue teniendo contenido
        if len(sanitizado) < 2:
            raise ValueError('El nombre de la empresa debe tener al menos 2 caracteres válidos')
        
        return sanitizado
    
    # VALIDADOR: Nombre
    @validator('nombre')
    def validar_nombre(cls, v):
        """
        Validar y sanitizar nombre del contacto
        
        Similar a validar_empresa
        """
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        
        sanitizado = sanitizar_texto(v)
        
        if len(sanitizado) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres válidos')
        
        return sanitizado
    
    # VALIDADOR: Email
    @validator('email')
    def validar_email(cls, v):
        """
        Validar y sanitizar email
        
        VALIDACIONES:
        1. Formato válido (automático con EmailStr)
        2. Convertir a minúsculas
        3. Eliminar espacios
        
        Args:
            v: Valor del campo email
            
        Returns:
            str: Email validado y sanitizado
        """
        # EmailStr ya valida el formato
        # Solo necesitamos sanitizar
        return sanitizar_email(v)
    
    # VALIDADOR: Teléfono
    @validator('telefono')
    def validar_telefono(cls, v):
        """
        Validar y sanitizar teléfono
        
        VALIDACIONES:
        1. Solo dígitos
        2. Exactamente 10 dígitos
        3. Debe empezar con 3 (Colombia)
        
        Args:
            v: Valor del campo telefono
            
        Returns:
            str | None: Teléfono validado o None
            
        Raises:
            ValueError: Si el teléfono es inválido
        """
        # Si no hay teléfono, retornar None
        if not v:
            return None
        
        # Sanitizar (eliminar todo excepto dígitos)
        sanitizado = sanitizar_telefono(v)
        
        # Si después de sanitizar no tiene 10 dígitos, error
        if not sanitizado or len(sanitizado) != 10:
            raise ValueError('El teléfono debe tener exactamente 10 dígitos')
        
        # Validar que empiece con 3 (teléfonos móviles en Colombia)
        if not sanitizado.startswith('3'):
            raise ValueError('El teléfono debe empezar con 3')
        
        return sanitizado
    
    # VALIDADOR: Mensaje
    @validator('mensaje')
    def validar_mensaje(cls, v):
        """
        Validar y sanitizar mensaje
        
        VALIDACIONES:
        1. Sanitizar (eliminar código malicioso)
        2. Limitar longitud
        
        Args:
            v: Valor del campo mensaje
            
        Returns:
            str | None: Mensaje validado o None
        """
        # Si no hay mensaje, retornar None
        if not v:
            return None
        
        # Sanitizar
        sanitizado = sanitizar_texto(v)
        
        # Si después de sanitizar está vacío, retornar None
        if not sanitizado:
            return None
        
        return sanitizado
    
    class Config:
        """
        Configuración de Pydantic
        
        schema_extra: Ejemplos para documentación OpenAPI
        """
        schema_extra = {
            "example": {
                "empresa": "Mi Empresa SAS",
                "nombre": "Juan Pérez",
                "email": "juan@empresa.com",
                "telefono": "3001234567",
                "mensaje": "Quiero más información sobre el Portal Jurídico"
            }
        }


class LeadResponse(BaseModel):
    """
    Modelo para RESPONDER al frontend
    
    CAMPOS ADICIONALES (vs LeadCreate):
    - id: UUID generado por el backend
    - fecha_creacion: Timestamp de creación
    - estado: Estado del lead (nuevo, contactado, cerrado)
    
    EJEMPLO:
        lead = LeadResponse(
            id="uuid-generado",
            empresa="Mi Empresa SAS",
            nombre="Juan Pérez",
            email="juan@empresa.com",
            telefono="3001234567",
            mensaje="Quiero más información",
            fecha_creacion=datetime.now(),
            estado="nuevo"
        )
    """
    
    # Campos heredados de LeadCreate
    id: str = Field(description="UUID único del lead")
    empresa: str
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    mensaje: Optional[str] = None
    
    # Campos adicionales
    fecha_creacion: datetime = Field(
        description="Fecha y hora de creación del lead"
    )
    estado: str = Field(
        default="nuevo",
        description="Estado del lead: nuevo, contactado, cerrado"
    )
    
    class Config:
        """
        Configuración de Pydantic
        
        orm_mode: Permite crear desde objetos ORM (SQLAlchemy)
        """
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "empresa": "Mi Empresa SAS",
                "nombre": "Juan Pérez",
                "email": "juan@empresa.com",
                "telefono": "3001234567",
                "mensaje": "Quiero más información",
                "fecha_creacion": "2026-01-28T12:30:00",
                "estado": "nuevo"
            }
        }
