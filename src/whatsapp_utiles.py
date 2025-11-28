from collections import namedtuple, Counter, defaultdict
from datetime import *

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
    res = []
    if len(mensajes) == 0 :
        return None
    res.append(mensajes[0][0])
    mensajes.reverse()
    res.append(mensajes[0][0])
    return (res[0],res[1])

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
    res =  []
    for i in mensajes:
        if ((fecha_inicio!= None) and (fecha_fin != None)):
            if (fecha_inicio <= i[0] <= fecha_fin):
                res.append(i)
        elif (fecha_fin == None) and (fecha_inicio != None):
            if (fecha_inicio <= i[0]):
                res.append(i)
        elif (fecha_inicio == None) and (fecha_fin != None): 
            if(i[0] <= fecha_fin):
                res.append(i)
        else:
            res.append(i)
    return res

def cuenta_mensajes_por_usuario(mensajes: list[Mensaje]) -> dict[str, int]:
    """
    Devuelve un diccionario con el número de mensajes por usuario.

    Parámetros:
    mensajes (list[Mensaje]): Lista de mensajes.

    Devuelve:
    dict[str, int]: Diccionario con el conteo de mensajes por usuario.
    """
    return Counter(m.usuario for m in mensajes)

def cuenta_mensajes_por_hora(mensajes: list[Mensaje]) -> dict[int, int]:
    """
    Devuelve un diccionario con el número de mensajes por hora del día (0-23).

    Parámetros:
    mensajes (list[Mensaje]): Lista de mensajes.

    Devuelve:
    dict[int, int]: Diccionario con el conteo de mensajes por hora.
    """    
    mensajes_por_hora = Counter([i.hora.hour for i in mensajes])
    return mensajes_por_hora



    
def cuenta_mensajes_por_dia_semana(mensajes: list[Mensaje]) -> dict[str, int]:
    """
    Devuelve un diccionario con el número de mensajes por día de la semana.
    Las claves deben ser los nombres de los días: Lunes, Martes...

    Parámetros:
    mensajes (list[Mensaje]): Lista de mensajes.

    Devuelve:
    dict[str, int]: Diccionario con el conteo de mensajes por día de la semana.
    """
    return Counter([DIAS_SEMANA[i.fecha.weekday()] for i in mensajes])

def calcula_longitud_media_por_usuario(mensajes: list[Mensaje]) -> dict[str, float]:
    """
    Devuelve un diccionario con la longitud media de los mensajes por usuario.

    Parámetros: 
    mensajes (list[Mensaje]): Lista de mensajes.

    Devuelve:
    dict[str, float]: Diccionario con la longitud media de los mensajes por usuario.
    """
    mensajes_por_usuario = cuenta_mensajes_por_usuario(mensajes)
    mensajes_recuento = defaultdict(int)
    for i in mensajes:
        mensajes_recuento[i.usuario] += len(i.texto)
    for i in mensajes_recuento:
        mensajes_recuento[i] = mensajes_recuento[i]/mensajes_por_usuario[i]
    return mensajes_recuento


def detecta_dia_mas_activo(mensajes: list[Mensaje]) -> tuple[date, int]|None:
    """Devuelve una tupla (fecha, numero_mensajes) del día con más actividad.

    Parámetros:
    mensajes (list[Mensaje]): Lista de mensajes.

    Devuelve:
    tuple[date, int]|None: Tupla con la fecha y el número de mensajes, o None si no hay mensajes.
    """
    if len(mensajes) == 0:
        return None
    m = Counter(m.fecha for m in mensajes)
    m = m.most_common(1)
    return (m[0][0],m[0][1])



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
    frecuencia_distintiva = Counter()
    for i in mensajes:
        palabras = i.texto
        palabras = palabras.lower()
        palabras_normalizadas = palabras.split()
        if i.usuario == usuario:

            frecuencia_distintiva.update(palabras_normalizadas)
        else:
            frecuencia_distintiva.subtract(palabras_normalizadas)
    return frecuencia_distintiva.most_common(n)


mensajes = [
        Mensaje(date(2024, 1, 1), time(10, 0), "Usuario1", "Hola mundo hola"),
        Mensaje(date(2024, 1, 2), time(11, 0), "Usuario2", "Hola adios"),
        Mensaje(date(2024, 1, 3), time(12, 0), "Usuario1", "mundo python"),
    ]
palabras = analiza_palabras_caracteristicas(mensajes, "Usuario1", n=3)    
palabras_dict = dict(palabras)
print(palabras_dict)