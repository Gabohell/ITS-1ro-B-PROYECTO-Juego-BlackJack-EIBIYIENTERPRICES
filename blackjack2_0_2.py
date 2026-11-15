# =====================================================
#  BLACKJACK en Python (2 barajas = 104 cartas)
#  Transcripcion del programa de PSeInt v2.0.2
#  - Saldo inicial: 100 pejecoins
#  - La mesa cuesta 25 pejecoins por ronda (apuesta minima)
#  - Ronda 1: apuesta de 25 pejecoins
#  - Ronda 2: opcion de DUPLICAR la apuesta (50 pejecoins) o retirarse
#  - Rondas 3 a 5: el jugador escribe cuanto apostar,
#    de 25 hasta (saldo - 1) para no quedar en ceros
#  - ALL IN: al escribir "ALL IN" apuestas TODO tu saldo
#    de una vez, sin importar cuantos pejecoins tengas
#  - Cada apuesta se resta del saldo; si le ganas al dealer,
#    la casa te paga y tu saldo aumenta
#  - Si te quedan menos de 25 pejecoins (lo que cuesta la mesa),
#    pierdes: "JUJUJU perdiste"
#  - Segunda oportunidad: la primera vez que te quedes con
#    menos de 25 pejecoins puedes pedir UN prestamo de 25 pejecoins
#  - Si terminas el juego con mas de 100 pejecoins, ganaste:
#    "EL DIAVLO ERE MUY BUENO"
#  - Empate: se devuelve la apuesta
#  - Victoria normal paga 1 a 1, Blackjack paga 3 a 2
#  - v1.5: cada carta se DIBUJA en pantalla con su valor y su palo
#  - v1.8: CHISPA, el robot crupier, reacciona con animaciones
#  - v1.9: intro de presentacion de EIBIYI
#  - v2.0: COMODINES (20% por ronda) y el legendario
#    PACTO CON EL DIAVLO (30% por partida). Se usan con (U).
#
#  Como jugar: abre una terminal (cmd, PowerShell o la de tu editor)
#  y escribe:   python blackjack2_0_2.py
#  (En IDLE la pantalla no se borra, mejor usa una terminal.)
# =====================================================

import os
import random
import time

COSTO_MESA = 25


# =====================================================
#  EQUIVALENTES DE PSeInt
# =====================================================

def borrar_pantalla():
    """Borrar Pantalla"""
    os.system("cls" if os.name == "nt" else "clear")


def esperar(ms):
    """Esperar <ms> Milisegundos"""
    time.sleep(ms / 1000)


def azar(n):
    """Azar(n): entero al azar de 0 a n-1 (igual que en PSeInt)"""
    return random.randrange(n)


def leer():
    """Leer: lee una linea del teclado (sin espacios al inicio/final)"""
    return input().strip()


# =====================================================
#  ANIMACIONES DE CHISPA
#  Todas reciben (estado, mensaje):
#    estado  -> texto que aparece arriba, en la "terminal"
#    mensaje -> texto final debajo de Chispa ("" = ninguno)
# =====================================================

def pantalla(titulo):
    borrar_pantalla()
    print("+----------------------------------------+")
    print("|  EIBIYI :: BLACKJACK :: CHISPA v2.0    |")
    print("+----------------------------------------+")
    print("  ESTADO: " + titulo)
    print("------------------------------------------")
    print()


def lineas_vacias(n):
    # range(0) no da vueltas, asi que con n = 0 no se escribe nada
    for _ in range(n):
        print()


def mensaje_final(mensaje):
    if mensaje != "":
        print()
        print("     >> " + mensaje + " <<")


# Dibujo base de Chispa
#  margen : espacios a la izquierda (para moverlo de lado)
#  antena : linea superior de la antena
#  ojos   : 3 caracteres, ej. "o o", "^ ^", "x x"
#  boca   : 1 caracter, ej. "-", "v", "~", "o"
#  brazos : 2 caracteres a cada lado del cuerpo, ej. "--", "__", "^^"
def dibujar_chispa(margen, antena, ojos, boca, brazos):
    print(margen + antena)
    print(margen + "         |")
    print(margen + "      +-----+")
    print(margen + "      | " + ojos + " |")
    print(margen + "      |  " + boca + "  |")
    print(margen + "      +-----+")
    print(margen + "    +---------+")
    print(margen + "  " + brazos + "|  [ $ ]  |" + brazos)
    print(margen + "    +---------+")
    print(margen + "       |   |")
    print(margen + "      _|   |_")


def frame_brazo_medio():
    print("         *")
    print("         |")
    print("      +-----+")
    print("      | o o |")
    print("      |  o  |")
    print("      +-----+")
    print("    +---------+   //")
    print("  --|  [ $ ]  |--//")
    print("    +---------+")
    print("       |   |")
    print("      _|   |_")


def frame_pulgar(ojos, brillo):
    print("         *        " + brillo)
    print("         |          _")
    print("      +-----+      | |")
    print("      | " + ojos + " |    __| |")
    print("      |  v  |   |    |")
    print("      +-----+   |____|")
    print("    +---------+    |")
    print("  --|  [ $ ]  |----+")
    print("    +---------+")
    print("       |   |")
    print("      _|   |_")


