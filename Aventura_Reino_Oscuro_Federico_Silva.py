"""
AVENTURA EN EL REINO OSCURO
Trabajo final de Paradigmas de Programacion
Nombre: Federico Fabian Silva



"""

import json
import random
import os

ARCHIVO = "partida_guardada.json"


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    input("\nPresione Enter para continuar...")


def titulo(texto):
    print("\n" + "=" * 60)
    print(texto.center(60))
    print("=" * 60)


def pedir_opcion(mensaje, opciones):
    """Pide una opcion y no permite continuar hasta que sea valida."""
    while True:
        respuesta = input(mensaje).strip()
        if respuesta in opciones:
            return respuesta
        print("Opcion incorrecta. Intente nuevamente.")


def crear_jugador():
    limpiar()
    titulo("CREACION DEL PERSONAJE")
    nombre = input("Ingrese el nombre de su personaje: ").strip()
    while nombre == "":
        nombre = input("El nombre no puede quedar vacio: ").strip()

    print("\nElija una clase:")
    print("1. Guerrero: mas vida y defensa")
    print("2. Arquero: mas posibilidad de golpe critico")
    print("3. Mago: mas ataque y energia")
    opcion = pedir_opcion("Opcion: ", ["1", "2", "3"])

    if opcion == "1":
        clase = "Guerrero"
        vida = 130
        ataque = 18
        defensa = 9
        energia = 45
        critico = 10
    elif opcion == "2":
        clase = "Arquero"
        vida = 110
        ataque = 17
        defensa = 7
        energia = 60
        critico = 22
    else:
        clase = "Mago"
        vida = 95
        ataque = 22
        defensa = 5
        energia = 85
        critico = 14

    jugador = {
        "nombre": nombre,
        "clase": clase,
        "nivel": 1,
        "experiencia": 0,
        "vida": vida,
        "vida_max": vida,
        "ataque": ataque,
        "defensa": defensa,
        "energia": energia,
        "energia_max": energia,
        "critico": critico,
        "oro": 60,
        "pociones": 3,
        "zona": 1,
        "enemigos_derrotados": 0,
        "jefe_final": False
    }
    return jugador


def mostrar_estado(jugador):
    titulo("ESTADO DEL PERSONAJE")
    print("Nombre:", jugador["nombre"])
    print("Clase:", jugador["clase"])
    print("Nivel:", jugador["nivel"])
    print("Experiencia:", jugador["experiencia"], "/", jugador["nivel"] * 100)
    print("Vida:", jugador["vida"], "/", jugador["vida_max"])
    print("Energia:", jugador["energia"], "/", jugador["energia_max"])
    print("Ataque:", jugador["ataque"])
    print("Defensa:", jugador["defensa"])
    print("Oro:", jugador["oro"])
    print("Pociones:", jugador["pociones"])
    print("Zona actual:", jugador["zona"])
    print("Enemigos derrotados:", jugador["enemigos_derrotados"])
    pausa()


def mostrar_instrucciones():
    limpiar()
    titulo("COMO JUGAR")
    print("El objetivo es recorrer las cuatro zonas del reino y derrotar")
    print("al Señor de las Sombras. Durante el recorrido se puede luchar,")
    print("descansar, comprar pociones y mejorar el personaje.")
    print("\nEn combate se puede:")
    print("- Atacar normalmente.")
    print("- Usar una habilidad que consume energia.")
    print("- Defenderse para recibir menos daño.")
    print("- Usar una pocion para recuperar vida.")
    print("- Escapar, excepto en los combates contra jefes.")
    print("\nZonas disponibles:")
    zonas = ["Bosque de los Ladrones", "Cuevas Abandonadas",
             "Campamento de los Orcos", "Castillo Oscuro"]
    for numero in range(len(zonas)):
        print(numero + 1, "-", zonas[numero])
    pausa()


def datos_enemigos(zona):
    """Devuelve una lista de enemigos posibles segun la zona."""
    if zona == 1:
        return [
            {"nombre": "Lobo salvaje", "vida": 55, "ataque": 12, "defensa": 3, "oro": 18, "exp": 30},
            {"nombre": "Bandido", "vida": 65, "ataque": 13, "defensa": 4, "oro": 24, "exp": 35}
        ]
    elif zona == 2:
        return [
            {"nombre": "Esqueleto", "vida": 80, "ataque": 16, "defensa": 5, "oro": 30, "exp": 45},
            {"nombre": "Araña gigante", "vida": 70, "ataque": 18, "defensa": 4, "oro": 28, "exp": 48}
        ]
    elif zona == 3:
        return [
            {"nombre": "Orco", "vida": 105, "ataque": 21, "defensa": 7, "oro": 42, "exp": 60},
            {"nombre": "Hechicero oscuro", "vida": 90, "ataque": 24, "defensa": 5, "oro": 48, "exp": 65}
        ]
    else:
        return [
            {"nombre": "Caballero maldito", "vida": 130, "ataque": 27, "defensa": 9, "oro": 65, "exp": 80},
            {"nombre": "Demonio menor", "vida": 120, "ataque": 29, "defensa": 7, "oro": 70, "exp": 85}
        ]


