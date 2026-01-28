"""
Utilidades para sanitización de datos

RESPONSABILIDAD:
- Limpiar inputs del usuario
- Eliminar código malicioso (HTML, JavaScript, SQL)
- Prevenir inyecciones

SEGURIDAD:
- Defensa contra XSS (Cross-Site Scripting)
- Defensa contra SQL Injection
- Defensa contra HTML Injection
"""

import bleach
import re
from typing import Optional


def sanitizar_texto(texto: str) -> str:
    """
    Sanitizar texto eliminando código malicioso
    
    PROCESO:
    1. Eliminar tags HTML/JavaScript con bleach
    2. Eliminar caracteres peligrosos (<, >, etc.)
    3. Eliminar caracteres SQL peligrosos (', ", --, etc.)
    4. Limpiar espacios
    
    Args:
        texto: Texto a sanitizar
        
    Returns:
        str: Texto limpio y seguro
        
    Ejemplos:
        >>> sanitizar_texto("<script>alert('xss')</script>")
        "scriptalert('xss')/script"
        
        >>> sanitizar_texto("Juan'; DROP TABLE users; --")
        "Juan DROP TABLE users "
    """
    if not texto:
        return texto
    
    # Paso 1: Eliminar HTML/JavaScript con bleach
    # tags=[] significa que NO se permite ningún tag HTML
    # strip=True elimina los tags en lugar de escaparlos
    limpio = bleach.clean(texto, tags=[], strip=True)
    
    # Paso 2: Eliminar caracteres peligrosos para HTML
    # < y > pueden usarse para inyectar HTML
    limpio = re.sub(r'[<>]', '', limpio)
    
    # Paso 3: Eliminar caracteres peligrosos para SQL
    # ', ", --, ; pueden usarse para inyección SQL
    limpio = re.sub(r"[';\"--]", '', limpio)
    
    # Paso 4: Limpiar espacios al inicio/final
    return limpio.strip()


def sanitizar_email(email: str) -> str:
    """
    Sanitizar email (convertir a minúsculas y limpiar)
    
    PROCESO:
    1. Convertir a minúsculas
    2. Eliminar espacios
    3. Validar formato básico
    
    Args:
        email: Email a sanitizar
        
    Returns:
        str: Email limpio
        
    Ejemplos:
        >>> sanitizar_email("  JUAN@EMPRESA.COM  ")
        "juan@empresa.com"
    """
    if not email:
        return email
    
    # Convertir a minúsculas y limpiar espacios
    limpio = email.lower().strip()
    
    # Eliminar espacios internos (no deberían existir en emails)
    limpio = limpio.replace(' ', '')
    
    return limpio


def sanitizar_telefono(telefono: Optional[str]) -> Optional[str]:
    """
    Sanitizar teléfono (solo dígitos)
    
    PROCESO:
    1. Eliminar todo excepto dígitos
    2. Validar longitud
    
    Args:
        telefono: Teléfono a sanitizar
        
    Returns:
        str | None: Teléfono limpio o None
        
    Ejemplos:
        >>> sanitizar_telefono("300-123-4567")
        "3001234567"
        
        >>> sanitizar_telefono("(300) 123-4567")
        "3001234567"
    """
    if not telefono:
        return None
    
    # Eliminar todo excepto dígitos
    limpio = re.sub(r'\D', '', telefono)
    
    # Si no tiene exactamente 10 dígitos, retornar None
    if len(limpio) != 10:
        return None
    
    return limpio