# ---- Pulgar arriba: le ganaste al dealer ----
def anim_pulgar_arriba(estado, mensaje):
    pantalla(estado)
    dibujar_chispa("", "         *", "o o", "-", "--")
    esperar(500)
    pantalla(estado)
    frame_brazo_medio()
    esperar(300)
    pantalla(estado)
    frame_pulgar("^ ^", "")
    esperar(400)
    pantalla(estado)
    frame_pulgar("^ -", "  *")
    esperar(350)
    pantalla(estado)
    frame_pulgar("^ ^", "*   *")
    esperar(350)
    pantalla(estado)
    frame_pulgar("^ ^", "  *")
    mensaje_final(mensaje)


# ---- Salto: Blackjack o gran victoria ----
def anim_blackjack(estado, mensaje):
    for _ in range(3):
        pantalla(estado)
        print("     *  YEAH!  *")
        dibujar_chispa("", "         *", "^ ^", "O", "^^")
        lineas_vacias(2)
        print("  ~~~~~~~~~~~~~~~~~~~~~~")
        esperar(250)
        pantalla(estado)
        lineas_vacias(3)
        dibujar_chispa("", "         *", "^ ^", "v", "--")
        print("  ~~~~~~~~~~~~~~~~~~~~~~")
        esperar(250)
    mensaje_final(mensaje)


# ---- Bust: te pasaste de 21 o te quedaste sin pejecoins ----
def anim_bust(estado, mensaje):
    pantalla("CALCULANDO...")
    dibujar_chispa("", "         *", "o o", "o", "--")
    esperar(500)
    for i in range(1, 7):
        margen = "   " if i % 2 == 0 else ""
        pantalla(estado)
        dibujar_chispa(margen, "         *", "@ @", "O", "--")
        esperar(120)
    pantalla(estado)
    dibujar_chispa("", "       *_", "x x", "~", "__")
    mensaje_final(mensaje)


# ---- Derrota: el dealer gana o te retiras ----
def anim_derrota(estado, mensaje):
    pantalla(estado)
    dibujar_chispa("", "         *", "o o", "-", "--")
    esperar(400)
    pantalla(estado)
    dibujar_chispa("", "         *", "o o", "~", "--")
    esperar(350)
    pantalla(estado)
    dibujar_chispa("", "        *", ". .", "~", "__")
    esperar(350)
    pantalla(estado)
    dibujar_chispa("", "       *_", ". ,", "n", "__")
    mensaje_final(mensaje)


# ---- Empate: Chispa mira a los lados y se encoge de hombros ----
def anim_empate(estado, mensaje):
    for i in range(1, 5):
        pantalla(estado)
        if i % 2 == 0:
            dibujar_chispa("", "         *", " oo", "-", "--")
        else:
            dibujar_chispa("", "         *", "oo ", "-", "--")
        esperar(250)
    pantalla(estado)
    dibujar_chispa("", "         *", "o o", "-", "~~")
    mensaje_final(mensaje)


# ---- Barajando: inicio del juego y cuando se rebaraja ----
def anim_barajando(estado, mensaje):
    figuras = ["[A]", "[K]", "[Q]", "[J]", "[10]"]
    for paso in range(1, 11):
        barra = "#" * paso + "." * (10 - paso)
        cartas = ""
        for j in range(5):
            cartas += figuras[(paso + j) % 5] + " "
        pantalla(estado)
        if paso % 2 == 0:
            dibujar_chispa("", "         *", "o o", "-", "--")
        else:
            dibujar_chispa("", "         *", "- -", "-", "~~")
        print()
        print("     " + cartas)
        print()
        print(f"     [{barra}] {paso * 10}%")
        esperar(200)
    mensaje_final(mensaje)


# =====================================================
#  INTRO DE EMPRESA: EIBIYI (estilo terminal retro)
#  1) La terminal "arranca" escribiendo letra por letra
#  2) Aparecen los dos hermanos chibi bajo las estrellas
#  3) Abren los ojos y miran hacia arriba (con brillo)
#  4) El nombre EIBIYI va emergiendo:  .  ->  :  ->  =  ->  #
#  5) "PRESENTA" y el copyright
# =====================================================

# Efecto maquina de escribir: muestra el texto letra por letra
# (En Python las cadenas siempre cuentan desde 0, asi que ya no hace
#  falta detectar si Subcadena empieza en 0 o en 1 como en PSeInt)
def teclear(texto):
    for car in texto:
        print(car, end="", flush=True)
        esperar(15)
    print()


# Cambia cada "#" de la linea por el caracter c
# (asi el logo va "emergiendo" de tenue a solido)
def revelar(linea, c):
    return linea.replace("#", c)


# Letras grandes del nombre EIBIYI (5 filas)
LOGO = [
    "######  ######  #####   ######  ##  ##  ######",
    "##        ##    ##  ##    ##    ##  ##    ##  ",
    "#####     ##    #####     ##     ####     ##  ",
    "##        ##    ##  ##    ##      ##      ##  ",
    "######  ######  #####   ######    ##    ######",
]


def logo_fila(f):
    return LOGO[f - 1]


# Cielo con estrellas que parpadean (3 variantes)
def estrellas(n):
    if n == 1:
        return "     .         *          .     "
    elif n == 2:
        return "     *         .          +     "
    else:
        return "     +         *          *     "