def crear_enemigo(zona):
    lista = datos_enemigos(zona)
    elegido = random.choice(lista)
    return elegido.copy()


def crear_jefe(zona):
    jefes = {
        1: {"nombre": "Jefe de los Bandidos", "vida": 115, "ataque": 18, "defensa": 6, "oro": 70, "exp": 90},
        2: {"nombre": "Reina Araña", "vida": 145, "ataque": 22, "defensa": 7, "oro": 100, "exp": 120},
        3: {"nombre": "General Orco", "vida": 180, "ataque": 27, "defensa": 10, "oro": 140, "exp": 160},
        4: {"nombre": "Señor de las Sombras", "vida": 240, "ataque": 33, "defensa": 12, "oro": 300, "exp": 300}
    }
    return jefes[zona].copy()


def calcular_daño(ataque, defensa):
    variacion = random.randint(-3, 4)
    daño = ataque + variacion - defensa
    if daño < 1:
        daño = 1
    return daño


def ataque_jugador(jugador, enemigo):
    daño = calcular_daño(jugador["ataque"], enemigo["defensa"])
    numero = random.randint(1, 100)
    if numero <= jugador["critico"]:
        daño = daño * 2
        print("¡Golpe critico!")
    enemigo["vida"] -= daño
    print("Atacaste y causaste", daño, "puntos de daño.")


def usar_habilidad(jugador, enemigo):
    costo = 20
    if jugador["energia"] < costo:
        print("No tenes energia suficiente.")
        return False

    jugador["energia"] -= costo
    if jugador["clase"] == "Guerrero":
        daño = calcular_daño(jugador["ataque"] + 12, enemigo["defensa"])
        print("Usaste Golpe demoledor.")
    elif jugador["clase"] == "Arquero":
        daño = calcular_daño(jugador["ataque"] + 8, enemigo["defensa"])
        if random.randint(1, 100) <= 35:
            daño += 10
            print("La flecha encontro un punto debil.")
        print("Usaste Flecha precisa.")
    else:
        daño = calcular_daño(jugador["ataque"] + 16, enemigo["defensa"])
        print("Usaste Bola de fuego.")

    enemigo["vida"] -= daño
    print("La habilidad causo", daño, "puntos de daño.")
    return True


def usar_pocion(jugador):
    if jugador["pociones"] <= 0:
        print("No te quedan pociones.")
        return False
    if jugador["vida"] == jugador["vida_max"]:
        print("Tu vida ya esta completa.")
        return False

    recuperacion = 45
    jugador["pociones"] -= 1
    jugador["vida"] += recuperacion
    if jugador["vida"] > jugador["vida_max"]:
        jugador["vida"] = jugador["vida_max"]
    print("Usaste una pocion. Vida actual:", jugador["vida"])
    return True


def subir_nivel(jugador):
    necesaria = jugador["nivel"] * 100
    while jugador["experiencia"] >= necesaria:
        jugador["experiencia"] -= necesaria
        jugador["nivel"] += 1
        jugador["vida_max"] += 15
        jugador["ataque"] += 3
        jugador["defensa"] += 2
        jugador["energia_max"] += 8
        jugador["vida"] = jugador["vida_max"]
        jugador["energia"] = jugador["energia_max"]
        print("\n¡Subiste al nivel", jugador["nivel"], "!")
        print("Tus estadisticas aumentaron y recuperaste toda la vida.")
        necesaria = jugador["nivel"] * 100


