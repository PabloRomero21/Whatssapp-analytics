import re
from datetime import datetime
from whatsapp_utiles import Mensaje

def leer_log_whatsapp(ruta_archivo: str) -> list[Mensaje]:
    """
    Lee un archivo de log de WhatsApp y devuelve una lista de objetos Mensaje.
    """
    mensajes = []
    
    # Patrón Regex Explicado:
    # 1. ^\[?                  -> Puede empezar con corchete (iOS)
    # 2. (\d{1,4}[/-]\d{1,2}[/-]\d{1,4}) -> Grupo 1: La Fecha (acepta / o -)
    # 3. [,\s]+                -> Separador fecha-hora (coma o espacio)
    # 4. (\d{1,2}:\d{2}(?::\d{2})?(?:\s?[apAP]\.?m\.?)?) -> Grupo 2: La Hora (HH:MM, con seg opcionales, AM/PM opcional)
    # 5. \]?:?[\s-]* -> Cierre corchete opcional, dos puntos opcionales, guión opcional
    # 6. (.*?):                -> Grupo 3: Usuario (captura todo hasta los dos puntos del mensaje)
    # 7. \s(.*)$               -> Grupo 4: El texto del mensaje
    
    patron = re.compile(
        r'^\[?(\d{1,4}[/-]\d{1,2}[/-]\d{1,4})[,\s]+(\d{1,2}:\d{2}(?::\d{2})?(?:\s?[apAP]\.?m\.?)?)\]?:?[\s-]*'
        r'(.*?):\s(.*)$'
    )

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en {ruta_archivo}")
        return []

    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue

        match = patron.match(linea)
        
        if match:
            fecha_str, hora_str, usuario, texto = match.groups()
            fecha_obj, hora_obj = _convertir_fechahora(fecha_str, hora_str)
            
            if len(usuario) > 50: 
                continue

            if fecha_obj and hora_obj:
                mensajes.append(Mensaje(fecha_obj, hora_obj, usuario, texto))
                
    return mensajes

def _convertir_fechahora(fecha_str, hora_str):
    """
    Intenta convertir strings de fecha y hora a objetos date y time
    probando varios formatos comunes.
    """
    # Formatos de fecha posibles (D/M/A, M/D/A, A-M-D, años 2 o 4 dígitos)
    formatos_fecha = [
        '%d/%m/%Y', '%d/%m/%y', # España/Latam
        '%m/%d/%y', '%m/%d/%Y', # USA
        '%Y-%m-%d'
    ]
    
    # Formatos de hora posibles
    formatos_hora = [
        '%H:%M',          # 24h simple (14:30)
        '%H:%M:%S',       # 24h con segundos
        '%I:%M %p',       # 12h (02:30 PM)
        '%I:%M:%S %p',    # 12h con segundos
        '%H:%M %p'        # Variaciones raras
    ]

    # Limpieza previa de la hora (quitar puntos en a.m./p.m. para estandarizar)
    hora_str_clean = hora_str.replace('.', '').upper()

    fecha_dt = None
    hora_dt = None

    # Intentar parsear fecha
    for fmt in formatos_fecha:
        try:
            fecha_dt = datetime.strptime(fecha_str, fmt).date()
            break
        except ValueError:
            continue

    # Intentar parsear hora
    for fmt in formatos_hora:
        try:
            hora_dt = datetime.strptime(hora_str_clean, fmt).time()
            break
        except ValueError:
            continue

    return fecha_dt, hora_dt