# Los dos hermanos chibi mirando hacia arriba
#  p = pupila:  "-" ojos cerrados,  "^" mirando arriba,  "*" brillo
# (las cadenas con \ llevan r delante para que Python no las tome
#  como secuencias de escape)
def dibujar_hermanos(margen, p):
    print(margen + r"    _/\/\/\_    " + r"   _/\/\/\/\_   ")
    print(margen + r"   /        \   " + r"   /        \   ")
    print(margen + "  |          |  " + "  |          |  ")
    print(margen + f"  | ({p})  ({p}) |  " + f"  | ({p})  ({p}) |  ")
    print(margen + "  |     o    |  " + "  | ~   o  ~ |  ")
    print(margen + r"   \________/   " + r"   \________/   ")
    print(margen + r"    /|    |\    " + r"    /|    |\    ")
    print(margen + r"     |_/\_|     " + r"     |_/\_|     ")


# Dibuja una escena completa del logo
#  n_estr : variante de estrellas (1 a 3)
#  pupila : ojos de los hermanos
#  etapa  : 0 = sin nombre, 1 a 4 = el nombre va emergiendo
def escena_logo(n_estr, pupila, etapa):
    borrar_pantalla()
    lineas_vacias(2)
    print("               " + estrellas(n_estr))
    print()
    dibujar_hermanos("               ", pupila)
    print()
    if etapa == 0:
        lineas_vacias(5)
    else:
        if etapa == 1:
            c = "."
        elif etapa == 2:
            c = ":"
        elif etapa == 3:
            c = "="
        else:
            c = "#"
        for f in range(1, 6):
            print("        " + revelar(logo_fila(f), c))
    print()


# Animacion completa de presentacion
def intro_eibiyi():
    # 1) Arranque de la terminal
    borrar_pantalla()
    teclear("EIBIYI SYSTEMS (R)  ::  TERMINAL DE JUEGO v2.0")
    teclear("==============================================")
    esperar(300)
    teclear("> Verificando memoria .............. 64K OK")
    teclear("> Cargando CHISPA.SYS .................. OK")
    teclear("> Preparando 2 barajas (104 cartas) .... OK")
    teclear("> Calibrando pejecoins ................. OK")
    teclear("> Cargando COMODINES.DAT ............... OK")
    teclear("> Iniciando BLACKJACK.EXE ...")
    esperar(800)

    # 2) Estrellas parpadeando y los hermanos con los ojos cerrados
    for i in range(1, 5):
        escena_logo((i % 2) + 1, "-", 0)
        esperar(300)

    # 3) Abren los ojos, miran hacia arriba y les brillan
    escena_logo(1, "^", 0)
    esperar(500)
    escena_logo(3, "*", 0)
    esperar(300)
    escena_logo(2, "^", 0)
    esperar(400)

    # 4) El nombre EIBIYI emerge poco a poco
    for i in range(1, 5):
        escena_logo((i % 3) + 1, "^", i)
        esperar(250)

    # 5) Texto de presentacion
    print("                     ", end="")
    teclear("-  P R E S E N T A  -")
    esperar(700)
    print("        ", end="")
    teclear("(C) 2026 EIBIYI. Todos los derechos reservados.")
    esperar(1500)


# =====================================================
#  CARTAS
#  Cada carta del mazo es un numero del 1 al 52:
#     1 a 13 = picas       14 a 26 = corazones
#    27 a 39 = diamantes   40 a 52 = treboles
# =====================================================

# Devuelve el valor de la carta (1 = A, 2..10, 11 = J, 12 = Q, 13 = K)
def valor_carta(carta):
    return ((carta - 1) % 13) + 1


# Devuelve el palo de la carta (1 = picas, 2 = corazones, 3 = diamantes, 4 = treboles)
def palo_carta(carta):
    return (carta - 1) // 13 + 1


# Devuelve el nombre de la carta (A, 2..10, J, Q, K)
def nombre_carta(c):
    if c == 1:
        return "A"
    elif c == 11:
        return "J"
    elif c == 12:
        return "Q"
    elif c == 13:
        return "K"
    else:
        return str(c)


# Dibujo de cada palo (4 filas)
#    picas     corazones   diamantes   treboles
#      .         _ _          ^           _
#     /.\       ( v )        / \         ( )
#    (_._)       \ /         \ /        (_|_)
#      |          v           v           |
ARTE_PALOS = {
    1: ["  .  ", r" /.\ ", "(_._)", "  |  "],
    2: [" _ _ ", "( v )", r" \ / ", "  v  "],
    3: ["  ^  ", r" / \ ", r" \ / ", "  v  "],
    4: ["  _  ", " ( ) ", "(_|_)", "  |  "],
}


# Devuelve una fila (1 a 4) del dibujo del palo
def arte_palo(palo, fila):
    return ARTE_PALOS[palo][fila - 1]


