from collections import namedtuple, Counter, defaultdict
from datetime import date

# Nombres de los días de la semana
DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

Mensaje = namedtuple('Mensaje', ['fecha', 'hora', 'usuario', 'texto'])

def calcula_rango_fechas(mensajes: list[Mensaje])-> tuple[date, date] | None:
    """
    Devuelve el rango de fechas de los mensajes recibidos.

    Parametros:
    mensajes (list[Mensaje]): Lista de mensajes (ordenados cronológicamente).

    Devuelve:
    tuple[date, date] | None: Tupla con la fecha del primer y último mensaje, o None si la lista está vacía.
    """
    # TODO: Ejercicio 1
    pass

def filtra_mensajes_por_fechas(mensajes: list[Mensaje], fecha_inicio: date|None=None, fecha_fin: date|None=None) -> list[Mensaje]:
    """
    Filtra los mensajes comprendidos entre dos fechas (inclusive). Si
    alguna de las fechas es None, no se aplica ese límite.

    Parámetros:
    mensajes (list[Mensaje]): Lista de mensajes.
    fecha_inicio (date|None): Fecha de inicio (inclusive) o None.
    fecha_fin (date|None): Fecha de fin (inclusive) o None.

    Devuelve:
    list[Mensaje]: Lista de mensajes filtrados.
    """
    # TODO: Ejercicio 2
    pass

def cuenta_mensajes_por_usuario(mensajes: list[Mensaje]) -> dict[str, int]:
    """
    Devuelve un diccionario con el número de mensajes por usuario.

    Parámetros:
    mensajes (list[Mensaje]): Lista de mensajes.

    Devuelve:
    dict[str, int]: Diccionario con el conteo de mensajes por usuario.
    """
    # TODO: Ejercicio 3.1
    pass

def cuenta_mensajes_por_hora(mensajes: list[Mensaje]) -> dict[int, int]:
    """
    Devuelve un diccionario con el número de mensajes por hora del día (0-23).

    Parámetros:
    mensajes (list[Mensaje]): Lista de mensajes.

    Devuelve:
    dict[int, int]: Diccionario con el conteo de mensajes por hora.
    """    
    # TODO: Ejercicio 3.2
    pass
    
def cuenta_mensajes_por_dia_semana(mensajes: list[Mensaje]) -> dict[str, int]:
    """
    Devuelve un diccionario con el número de mensajes por día de la semana.
    Las claves deben ser los nombres de los días: Lunes, Martes...

    Parámetros:
    mensajes (list[Mensaje]): Lista de mensajes.

    Devuelve:
    dict[str, int]: Diccionario con el conteo de mensajes por día de la semana.
    """
    # TODO: Ejercicio 3.3
    pass

def calcula_longitud_media_por_usuario(mensajes: list[Mensaje]) -> dict[str, float]:
    """
    Devuelve un diccionario con la longitud media de los mensajes por usuario.

    Parámetros: 
    mensajes (list[Mensaje]): Lista de mensajes.

    Devuelve:
    dict[str, float]: Diccionario con la longitud media de los mensajes por usuario.
    """
    # TODO: Ejercicio 4
    pass

def detecta_dia_mas_activo(mensajes: list[Mensaje]) -> tuple[date, int]|None:
    """Devuelve una tupla (fecha, numero_mensajes) del día con más actividad.

    Parámetros:
    mensajes (list[Mensaje]): Lista de mensajes.

    Devuelve:
    tuple[date, int]|None: Tupla con la fecha y el número de mensajes, o None si no hay mensajes.
    """
    # TODO: Ejercicio 5
    pass

def analiza_palabras_caracteristicas(mensajes: list[Mensaje], usuario: str, n: int = 100) -> list[tuple[str, int]]:
    """
    Devuelve un diccionario con las n palabras más características de un usuario y sus recuentos. 
    Los recuentos se calculan sumando las apariciones de las palabras en mensajes del usuario y restando las 
    apariciones de esas palabras en mensajes de otros usuarios.

    Parámetros:
    mensajes (list[Mensaje]): Lista de mensajes.
    usuario (str): Nombre del usuario a analizar.
    n (int): Número de palabras más frecuentes a devolver.

    Devuelve:
    list[tuple[str, int]]: Lista con las n palabras más frecuentes y su conteo.
    """
    # TODO: Ejercicio 6
    pass
