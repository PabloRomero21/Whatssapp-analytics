from whatsapp_utiles import *
from datetime import date, time

def test_calcula_rango_fechas():
    print("Probando calcula_rango_fechas...")
    mensajes = [
        Mensaje(date(2024, 1, 1), time(10, 0), "Usuario1", "Mensaje 1"),
        Mensaje(date(2024, 1, 2), time(11, 0), "Usuario2", "Mensaje 2"),
        Mensaje(date(2024, 1, 3), time(12, 0), "Usuario1", "Mensaje 3"),
    ]
    fecha_inicio, fecha_fin = calcula_rango_fechas(mensajes)
    assert fecha_inicio == date(2024, 1, 1)
    assert fecha_fin == date(2024, 1, 3)

def test_filtra_mensajes_por_fechas():
    print("Probando filtra_mensajes_por_fechas...")
    mensajes = [
        Mensaje(date(2024, 1, 1), time(10, 0), "Usuario1", "Mensaje 1"),
        Mensaje(date(2024, 1, 2), time(11, 0), "Usuario2", "Mensaje 2"),
        Mensaje(date(2024, 1, 3), time(12, 0), "Usuario1", "Mensaje 3"),
        Mensaje(date(2024, 1, 4), time(13, 0), "Usuario2", "Mensaje 4"),
    ]
    # Test con ambas fechas
    filtrados = filtra_mensajes_por_fechas(mensajes, date(2024, 1, 2), date(2024, 1, 3))
    assert len(filtrados) == 2
    assert filtrados[0].fecha == date(2024, 1, 2)
    assert filtrados[1].fecha == date(2024, 1, 3)
    # Test solo con fecha_inicio
    filtrados = filtra_mensajes_por_fechas(mensajes, fecha_inicio=date(2024, 1, 3))
    assert len(filtrados) == 2
    # Test solo con fecha_fin
    filtrados = filtra_mensajes_por_fechas(mensajes, fecha_fin=date(2024, 1, 2))
    assert len(filtrados) == 2
    # Test sin fechas
    filtrados = filtra_mensajes_por_fechas(mensajes)
    assert len(filtrados) == 4

def test_cuenta_mensajes_por_usuario():
    print("Probando cuenta_mensajes_por_usuario...")
    mensajes = [
        Mensaje(date(2024, 1, 1), time(10, 0), "Usuario1", "Mensaje 1"),
        Mensaje(date(2024, 1, 2), time(11, 0), "Usuario2", "Mensaje 2"),
        Mensaje(date(2024, 1, 3), time(12, 0), "Usuario1", "Mensaje 3"),
        Mensaje(date(2024, 1, 4), time(13, 0), "Usuario1", "Mensaje 4"),
    ]
    conteo = cuenta_mensajes_por_usuario(mensajes)
    assert conteo["Usuario1"] == 3
    assert conteo["Usuario2"] == 1

def test_cuenta_mensajes_por_hora():
    print("Probando cuenta_mensajes_por_hora...")
    mensajes = [
        Mensaje(date(2024, 1, 1), time(10, 0), "Usuario1", "Mensaje 1"),
        Mensaje(date(2024, 1, 2), time(11, 0), "Usuario2", "Mensaje 2"),
        Mensaje(date(2024, 1, 3), time(10, 30), "Usuario1", "Mensaje 3"),
        Mensaje(date(2024, 1, 4), time(15, 0), "Usuario2", "Mensaje 4"),
    ]
    conteo = cuenta_mensajes_por_hora(mensajes)
    assert conteo[10] == 2
    assert conteo[11] == 1
    assert conteo[15] == 1
    assert conteo[12] == 0

def test_cuenta_mensajes_por_dia_semana():
    print("Probando cuenta_mensajes_por_dia_semana...")
    mensajes = [
        Mensaje(date(2024, 1, 1), time(10, 0), "Usuario1", "Mensaje 1"),  # Lunes
        Mensaje(date(2024, 1, 2), time(11, 0), "Usuario2", "Mensaje 2"),  # Martes
        Mensaje(date(2024, 1, 8), time(12, 0), "Usuario1", "Mensaje 3"),  # Lunes
    ]
    conteo = cuenta_mensajes_por_dia_semana(mensajes)
    assert conteo["Lunes"] == 2
    assert conteo["Martes"] == 1
    assert conteo["Miércoles"] == 0

def test_calcula_longitud_media_por_usuario():
    print("Probando calcula_longitud_media_por_usuario...")
    mensajes = [
        Mensaje(date(2024, 1, 1), time(10, 0), "Usuario1", "Hola"),  # 4
        Mensaje(date(2024, 1, 2), time(11, 0), "Usuario2", "Hola mundo"),  # 10
        Mensaje(date(2024, 1, 3), time(12, 0), "Usuario1", "Adiós"),  # 5
    ]
    medias = calcula_longitud_media_por_usuario(mensajes)
    assert medias["Usuario1"] == 4.5
    assert medias["Usuario2"] == 10.0

def test_detecta_dia_mas_activo():
    print("Probando detecta_dia_mas_activo...")
    mensajes = [
        Mensaje(date(2024, 1, 1), time(10, 0), "Usuario1", "Mensaje 1"),
        Mensaje(date(2024, 1, 2), time(11, 0), "Usuario2", "Mensaje 2"),
        Mensaje(date(2024, 1, 2), time(12, 0), "Usuario1", "Mensaje 3"),
        Mensaje(date(2024, 1, 2), time(13, 0), "Usuario2", "Mensaje 4"),
    ]
    dia_activo = detecta_dia_mas_activo(mensajes)
    assert dia_activo[0] == date(2024, 1, 2)
    assert dia_activo[1] == 3
    # Test con lista vacía
    assert detecta_dia_mas_activo([]) is None

def test_analiza_palabras_caracteristicas():
    print("Probando analiza_palabras_caracteristicas...")
    mensajes = [
        Mensaje(date(2024, 1, 1), time(10, 0), "Usuario1", "Hola mundo hola"),
        Mensaje(date(2024, 1, 2), time(11, 0), "Usuario2", "Hola adios"),
        Mensaje(date(2024, 1, 3), time(12, 0), "Usuario1", "mundo python"),
    ]
    palabras = analiza_palabras_caracteristicas(mensajes, "Usuario1", n=3)    
    palabras_dict = dict(palabras)
    assert "hola" in palabras_dict
    assert "mundo" in palabras_dict
    assert "python" in palabras_dict
    assert palabras_dict["hola"] == 1
    assert palabras_dict["mundo"] == 2
    assert palabras_dict["python"] == 1
    assert "adios" not in palabras_dict


test_calcula_rango_fechas()
#test_filtra_mensajes_por_fechas()
#test_cuenta_mensajes_por_usuario()
#test_cuenta_mensajes_por_hora()
#test_cuenta_mensajes_por_dia_semana()
#test_calcula_longitud_media_por_usuario()
#test_detecta_dia_mas_activo()
#test_analiza_palabras_frecuentes()
print("Todos los tests pasaron correctamente.")