# Devuelve una linea (1 a 8) del dibujo de una carta
# Si oculta es True, dibuja la carta boca abajo
def linea_carta(linea, carta, oculta):
    if oculta:
        if linea in (1, 8):
            return "+---------+"
        elif linea in (2, 4, 6):
            return r"|/\/\/\/\/|"
        else:
            return r"|\/\/\/\/\|"

    valor = nombre_carta(valor_carta(carta))
    # El 10 ocupa dos letras; a las demas se les agrega un espacio
    if len(valor) == 1:
        izq = valor + " "
        der = " " + valor
    else:
        izq = valor
        der = valor

    if linea in (1, 8):
        return "+---------+"
    elif linea == 2:
        return "|" + izq + "       |"
    elif linea == 7:
        return "|       " + der + "|"
    else:
        return "|  " + arte_palo(palo_carta(carta), linea - 2) + "  |"


# Dibuja las cartas de una mano, una al lado de la otra
# Si con_oculta es True, agrega al final una carta boca abajo
# (la carta oculta del dealer). Maximo 6 cartas por renglon.
def dibujar_mano(cartas, con_oculta=False):
    n = len(cartas)
    total = n + 1 if con_oculta else n
    for primera in range(0, total, 6):
        ultima = min(primera + 6, total)
        for linea in range(1, 9):
            for i in range(primera, ultima):
                if i >= n:
                    print(linea_carta(linea, 1, True) + "  ", end="")
                else:
                    print(linea_carta(linea, cartas[i], False) + "  ", end="")
            print()


# Revisa que el texto escrito sea un numero entero positivo
# (sirve para que el programa no truene si se escribe algo raro)
def es_numero(texto):
    if 0 < len(texto) <= 9:
        return all("0" <= car <= "9" for car in texto)
    return False


# =====================================================
#  MAZO Y MANOS
#  En PSeInt se pasaban por referencia (mazo, pos, suma, ases...).
#  En Python se agrupan en objetos: al pasar el objeto a una
#  funcion, los cambios que haga se quedan guardados.
# =====================================================

class Mazo:
    """Las 104 cartas y la posicion de la siguiente carta a robar."""

    def __init__(self):
        self.cartas = [0] * 104
        self.pos = 0  # indice (desde 0) de la siguiente carta

    def restantes(self):
        return 104 - self.pos


class Mano:
    """Cartas de un jugador, su suma y cuantos ases valen 11."""

    def __init__(self):
        self.cartas = []
        self.suma = 0
        self.ases = 0


class Jugador:
    """Saldo, comodines y estadisticas del jugador."""

    def __init__(self):
        self.saldo = 100
        # Cada comodin es [tipo_real, tipo_visible] (maximo 2)
        self.comodines = []
        self.tiene_pacto = False
        self.usados = 0


# Arma el mazo con 2 barajas (104 cartas, sin jokers) y lo revuelve
# Cada carta (valor + palo) aparece 2 veces: una por cada baraja
def barajar(mazo):
    mazo.cartas = [(i % 52) + 1 for i in range(104)]
    # Revolver (algoritmo de Fisher-Yates)
    for i in range(103, 0, -1):
        j = random.randint(0, i)
        mazo.cartas[i], mazo.cartas[j] = mazo.cartas[j], mazo.cartas[i]
    mazo.pos = 0
    print("*** Se barajan las 2 barajas (104 cartas) ***")


# Saca la siguiente carta del mazo, la guarda en la mano
# y la suma a los puntos
# El As vale 11, pero baja a 1 si la mano se pasa de 21
def robar_carta(mazo, mano):
    if mazo.pos >= 104:
        barajar(mazo)
    c = mazo.cartas[mazo.pos]
    mazo.pos += 1
    mano.cartas.append(c)
    v = valor_carta(c)
    if v == 1:
        mano.suma += 11
        mano.ases += 1
    elif v > 10:
        mano.suma += 10
    else:
        mano.suma += v
    while mano.suma > 21 and mano.ases > 0:
        mano.suma -= 10
        mano.ases -= 1


# Recalcula la suma y los ases de una mano completa
def recalcular_mano(mano):
    mano.suma = 0
    mano.ases = 0
    for carta in mano.cartas:
        v = valor_carta(carta)
        if v == 1:
            mano.suma += 11
            mano.ases += 1
        elif v > 10:
            mano.suma += 10
        else:
            mano.suma += v
    while mano.suma > 21 and mano.ases > 0:
        mano.suma -= 10
        mano.ases -= 1


# Revuelve solo las cartas que quedan en el mazo (de pos al final)
def revolver_resto(mazo):
    for i in range(103, mazo.pos, -1):
        j = random.randint(mazo.pos, i)
        mazo.cartas[i], mazo.cartas[j] = mazo.cartas[j], mazo.cartas[i]


# =====================================================
#  COMODINES (v2.0)
#  Normales (20% de que te toque uno por ronda, maximo 2):
#    1 = RAYOS X           ves la carta oculta del dealer
#                          (30% falla: -10 pejecoins)
#    2 = CAMBIO DE CARTA   descartas tu ultima carta y sacas otra
#    3 = VISTAZO           ves la siguiente carta del mazo
#                          (35% Chispa te cacha y revuelve el mazo)
#    4 = AS BAJO LA MANGA  conviertes una carta en As
#                          (40% te cachan: pierdes la mano y -20 de multa)
#    5 = RADIACTIVO        se disfraza de uno de los 4 anteriores;
#                          al usarlo te quita 15 pejecoins
#  Legendario (30% de que aparezca UNA vez por partida):
#    PACTO CON EL DIAVLO   65% tu mano se vuelve BLACKJACK y ganas
#                          la ronda / 35% pierdes TODA la partida
# =====================================================