def combate(jugador, enemigo, es_jefe=False):
    titulo("COMBATE CONTRA " + enemigo["nombre"].upper())
    defendiendo = False

    while jugador["vida"] > 0 and enemigo["vida"] > 0:
        print("\n", jugador["nombre"], "- Vida:", jugador["vida"], "Energia:", jugador["energia"])
        print(enemigo["nombre"], "- Vida:", max(0, enemigo["vida"]))
        print("1. Atacar")
        print("2. Usar habilidad")
        print("3. Defender")
        print("4. Usar pocion")
        print("5. Escapar")
        opcion = pedir_opcion("Accion: ", ["1", "2", "3", "4", "5"])

        turno_realizado = True
        defendiendo = False

        if opcion == "1":
            ataque_jugador(jugador, enemigo)
        elif opcion == "2":
            turno_realizado = usar_habilidad(jugador, enemigo)
        elif opcion == "3":
            defendiendo = True
            print("Te preparaste para recibir el proximo ataque.")
        elif opcion == "4":
            turno_realizado = usar_pocion(jugador)
        else:
            if es_jefe:
                print("No se puede escapar de un jefe.")
                turno_realizado = False
            else:
                posibilidad = random.randint(1, 100)
                if posibilidad <= 55:
                    print("Lograste escapar.")
                    return "escape"
                print("No pudiste escapar.")

        if not turno_realizado:
            continue

        if enemigo["vida"] <= 0:
            break

        daño_enemigo = calcular_daño(enemigo["ataque"], jugador["defensa"])
        if defendiendo:
            daño_enemigo = daño_enemigo // 2
            if daño_enemigo < 1:
                daño_enemigo = 1
        jugador["vida"] -= daño_enemigo
        print(enemigo["nombre"], "te causo", daño_enemigo, "puntos de daño.")

        if jugador["energia"] < jugador["energia_max"]:
            jugador["energia"] += 5
            if jugador["energia"] > jugador["energia_max"]:
                jugador["energia"] = jugador["energia_max"]

    if jugador["vida"] <= 0:
        print("\nFuiste derrotado.")
        return "derrota"

    print("\nDerrotaste a", enemigo["nombre"])
    print("Ganaste", enemigo["oro"], "monedas y", enemigo["exp"], "de experiencia.")
    jugador["oro"] += enemigo["oro"]
    jugador["experiencia"] += enemigo["exp"]
    jugador["enemigos_derrotados"] += 1
    subir_nivel(jugador)
    return "victoria"


def tienda(jugador):
    while True:
        limpiar()
        titulo("TIENDA DEL PUEBLO")
        print("Oro disponible:", jugador["oro"])
        print("1. Comprar pocion - 25 monedas")
        print("2. Mejorar ataque - 90 monedas")
        print("3. Mejorar defensa - 80 monedas")
        print("4. Salir")
        opcion = pedir_opcion("Opcion: ", ["1", "2", "3", "4"])

        if opcion == "1":
            if jugador["oro"] >= 25:
                jugador["oro"] -= 25
                jugador["pociones"] += 1
                print("Compraste una pocion.")
            else:
                print("No tenes suficiente oro.")
        elif opcion == "2":
            if jugador["oro"] >= 90:
                jugador["oro"] -= 90
                jugador["ataque"] += 2
                print("Tu ataque aumento en 2 puntos.")
            else:
                print("No tenes suficiente oro.")
        elif opcion == "3":
            if jugador["oro"] >= 80:
                jugador["oro"] -= 80
                jugador["defensa"] += 2
                print("Tu defensa aumento en 2 puntos.")
            else:
                print("No tenes suficiente oro.")
        else:
            break
        pausa()


def descansar(jugador):
    costo = 15
    titulo("POSADA")
    if jugador["oro"] < costo:
        print("No tenes las", costo, "monedas necesarias.")
    elif jugador["vida"] == jugador["vida_max"] and jugador["energia"] == jugador["energia_max"]:
        print("No necesitas descansar.")
    else:
        jugador["oro"] -= costo
        jugador["vida"] = jugador["vida_max"]
        jugador["energia"] = jugador["energia_max"]
        print("Descansaste y recuperaste toda la vida y energia.")
    pausa()


def evento_aleatorio(jugador):
    numero = random.randint(1, 4)
    titulo("EVENTO DEL CAMINO")
    if numero == 1:
        oro = random.randint(15, 40)
        jugador["oro"] += oro
        print("Encontraste una bolsa con", oro, "monedas.")
    elif numero == 2:
        jugador["pociones"] += 1
        print("Un viajero te regalo una pocion.")
    elif numero == 3:
        daño = random.randint(5, 15)
        jugador["vida"] -= daño
        if jugador["vida"] < 1:
            jugador["vida"] = 1
        print("Caíste en una trampa y perdiste", daño, "puntos de vida.")
    else:
        energia = 20
        jugador["energia"] += energia
        if jugador["energia"] > jugador["energia_max"]:
            jugador["energia"] = jugador["energia_max"]
        print("Encontraste una fuente magica y recuperaste energia.")
    pausa()