def nombre_comodin(t):
    if t == 1:
        return "RAYOS X"
    elif t == 2:
        return "CAMBIO DE CARTA"
    elif t == 3:
        return "VISTAZO"
    elif t == 4:
        return "AS BAJO LA MANGA"
    else:
        return "COMODIN RADIACTIVO"


def desc_comodin(t):
    if t == 1:
        return "Ves la carta oculta del dealer (30% falla: -10 pejecoins)"
    elif t == 2:
        return "Descartas tu ultima carta y sacas otra (puede salir peor)"
    elif t == 3:
        return "Ves la siguiente carta del mazo (35% Chispa revuelve el mazo)"
    else:
        return "Conviertes una carta en As (40% te cachan: pierdes y -20 de multa)"


# Quita pejecoins sin dejar el saldo en negativo
def cobrar_multa(jugador, cantidad):
    cobro = min(cantidad, jugador.saldo)
    jugador.saldo -= cobro
    print(f"  -{cobro} pejecoins. Saldo: {jugador.saldo} pejecoins.")


# Quita el comodin de la posicion indicada (1, 2, ...).
# Si la posicion no es valida no hace nada.
def quitar_comodin(jugador, posicion):
    if 1 <= posicion <= len(jugador.comodines):
        jugador.comodines.pop(posicion - 1)


# Muestra en una linea los comodines que tienes
# (si la lista esta vacia el for simplemente no da vueltas,
#  asi que aqui no existe el error que tenia la version de PSeInt)
def mostrar_comodines(jugador):
    texto = "Comodines: "
    for real, visible in jugador.comodines:
        texto += "[" + nombre_comodin(visible) + "] "
    if jugador.tiene_pacto:
        texto += "[PACTO CON EL DIAVLO]"
    print(texto)


# Pide elegir un comodin. Devuelve 0 si cancela, 1 a n para
# un comodin normal, o n + 1 para el Pacto con el DIAVLO
def elegir_comodin(jugador):
    print()
    print("--------- TUS COMODINES ---------")
    for i, (real, visible) in enumerate(jugador.comodines, start=1):
        print(f"  {i}. {nombre_comodin(visible)}: {desc_comodin(visible)}")
    max_op = len(jugador.comodines)
    if jugador.tiene_pacto:
        max_op += 1
        print(f"  {max_op}. PACTO CON EL DIAVLO: 65% BLACKJACK / 35% pierdes TODA la partida")
    print("  0. Cancelar")
    while True:
        print("Elige: ", end="")
        texto = leer()
        op = int(texto) if es_numero(texto) else -1
        if 0 <= op <= max_op:
            return op
        print("Opcion no valida.")


# Muestra la mesa: dealer con su carta oculta y tus cartas
def mostrar_mesa(mano_d, mano_j):
    print()
    print("DEALER (una carta oculta):")
    dibujar_mano(mano_d.cartas[:1], True)
    print()
    print("TUS CARTAS:")
    dibujar_mano(mano_j.cartas)
    print(f"Tus cartas suman: {mano_j.suma}")


# ---- Animacion: Chispa te entrega un comodin ----
def anim_comodin(estado, mensaje):
    for k in range(3, -1, -1):
        pantalla(estado)
        lineas_vacias(k)
        print("            [?]")
        lineas_vacias(3 - k)
        dibujar_chispa("", "         *", "o o", "o", "^^")
        esperar(250)
    pantalla(estado)
    print("          * [?] *")
    lineas_vacias(3)
    dibujar_chispa("", "         *", "^ ^", "v", "^^")
    mensaje_final(mensaje)


# ---- Animacion: Chispa se rie de ti (comodin radiactivo) ----
def anim_risa(estado, mensaje):
    for i in range(1, 7):
        pantalla(estado)
        if i % 2 == 0:
            print("          JA  JA  JA")
            dibujar_chispa("", "         *", "^ ^", "D", "^^")
        else:
            print("       JA  JA  JA")
            dibujar_chispa("  ", "         *", "> <", "O", "--")
        esperar(200)
    mensaje_final(mensaje)


# ---- Animacion: se sella el Pacto con el DIAVLO (suspenso) ----
def anim_pacto():
    for i in range(1, 11):
        pantalla("PACTO CON EL DIAVLO: SELLANDO TU DESTINO...")
        if i % 2 == 0:
            print("      >>>  B L A C K J A C K  <<<")
            dibujar_chispa("", "         *", "O O", "o", "--")
        else:
            print("      >>>  P E R D E R  T O D O  <<<")
            dibujar_chispa("", "         *", "o o", "o", "--")
        esperar(220)


# =====================================================
#  RONDA
# =====================================================

# Juega una ronda completa contra el dealer
# Devuelve: 0 = pierde (el dealer gana), 1 = empate, 2 = gana,
#           3 = gana con Blackjack, 4 = pierde por pasarse de 21,
#           5 = pierde TODA la partida (Pacto con el DIAVLO fallido),
#           6 = lo cacharon con el As bajo la manga
def jugar_ronda(mazo, jugador):
    mano_j = Mano()
    mano_d = Mano()
    resultado = 0
    terminada = False

    # Reparto inicial: 2 cartas al jugador y 2 al dealer (una boca abajo)
    robar_carta(mazo, mano_j)
    robar_carta(mazo, mano_j)
    robar_carta(mazo, mano_d)
    robar_carta(mazo, mano_d)

    mostrar_mesa(mano_d, mano_j)

    if mano_j.suma == 21:
        # Blackjack natural del jugador
        print("BLACKJACK!")
        print()
        print("Dealer voltea su carta:")
        dibujar_mano(mano_d.cartas)
        print(f"El dealer suma: {mano_d.suma}")
        if mano_d.suma == 21:
            return 1
        return 3

    # Turno del jugador
    eleccion = ""
    while mano_j.suma < 21 and eleccion != "P" and not terminada:
        hay_comodines = len(jugador.comodines) > 0 or jugador.tiene_pacto
        if hay_comodines:
            mostrar_comodines(jugador)
            print("(C) Pedir carta,  (P) Plantarte  o  (U) Usar comodin:")
        else:
            print("(C) Pedir carta  o  (P) Plantarte:")
        eleccion = leer().upper()

        if eleccion == "C":
            robar_carta(mazo, mano_j)
            print()
            print("TUS CARTAS:")
            dibujar_mano(mano_j.cartas)
            print(f"Tus cartas suman: {mano_j.suma}")

        elif eleccion == "U" and hay_comodines:
            op = elegir_comodin(jugador)
            if op > 0:
                jugador.usados += 1
                if op > len(jugador.comodines):
                    # ====== PACTO CON EL DIAVLO ======
                    jugador.tiene_pacto = False
                    anim_pacto()
                    if azar(100) < 65:
                        # Tu mano se convierte en A + K = BLACKJACK
                        mano_j.cartas = [1, 13]
                        recalcular_mano(mano_j)
                        pantalla("EL DIAVLO CUMPLIO SU PACTO")
                        print("TU MANO AHORA ES:")
                        dibujar_mano(mano_j.cartas)
                        print(f"Tus cartas suman: {mano_j.suma}")
                        print("BLACKJACK! Ganas la ronda automaticamente.")
                        resultado = 3
                    else:
                        pantalla("EL DIAVLO COBRA SU PACTO")
                        dibujar_chispa("", "       *_", "x x", "~", "__")
                        print()
                        print("El pacto salio mal... pierdes TODA la partida.")
                        resultado = 5
                    terminada = True
                else:
                    # ====== COMODIN NORMAL ======
                    tipo, vis = jugador.comodines[op - 1]
                    quitar_comodin(jugador, op)
                    print()
                    print(f">> Usas {nombre_comodin(vis)}...")

                    if tipo == 1:
                        # RAYOS X
                        if azar(100) < 70:
                            print("La carta oculta del dealer es:")
                            dibujar_mano(mano_d.cartas)
                            print(f"El dealer suma: {mano_d.suma}")
                        else:
                            print("El escaner se sobrecalento! No viste nada.")
                            cobrar_multa(jugador, 10)

                    elif tipo == 2:
                        # CAMBIO DE CARTA
                        print("Descartas tu ultima carta y sacas otra...")
                        mano_j.cartas.pop()
                        recalcular_mano(mano_j)
                        robar_carta(mazo, mano_j)
                        mostrar_mesa(mano_d, mano_j)

                    elif tipo == 3:
                        # VISTAZO
                        if mazo.pos >= 104:
                            barajar(mazo)
                        if azar(100) < 65:
                            print("La siguiente carta del mazo es:")
                            dibujar_mano([mazo.cartas[mazo.pos]])
                        else:
                            print("Chispa te cacho espiando el mazo y lo revolvio!")
                            revolver_resto(mazo)

                    elif tipo == 4:
                        # AS BAJO LA MANGA
                        n_j = len(mano_j.cartas)
                        print(f"Que carta quieres convertir en As? (1 a {n_j})")
                        while True:
                            texto = leer()
                            k = int(texto) if es_numero(texto) else 0
                            if 1 <= k <= n_j:
                                break
                            print(f"Escribe un numero del 1 al {n_j}")
                        if azar(100) < 40:
                            print("EL DEALER TE CACHO CON EL AS EN LA MANGA!")
                            resultado = 6
                            terminada = True
                        else:
                            carta = mano_j.cartas[k - 1]
                            mano_j.cartas[k - 1] = (palo_carta(carta) - 1) * 13 + 1
                            recalcular_mano(mano_j)
                            print("Nadie se dio cuenta...")
                            mostrar_mesa(mano_d, mano_j)

                    else:
                        # RADIACTIVO (estaba disfrazado)
                        anim_risa("ERA UN COMODIN RADIACTIVO!", "CHISPA SE RIE DE TI")
                        print()
                        cobrar_multa(jugador, 15)
                        mostrar_mesa(mano_d, mano_j)

        elif eleccion != "P":
            print("Opcion no valida.")

    if not terminada:
        if mano_j.suma > 21:
            print("Te pasaste de 21.")
            resultado = 4
        else:
            # Turno del dealer: voltea su carta y pide hasta tener 17 o mas
            print()
            print("Dealer voltea su carta:")
            dibujar_mano(mano_d.cartas)
            print(f"El dealer suma: {mano_d.suma}")
            while mano_d.suma < 17:
                robar_carta(mazo, mano_d)
                print()
                print("Dealer pide carta:")
                dibujar_mano(mano_d.cartas)
                print(f"El dealer suma: {mano_d.suma}")

            if mano_d.suma > 21:
                print("El dealer se paso de 21.")
                resultado = 2
            elif mano_j.suma > mano_d.suma:
                resultado = 2
            elif mano_j.suma < mano_d.suma:
                resultado = 0
            else:
                resultado = 1

    return resultado