def nombres_zonas():
    return {
        1: "Bosque de los Ladrones",
        2: "Cuevas Abandonadas",
        3: "Campamento de los Orcos",
        4: "Castillo Oscuro"
    }


def explorar(jugador):
    limpiar()
    zona = jugador["zona"]
    nombre_zona = nombres_zonas()[zona]
    titulo("EXPLORANDO: " + nombre_zona.upper())

    posibilidad = random.randint(1, 100)
    if posibilidad <= 70:
        enemigo = crear_enemigo(zona)
        resultado = combate(jugador, enemigo)
        pausa()
        return resultado
    else:
        evento_aleatorio(jugador)
        return "evento"


def enfrentar_jefe(jugador):
    zona = jugador["zona"]
    minimo = zona * 2
    if jugador["enemigos_derrotados"] < minimo:
        print("Necesitas derrotar al menos", minimo, "enemigos antes de enfrentar al jefe.")
        pausa()
        return "pendiente"

    jefe = crear_jefe(zona)
    resultado = combate(jugador, jefe, True)
    if resultado == "victoria":
        if zona < 4:
            jugador["zona"] += 1
            print("\nDesbloqueaste una nueva zona:", nombres_zonas()[jugador["zona"]])
        else:
            jugador["jefe_final"] = True
    pausa()
    return resultado


def guardar_partida(jugador):
    try:
        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump(jugador, archivo, indent=4, ensure_ascii=False)
        print("Partida guardada correctamente.")
    except OSError:
        print("No se pudo guardar la partida.")
    pausa()


def cargar_partida():
    if not os.path.exists(ARCHIVO):
        print("No existe una partida guardada.")
        pausa()
        return None
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            jugador = json.load(archivo)
        print("Partida cargada correctamente.")
        pausa()
        return jugador
    except (OSError, json.JSONDecodeError):
        print("El archivo de guardado no se pudo leer.")
        pausa()
        return None


def final_del_juego(jugador):
    limpiar()
    titulo("FINAL DEL JUEGO")
    print(jugador["nombre"], "derroto al Señor de las Sombras.")
    print("La luz regreso al reino y los pueblos volvieron a vivir en paz.")
    print("\nResumen de la partida:")
    print("Clase:", jugador["clase"])
    print("Nivel alcanzado:", jugador["nivel"])
    print("Enemigos derrotados:", jugador["enemigos_derrotados"])
    print("Oro restante:", jugador["oro"])
    print("\nGracias por jugar.")
    pausa()


def jugar(jugador):
    jugando = True
    while jugando and jugador["vida"] > 0 and not jugador["jefe_final"]:
        limpiar()
        titulo("AVENTURA EN EL REINO OSCURO")
        print("Personaje:", jugador["nombre"], "-", jugador["clase"])
        print("Zona:", nombres_zonas()[jugador["zona"]])
        print("Vida:", jugador["vida"], "/", jugador["vida_max"])
        print("\n1. Explorar")
        print("2. Enfrentar al jefe de la zona")
        print("3. Ir a la tienda")
        print("4. Descansar en la posada")
        print("5. Ver estado")
        print("6. Guardar partida")
        print("7. Volver al menu principal")
        opcion = pedir_opcion("Opcion: ", ["1", "2", "3", "4", "5", "6", "7"])

        if opcion == "1":
            explorar(jugador)
        elif opcion == "2":
            enfrentar_jefe(jugador)
        elif opcion == "3":
            tienda(jugador)
        elif opcion == "4":
            descansar(jugador)
        elif opcion == "5":
            mostrar_estado(jugador)
        elif opcion == "6":
            guardar_partida(jugador)
        else:
            jugando = False

    if jugador["jefe_final"]:
        final_del_juego(jugador)
    elif jugador["vida"] <= 0:
        titulo("FIN DE LA PARTIDA")
        print("Tu personaje fue derrotado. Podes cargar una partida anterior")
        print("o comenzar nuevamente desde el menu principal.")
        pausa()


def menu_principal():
    salir = False
    while not salir:
        limpiar()
        titulo("AVENTURA EN EL REINO OSCURO")
        print("1. Nueva partida")
        print("2. Cargar partida")
        print("3. Instrucciones")
        print("4. Salir")
        opcion = pedir_opcion("Opcion: ", ["1", "2", "3", "4"])

        if opcion == "1":
            jugador = crear_jugador()
            jugar(jugador)
        elif opcion == "2":
            jugador = cargar_partida()
            if jugador is not None:
                jugar(jugador)
        elif opcion == "3":
            mostrar_instrucciones()
        else:
            print("Gracias por jugar.")
            salir = True


if __name__ == "__main__":
    menu_principal()