# =====================================================
#  PROGRAMA PRINCIPAL
# =====================================================

def main():
    mazo = Mazo()
    jugador = Jugador()
    apuesta = COSTO_MESA
    ronda = 0
    prestamo_usado = False
    all_in = False
    # 0 = no jugo, 1 = se retiro, 2 = sin pejecoins para la mesa,
    # 3 = completo 5 rondas, 4 = pacto fallido
    motivo = 0

    # El Pacto con el DIAVLO tiene 30% de aparecer UNA vez por partida,
    # en una ronda al azar (1 a 5). Si no sale, ronda_pacto queda en 0.
    if azar(100) < 30:
        ronda_pacto = azar(5) + 1
    else:
        ronda_pacto = 0

    # Intro de la empresa
    intro_eibiyi()

    # Bienvenida con Chispa
    pantalla("BIENVENIDO A LA MESA")
    dibujar_chispa("", "         *", "^ ^", "v", "--")
    print()
    print("=========== BLACKJACK ===========")
    print(f"Tienes {jugador.saldo} pejecoins. Se juegan maximo 5 rondas.")
    print(f"La mesa cuesta {COSTO_MESA} pejecoins por ronda.")
    print("Cada ronda Chispa puede regalarte un COMODIN... usalo con cuidado.")
    print("Quieres jugar? (S/N)")
    respuesta = leer()
    if respuesta.upper() == "S":
        seguir = True
        barajar(mazo)
        anim_barajando("BARAJANDO 2 BARAJAS (104 CARTAS)...", "MAZO LISTO. A JUGAR!")
    else:
        seguir = False

    while seguir:
        ronda += 1

        # Si quedan menos de 20 cartas, se vuelve a barajar
        if mazo.restantes() < 20:
            barajar(mazo)
            anim_barajando("QUEDAN POCAS CARTAS: REBARAJANDO...", "MAZO NUEVO LISTO")

        # ---- Comodines: 20% por ronda (maximo 2 guardados) ----
        if len(jugador.comodines) < 2 and azar(100) < 20:
            tipo = azar(5) + 1
            if tipo == 5:
                # El radiactivo se disfraza de un comodin normal
                visible = azar(4) + 1
            else:
                visible = tipo
            jugador.comodines.append([tipo, visible])
            anim_comodin("CHISPA ENCONTRO UN COMODIN", "RECIBISTE: " + nombre_comodin(visible))
            print("     " + desc_comodin(visible))
            time.sleep(3)

        # ---- Pacto con el DIAVLO: solo en la ronda sorteada ----
        if ronda == ronda_pacto:
            jugador.tiene_pacto = True
            anim_comodin("!!! COMODIN LEGENDARIO !!!", "RECIBISTE: PACTO CON EL DIAVLO")
            print("     65% tu mano se vuelve BLACKJACK y ganas la ronda")
            print("     35% pierdes TODA la partida. Tu decides cuando usarlo...")
            time.sleep(3)

        jugador.saldo -= apuesta
        print()
        print(f"------ RONDA {ronda} de 5 | Apuesta: {apuesta} pejecoins ------")
        if all_in:
            print("************ ALL IN ************")
        print(f"Saldo despues de apostar: {jugador.saldo} pejecoins | "
              f"Cartas en el mazo: {mazo.restantes()}")

        resultado = jugar_ronda(mazo, jugador)

        # Pausa automatica para que el jugador vea las cartas antes de la animacion
        print()
        print("Chispa esta revisando la mano...")
        time.sleep(2)

        if resultado == 0:
            anim_derrota("EL DEALER GANA LA MANO", "EL DEALER TE GANO ESTA VEZ")
            print()
            print(f"Perdiste {apuesta} pejecoins.")
        elif resultado == 1:
            anim_empate("EMPATE CON EL DEALER", "NADIE GANA, NADIE PIERDE")
            print()
            print(f"Empate. Recuperas tus {apuesta} pejecoins.")
            jugador.saldo += apuesta
        elif resultado == 2:
            anim_pulgar_arriba("VICTORIA", "BIEN JUGADO! GANASTE LA MANO")
            print()
            print(f"Le ganaste al dealer! La casa te paga {apuesta} pejecoins.")
            jugador.saldo += apuesta * 2
        elif resultado == 3:
            anim_blackjack("!!! BLACKJACK !!!", "BLACKJACK! LA CASA PAGA 3 A 2")
            premio = apuesta * 3 // 2
            print()
            print(f"Ganaste con Blackjack! La casa te paga {premio} pejecoins.")
            jugador.saldo += apuesta + premio
        elif resultado == 4:
            anim_bust("ERROR: VALOR > 21", "BUST! TE PASASTE DE 21")
            print()
            print(f"Perdiste {apuesta} pejecoins.")
        elif resultado == 5:
            anim_bust("PACTO FALLIDO", "EL DIAVLO SE LLEVO TODOS TUS PEJECOINS")
            print()
            print("Pierdes TODA la partida.")
            jugador.saldo = 0
        elif resultado == 6:
            anim_derrota("TE CACHARON HACIENDO TRAMPA", "EL DEALER VIO EL AS EN TU MANGA")
            print()
            print(f"Perdiste {apuesta} pejecoins y pagas una multa de 20:")
            cobrar_multa(jugador, 20)
        print(f"Saldo actual: {jugador.saldo} pejecoins.")
        all_in = False

        if resultado == 5:
            motivo = 4
            seguir = False
        elif ronda == 5:
            motivo = 3
            seguir = False
        else:
            # Si no alcanza para pagar la mesa: prestamo (una sola vez) o pierdes
            if jugador.saldo < COSTO_MESA:
                if not prestamo_usado:
                    print(f"No te alcanza para pagar la mesa ({COSTO_MESA} pejecoins).")
                    print("Quieres un PRESTAMO de 25 pejecoins? (S/N)")
                    respuesta = leer()
                    if respuesta.upper() == "S":
                        jugador.saldo += 25
                        prestamo_usado = True
                        print(f"Recibes 25 pejecoins prestados. Ahora tienes "
                              f"{jugador.saldo} pejecoins. Es tu ultima oportunidad.")
                    else:
                        motivo = 2
                        seguir = False
                else:
                    print("No te alcanza para pagar la mesa y ya usaste tu prestamo.")
                    motivo = 2
                    seguir = False

            if seguir:
                if ronda == 1:
                    # Despues de la ronda 1: duplicar la apuesta o terminar
                    print(f"Quieres DUPLICAR la apuesta ({apuesta * 2} pejecoins) "
                          f"para la ronda 2? (S/N)")
                    respuesta = leer()
                    if respuesta.upper() == "S":
                        apuesta *= 2
                    else:
                        motivo = 1
                        seguir = False
                else:
                    # Rondas 3 a 5: apuesta libre o ALL IN
                    print(f"Quieres jugar la ronda {ronda + 1}? (S/N)")
                    respuesta = leer()
                    if respuesta.upper() == "S":
                        if jugador.saldo == COSTO_MESA:
                            # Solo alcanza para la apuesta minima: se apuesta todo
                            print(f"Solo te alcanza para la mesa: vas ALL IN con "
                                  f"{jugador.saldo} pejecoins.")
                            apuesta = jugador.saldo
                            all_in = True
                        else:
                            # Apuesta normal: de 25 a (saldo - 1) para no quedar en ceros
                            # ALL IN: apostar todo el saldo (disponible siempre)
                            maximo = jugador.saldo - 1
                            apuesta_valida = False
                            while not apuesta_valida:
                                print(f"Cuantos pejecoins quieres apostar? ({COSTO_MESA} a "
                                      f"{maximo}) o escribe ALL IN para apostar tus "
                                      f"{jugador.saldo} pejecoins")
                                texto_apuesta = leer()
                                if texto_apuesta.upper() == "ALL IN":
                                    all_in = True
                                    apuesta = jugador.saldo
                                    apuesta_valida = True
                                elif es_numero(texto_apuesta):
                                    apuesta = int(texto_apuesta)
                                    if COSTO_MESA <= apuesta <= maximo:
                                        apuesta_valida = True
                                    else:
                                        print(f"Cantidad no valida. La mesa cuesta minimo "
                                              f"{COSTO_MESA} pejecoins.")
                                else:
                                    print("Escribe una cifra o ALL IN.")
                    else:
                        motivo = 1
                        seguir = False

    # Mensaje final
    print()
    if motivo == 0:
        print("Hasta luego.")
    else:
        print()
        print("Calculando el resultado final...")
        time.sleep(2)
        if motivo == 2 or motivo == 4 or jugador.saldo < COSTO_MESA:
            anim_bust("FIN DEL JUEGO: SIN PEJECOINS", "")
            print()
            print("================================")
            print("        JUJUJU perdiste")
            print("================================")
            if motivo == 4:
                print("  (El DIAVLO cobro su pacto)")
        elif jugador.saldo > 100:
            anim_blackjack("!!! GANASTE EL JUEGO !!!", "")
            print()
            print("================================")
            print("   EL DIAVLO ERE MUY BUENO")
            print("================================")
        elif motivo == 1:
            anim_derrota("TE RETIRAS DE LA MESA", "")
            print()
            print("======= TE RETIRAS DEL JUEGO POBRE? =======")
        else:
            anim_empate("FIN DE LAS 5 RONDAS", "")
            print()
            print("======= COMPLETASTE LAS 5 RONDAS =======")
        print(f"Puntuacion final: {jugador.saldo} pejecoins.")
        print(f"Comodines usados: {jugador.usados}")
        if prestamo_usado:
            print("(Usaste el prestamo de 25 pejecoins)")

    # Igual que PSeInt, la ventana no se cierra hasta que presiones algo
    input("\nPresiona ENTER para salir...")


if __name__ == "__main__":
    main()
