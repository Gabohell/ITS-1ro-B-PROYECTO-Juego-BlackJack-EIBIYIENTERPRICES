#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================
 BLACKJACK v2.0  -  EIBIYI
 Transcripcion a Python del pseudocodigo blackjack2.0.psc (PSeInt)
=====================================================
 - 2 barajas = 104 cartas
 - Saldo inicial: 100 pejecoins
 - La mesa cuesta 25 pejecoins por ronda (apuesta minima)
 - Ronda 1: apuesta de 25 pejecoins
 - Ronda 2: opcion de DUPLICAR la apuesta o retirarse
 - Rondas 3 a 5: apuesta libre de 25 a (saldo - 1), o "ALL IN"
 - Prestamo de 25 pejecoins (una sola vez) si no alcanza para la mesa
 - Victoria paga 1 a 1, Blackjack paga 3 a 2, empate devuelve la apuesta
 - Si terminas con mas de 100 pejecoins: "EL DIAVLO ERE MUY BUENO"
 - Chispa, el robot crupier, reacciona con animaciones
 - Intro de presentacion de EIBIYI
 - COMODINES: 20% por ronda de recibir uno (maximo 2) y 30% por
   partida del legendario PACTO CON EL DIAVLO

 Ejecutalo desde una terminal (CMD, PowerShell o la terminal de
 VS Code):   python blackjack2_0.py
 (En IDLE no se puede borrar la pantalla, asi que las animaciones
 se verian una debajo de otra.)
=====================================================
"""

import os
import random
import sys
import time

# ----------------- Constantes del juego -----------------
COSTO_MESA = 25
SALDO_INICIAL = 100
MAX_RONDAS = 5
TOTAL_CARTAS = 104
PRESTAMO = 25

# Resultados de una ronda
PIERDE = 0          # el dealer gana
EMPATE = 1
GANA = 2
BLACKJACK = 3
BUST = 4            # te pasaste de 21
PACTO_FALLIDO = 5   # pierdes TODA la partida
CACHADO = 6         # te cacharon con el As bajo la manga

# Comodines
RAYOS_X = 1
CAMBIO_CARTA = 2
VISTAZO = 3
AS_BAJO_LA_MANGA = 4
RADIACTIVO = 5

NOMBRES_COMODIN = {
    RAYOS_X: "RAYOS X",
    CAMBIO_CARTA: "CAMBIO DE CARTA",
    VISTAZO: "VISTAZO",
    AS_BAJO_LA_MANGA: "AS BAJO LA MANGA",
    RADIACTIVO: "COMODIN RADIACTIVO",
}

DESC_COMODIN = {
    RAYOS_X: "Ves la carta oculta del dealer (30% falla: -10 pejecoins)",
    CAMBIO_CARTA: "Descartas tu ultima carta y sacas otra (puede salir peor)",
    VISTAZO: "Ves la siguiente carta del mazo (35% Chispa revuelve el mazo)",
    AS_BAJO_LA_MANGA: "Conviertes una carta en As (40% te cachan: pierdes y -20 de multa)",
}


# =====================================================
#  UTILIDADES
# =====================================================

def esperar_ms(ms):
    """Equivale a 'Esperar X Milisegundos' de PSeInt."""
    time.sleep(ms / 1000)


def borrar_pantalla():
    """Equivale a 'Borrar Pantalla' de PSeInt."""
    os.system("cls" if os.name == "nt" else "clear")


def leer():
    """Equivale a 'Leer' de PSeInt (devuelve el texto sin espacios extra)."""
    try:
        return input().strip()
    except EOFError:
        return ""


def es_numero(texto):
    """Revisa que el texto sea un numero entero positivo (maximo 9 cifras)."""
    return 0 < len(texto) <= 9 and all(c in "0123456789" for c in texto)


def azar(probabilidad):
    """Devuelve True con la probabilidad indicada (en %)."""
    return random.randrange(100) < probabilidad


def colores_terminal():
    """Letras verdes estilo terminal retro (si la consola lo permite)."""
    if os.name == "nt":
        os.system("color 0A")          # fondo negro, letras verde claro
    else:
        print("\033[92m", end="")      # codigo ANSI para verde


# =====================================================
#  ANIMACIONES DE CHISPA
# =====================================================

def pantalla(titulo):
    borrar_pantalla()
    print("+----------------------------------------+")
    print("|  EIBIYI :: BLACKJACK :: CHISPA v2.0    |")
    print("+----------------------------------------+")
    print(f"  ESTADO: {titulo}")
    print("------------------------------------------")
    print()


def lineas_vacias(n):
    for _ in range(n):
        print()


def mensaje_final(mensaje):
    if mensaje:
        print()
        print(f"     >> {mensaje} <<")


def dibujar_chispa(margen="", antena="         *", ojos="o o", boca="-", brazos="--"):
    """Dibujo base de Chispa (ojos = 3 caracteres, boca = 1, brazos = 2)."""
    print(margen + antena)
    print(margen + "         |")
    print(margen + "      +-----+")
    print(f"{margen}      | {ojos} |")
    print(f"{margen}      |  {boca}  |")
    print(margen + "      +-----+")
    print(margen + "    +---------+")
    print(f"{margen}  {brazos}|  [ $ ]  |{brazos}")
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
    print(f"      | {ojos} |    __| |")
    print("      |  v  |   |    |")
    print("      +-----+   |____|")
    print("    +---------+    |")
    print("  --|  [ $ ]  |----+")
    print("    +---------+")
    print("       |   |")
    print("      _|   |_")


def anim_pulgar_arriba(estado, mensaje):
    """Le ganaste al dealer."""
    pantalla(estado)
    dibujar_chispa()
    esperar_ms(500)
    pantalla(estado)
    frame_brazo_medio()
    esperar_ms(300)
    for ojos, brillo, ms in (("^ ^", "", 400), ("^ -", "  *", 350), ("^ ^", "*   *", 350)):
        pantalla(estado)
        frame_pulgar(ojos, brillo)
        esperar_ms(ms)
    pantalla(estado)
    frame_pulgar("^ ^", "  *")
    mensaje_final(mensaje)


def anim_blackjack(estado, mensaje):
    """Chispa salta de emocion (Blackjack o gran victoria)."""
    for _ in range(3):
        pantalla(estado)
        print("     *  YEAH!  *")
        dibujar_chispa(ojos="^ ^", boca="O", brazos="^^")
        lineas_vacias(2)
        print("  ~~~~~~~~~~~~~~~~~~~~~~")
        esperar_ms(250)
        pantalla(estado)
        lineas_vacias(3)
        dibujar_chispa(ojos="^ ^", boca="v")
        print("  ~~~~~~~~~~~~~~~~~~~~~~")
        esperar_ms(250)
    mensaje_final(mensaje)


def anim_bust(estado, mensaje):
    """Te pasaste de 21 o te quedaste sin pejecoins."""
    pantalla("CALCULANDO...")
    dibujar_chispa(boca="o")
    esperar_ms(500)
    for i in range(1, 7):
        margen = "   " if i % 2 == 0 else ""
        pantalla(estado)
        dibujar_chispa(margen, ojos="@ @", boca="O")
        esperar_ms(120)
    pantalla(estado)
    dibujar_chispa(antena="       *_", ojos="x x", boca="~", brazos="__")
    mensaje_final(mensaje)


def anim_derrota(estado, mensaje):
    """El dealer gana o te retiras."""
    frames = (
        ("         *", "o o", "-", "--", 400),
        ("         *", "o o", "~", "--", 350),
        ("        *", ". .", "~", "__", 350),
    )
    for antena, ojos, boca, brazos, ms in frames:
        pantalla(estado)
        dibujar_chispa(antena=antena, ojos=ojos, boca=boca, brazos=brazos)
        esperar_ms(ms)
    pantalla(estado)
    dibujar_chispa(antena="       *_", ojos=". ,", boca="n", brazos="__")
    mensaje_final(mensaje)


def anim_empate(estado, mensaje):
    """Chispa mira a los lados y se encoge de hombros."""
    for i in range(1, 5):
        pantalla(estado)
        dibujar_chispa(ojos=" oo" if i % 2 == 0 else "oo ")
        esperar_ms(250)
    pantalla(estado)
    dibujar_chispa(brazos="~~")
    mensaje_final(mensaje)


def anim_barajando(estado, mensaje):
    """Inicio del juego y cuando se rebaraja el mazo."""
    figuras = ["[A]", "[K]", "[Q]", "[J]", "[10]"]
    for paso in range(1, 11):
        barra = "#" * paso + "." * (10 - paso)
        cartas = "".join(figuras[(paso + j) % 5] + " " for j in range(5))
        pantalla(estado)
        if paso % 2 == 0:
            dibujar_chispa()
        else:
            dibujar_chispa(ojos="- -", brazos="~~")
        print()
        print("     " + cartas)
        print()
        print(f"     [{barra}] {paso * 10}%")
        esperar_ms(200)
    mensaje_final(mensaje)


def anim_comodin(estado, mensaje):
    """Chispa te entrega un comodin (la carta [?] sube)."""
    for k in range(3, -1, -1):
        pantalla(estado)
        lineas_vacias(k)
        print("            [?]")
        lineas_vacias(3 - k)
        dibujar_chispa(boca="o", brazos="^^")
        esperar_ms(250)
    pantalla(estado)
    print("          * [?] *")
    lineas_vacias(3)
    dibujar_chispa(ojos="^ ^", boca="v", brazos="^^")
    mensaje_final(mensaje)


def anim_risa(estado, mensaje):
    """Chispa se rie de ti (comodin radiactivo)."""
    for i in range(1, 7):
        pantalla(estado)
        if i % 2 == 0:
            print("          JA  JA  JA")
            dibujar_chispa(ojos="^ ^", boca="D", brazos="^^")
        else:
            print("       JA  JA  JA")
            dibujar_chispa("  ", ojos="> <", boca="O")
        esperar_ms(200)
    mensaje_final(mensaje)


def anim_pacto():
    """Suspenso mientras se sella el Pacto con el DIAVLO."""
    for i in range(1, 11):
        pantalla("PACTO CON EL DIAVLO: SELLANDO TU DESTINO...")
        if i % 2 == 0:
            print("      >>>  B L A C K J A C K  <<<")
            dibujar_chispa(ojos="O O", boca="o")
        else:
            print("      >>>  P E R D E R  T O D O  <<<")
            dibujar_chispa(boca="o")
        esperar_ms(220)


# =====================================================
#  INTRO DE EMPRESA: EIBIYI (estilo terminal retro)
# =====================================================

LOGO_EIBIYI = [
    "######  ######  #####   ######  ##  ##  ######",
    "##        ##    ##  ##    ##    ##  ##    ##  ",
    "#####     ##    #####     ##     ####     ##  ",
    "##        ##    ##  ##    ##      ##      ##  ",
    "######  ######  #####   ######    ##    ######",
]

ESTRELLAS = [
    "     .         *          .     ",
    "     *         .          +     ",
    "     +         *          *     ",
]


def teclear(texto, ms=15):
    """Efecto maquina de escribir: muestra el texto letra por letra."""
    for letra in texto:
        print(letra, end="", flush=True)
        esperar_ms(ms)
    print()


def revelar(linea, c):
    """Cambia cada '#' por c, para que el logo vaya 'emergiendo'."""
    return linea.replace("#", c)


def dibujar_hermanos(margen, p):
    """Los dos hermanos chibi mirando hacia arriba (p = pupila)."""
    print(margen + r"    _/\/\/\_    " + r"   _/\/\/\/\_   ")
    print(margen + r"   /        \   " + r"   /        \   ")
    print(margen + "  |          |  " + "  |          |  ")
    print(margen + f"  | ({p})  ({p}) |  " + f"  | ({p})  ({p}) |  ")
    print(margen + "  |     o    |  " + "  | ~   o  ~ |  ")
    print(margen + r"   \________/   " + r"   \________/   ")
    print(margen + r"    /|    |\    " + r"    /|    |\    ")
    print(margen + r"     |_/\_|     " + r"     |_/\_|     ")


def escena_logo(n_estr, pupila, etapa):
    """etapa 0 = sin nombre; 1 a 4 = el nombre va emergiendo."""
    borrar_pantalla()
    lineas_vacias(2)
    print(" " * 15 + ESTRELLAS[n_estr - 1])
    print()
    dibujar_hermanos(" " * 15, pupila)
    print()
    if etapa == 0:
        lineas_vacias(5)
    else:
        c = {1: ".", 2: ":", 3: "="}.get(etapa, "#")
        for fila in LOGO_EIBIYI:
            print(" " * 8 + revelar(fila, c))
    print()


def intro_eibiyi():
    # 1) Arranque de la terminal
    borrar_pantalla()
    teclear("EIBIYI SYSTEMS (R)  ::  TERMINAL DE JUEGO v2.0")
    teclear("==============================================")
    esperar_ms(300)
    teclear("> Verificando memoria .............. 64K OK")
    teclear("> Cargando CHISPA.SYS .................. OK")
    teclear("> Preparando 2 barajas (104 cartas) .... OK")
    teclear("> Calibrando pejecoins ................. OK")
    teclear("> Cargando COMODINES.DAT ............... OK")
    teclear("> Iniciando BLACKJACK.EXE ...")
    esperar_ms(800)

    # 2) Estrellas parpadeando y los hermanos con los ojos cerrados
    for i in range(1, 5):
        escena_logo((i % 2) + 1, "-", 0)
        esperar_ms(300)

    # 3) Abren los ojos, miran hacia arriba y les brillan
    escena_logo(1, "^", 0)
    esperar_ms(500)
    escena_logo(3, "*", 0)
    esperar_ms(300)
    escena_logo(2, "^", 0)
    esperar_ms(400)

    # 4) El nombre EIBIYI emerge poco a poco
    for i in range(1, 5):
        escena_logo((i % 3) + 1, "^", i)
        esperar_ms(250)

    # 5) Texto de presentacion
    print(" " * 21, end="")
    teclear("-  P R E S E N T A  -")
    esperar_ms(700)
    print(" " * 8, end="")
    teclear("(C) 2026 EIBIYI. Todos los derechos reservados.")
    esperar_ms(1500)


# =====================================================
#  CARTAS
#  Cada carta es un numero del 1 al 52:
#     1 a 13 = picas        14 a 26 = corazones
#    27 a 39 = diamantes    40 a 52 = treboles
# =====================================================

ARTE_PALOS = {
    1: ["  .  ", r" /.\ ", "(_._)", "  |  "],   # picas
    2: [" _ _ ", "( v )", r" \ / ", "  v  "],   # corazones
    3: ["  ^  ", r" / \ ", r" \ / ", "  v  "],  # diamantes
    4: ["  _  ", " ( ) ", "(_|_)", "  |  "],    # treboles
}


def valor_carta(carta):
    """1 = A, 2..10, 11 = J, 12 = Q, 13 = K"""
    return (carta - 1) % 13 + 1


def palo_carta(carta):
    """1 = picas, 2 = corazones, 3 = diamantes, 4 = treboles"""
    return (carta - 1) // 13 + 1


def nombre_carta(valor):
    return {1: "A", 11: "J", 12: "Q", 13: "K"}.get(valor, str(valor))


def linea_carta(linea, carta, oculta):
    """Devuelve la linea (1 a 8) del dibujo de una carta."""
    if oculta:
        if linea in (1, 8):
            return "+---------+"
        if linea in (2, 4, 6):
            return r"|/\/\/\/\/|"
        return r"|\/\/\/\/\|"
    valor = nombre_carta(valor_carta(carta))
    izq = valor.ljust(2)   # el 10 ocupa dos letras; a las demas se les agrega un espacio
    der = valor.rjust(2)
    if linea in (1, 8):
        return "+---------+"
    if linea == 2:
        return f"|{izq}       |"
    if linea == 7:
        return f"|       {der}|"
    return f"|  {ARTE_PALOS[palo_carta(carta)][linea - 3]}  |"


def dibujar_mano(cartas, con_oculta=False):
    """Dibuja las cartas una al lado de la otra (maximo 6 por renglon).
    Si con_oculta es True, agrega al final una carta boca abajo."""
    total = len(cartas) + (1 if con_oculta else 0)
    for primera in range(0, total, 6):
        ultima = min(primera + 6, total)
        for linea in range(1, 9):
            renglon = ""
            for i in range(primera, ultima):
                if i >= len(cartas):
                    renglon += linea_carta(linea, 1, True) + "  "
                else:
                    renglon += linea_carta(linea, cartas[i], False) + "  "
            print(renglon)


class Mazo:
    """Dos barajas (104 cartas, sin jokers)."""

    def __init__(self):
        self.cartas = []
        self.pos = 0
        self.barajar()

    def barajar(self):
        self.cartas = [(i % 52) + 1 for i in range(TOTAL_CARTAS)]
        # Revolver (algoritmo de Fisher-Yates)
        for i in range(TOTAL_CARTAS - 1, 0, -1):
            j = random.randint(0, i)
            self.cartas[i], self.cartas[j] = self.cartas[j], self.cartas[i]
        self.pos = 0
        print("*** Se barajan las 2 barajas (104 cartas) ***")

    def restantes(self):
        return TOTAL_CARTAS - self.pos

    def sacar(self):
        if self.pos >= TOTAL_CARTAS:
            self.barajar()
        carta = self.cartas[self.pos]
        self.pos += 1
        return carta

    def ver_siguiente(self):
        if self.pos >= TOTAL_CARTAS:
            self.barajar()
        return self.cartas[self.pos]

    def revolver_resto(self):
        """Revuelve solo las cartas que aun no salen."""
        resto = self.cartas[self.pos:]
        random.shuffle(resto)
        self.cartas[self.pos:] = resto


class Mano:
    """Cartas de un jugador con su suma (el As vale 11 o 1)."""

    def __init__(self):
        self.cartas = []
        self.suma = 0
        self.ases = 0

    def recalcular(self):
        self.suma = 0
        self.ases = 0
        for carta in self.cartas:
            v = valor_carta(carta)
            if v == 1:
                self.suma += 11
                self.ases += 1
            elif v > 10:
                self.suma += 10
            else:
                self.suma += v
        while self.suma > 21 and self.ases > 0:
            self.suma -= 10
            self.ases -= 1

    def agregar(self, carta):
        self.cartas.append(carta)
        self.recalcular()


class Jugador:
    def __init__(self):
        self.saldo = SALDO_INICIAL
        self.inventario = []     # lista de (tipo_real, tipo_visible)
        self.tiene_pacto = False
        self.usados = 0


# =====================================================
#  COMODINES
# =====================================================

def cobrar_multa(jugador, cantidad):
    """Quita pejecoins sin dejar el saldo en negativo."""
    cobro = min(cantidad, jugador.saldo)
    jugador.saldo -= cobro
    print(f"  -{cobro} pejecoins. Saldo: {jugador.saldo} pejecoins.")


def mostrar_comodines(jugador):
    texto = "Comodines: "
    for _, visible in jugador.inventario:
        texto += f"[{NOMBRES_COMODIN[visible]}] "
    if jugador.tiene_pacto:
        texto += "[PACTO CON EL DIAVLO]"
    print(texto)


def elegir_comodin(jugador):
    """Devuelve 0 si cancela, 1..n para un comodin normal,
    o n + 1 para el Pacto con el DIAVLO."""
    print()
    print("--------- TUS COMODINES ---------")
    for i, (_, visible) in enumerate(jugador.inventario, start=1):
        print(f"  {i}. {NOMBRES_COMODIN[visible]}: {DESC_COMODIN[visible]}")
    max_op = len(jugador.inventario)
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


def mostrar_mesa(dealer, mano):
    print()
    print("DEALER (una carta oculta):")
    dibujar_mano(dealer.cartas[:1], con_oculta=True)
    print()
    print("TUS CARTAS:")
    dibujar_mano(mano.cartas)
    print(f"Tus cartas suman: {mano.suma}")


def usar_comodin(mazo, jugador, dealer, mano):
    """Usa un comodin. Devuelve un resultado si la ronda termina,
    o None si el juego sigue."""
    op = elegir_comodin(jugador)
    if op == 0:
        return None
    jugador.usados += 1

    # ====== PACTO CON EL DIAVLO ======
    if op > len(jugador.inventario):
        jugador.tiene_pacto = False
        anim_pacto()
        if azar(65):
            mano.cartas = [1, 13]          # A + K de picas = BLACKJACK
            mano.recalcular()
            pantalla("EL DIAVLO CUMPLIO SU PACTO")
            print("TU MANO AHORA ES:")
            dibujar_mano(mano.cartas)
            print(f"Tus cartas suman: {mano.suma}")
            print("BLACKJACK! Ganas la ronda automaticamente.")
            return BLACKJACK
        pantalla("EL DIAVLO COBRA SU PACTO")
        dibujar_chispa(antena="       *_", ojos="x x", boca="~", brazos="__")
        print()
        print("El pacto salio mal... pierdes TODA la partida.")
        return PACTO_FALLIDO

    # ====== COMODIN NORMAL ======
    tipo, visible = jugador.inventario.pop(op - 1)
    print()
    print(f">> Usas {NOMBRES_COMODIN[visible]}...")

    if tipo == RAYOS_X:
        if azar(70):
            print("La carta oculta del dealer es:")
            dibujar_mano(dealer.cartas)
            print(f"El dealer suma: {dealer.suma}")
        else:
            print("El escaner se sobrecalento! No viste nada.")
            cobrar_multa(jugador, 10)

    elif tipo == CAMBIO_CARTA:
        print("Descartas tu ultima carta y sacas otra...")
        mano.cartas.pop()
        mano.agregar(mazo.sacar())
        mostrar_mesa(dealer, mano)

    elif tipo == VISTAZO:
        if azar(65):
            print("La siguiente carta del mazo es:")
            dibujar_mano([mazo.ver_siguiente()])
        else:
            print("Chispa te cacho espiando el mazo y lo revolvio!")
            mazo.revolver_resto()

    elif tipo == AS_BAJO_LA_MANGA:
        n = len(mano.cartas)
        print(f"Que carta quieres convertir en As? (1 a {n})")
        while True:
            texto = leer()
            k = int(texto) if es_numero(texto) else 0
            if 1 <= k <= n:
                break
            print(f"Escribe un numero del 1 al {n}")
        if azar(40):
            print("EL DEALER TE CACHO CON EL AS EN LA MANGA!")
            return CACHADO
        carta = mano.cartas[k - 1]
        mano.cartas[k - 1] = (palo_carta(carta) - 1) * 13 + 1
        mano.recalcular()
        print("Nadie se dio cuenta...")
        mostrar_mesa(dealer, mano)

    else:  # RADIACTIVO (estaba disfrazado)
        anim_risa("ERA UN COMODIN RADIACTIVO!", "CHISPA SE RIE DE TI")
        print()
        cobrar_multa(jugador, 15)
        mostrar_mesa(dealer, mano)

    return None


# =====================================================
#  RONDA
# =====================================================

def jugar_ronda(mazo, jugador):
    """Juega una ronda completa contra el dealer y devuelve el resultado."""
    mano = Mano()
    dealer = Mano()

    # Reparto inicial: 2 cartas al jugador y 2 al dealer (una boca abajo)
    mano.agregar(mazo.sacar())
    mano.agregar(mazo.sacar())
    dealer.agregar(mazo.sacar())
    dealer.agregar(mazo.sacar())

    mostrar_mesa(dealer, mano)

    if mano.suma == 21:
        # Blackjack natural del jugador
        print("BLACKJACK!")
        print()
        print("Dealer voltea su carta:")
        dibujar_mano(dealer.cartas)
        print(f"El dealer suma: {dealer.suma}")
        return EMPATE if dealer.suma == 21 else BLACKJACK

    # Turno del jugador
    eleccion = ""
    while mano.suma < 21 and eleccion != "P":
        tiene_comodines = bool(jugador.inventario) or jugador.tiene_pacto
        if tiene_comodines:
            mostrar_comodines(jugador)
            print("(C) Pedir carta,  (P) Plantarte  o  (U) Usar comodin:")
        else:
            print("(C) Pedir carta  o  (P) Plantarte:")
        eleccion = leer().upper()

        if eleccion == "C":
            mano.agregar(mazo.sacar())
            print()
            print("TUS CARTAS:")
            dibujar_mano(mano.cartas)
            print(f"Tus cartas suman: {mano.suma}")
        elif eleccion == "U" and tiene_comodines:
            resultado = usar_comodin(mazo, jugador, dealer, mano)
            if resultado is not None:
                return resultado
        elif eleccion != "P":
            print("Opcion no valida.")

    if mano.suma > 21:
        print("Te pasaste de 21.")
        return BUST

    # Turno del dealer: voltea su carta y pide hasta tener 17 o mas
    print()
    print("Dealer voltea su carta:")
    dibujar_mano(dealer.cartas)
    print(f"El dealer suma: {dealer.suma}")
    while dealer.suma < 17:
        dealer.agregar(mazo.sacar())
        print()
        print("Dealer pide carta:")
        dibujar_mano(dealer.cartas)
        print(f"El dealer suma: {dealer.suma}")

    if dealer.suma > 21:
        print("El dealer se paso de 21.")
        return GANA
    if mano.suma > dealer.suma:
        return GANA
    if mano.suma < dealer.suma:
        return PIERDE
    return EMPATE


# =====================================================
#  PROGRAMA PRINCIPAL
# =====================================================

def main():
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
    ronda_pacto = random.randint(1, MAX_RONDAS) if azar(30) else 0

    colores_terminal()

    # Intro de la empresa
    intro_eibiyi()

    # Bienvenida con Chispa
    pantalla("BIENVENIDO A LA MESA")
    dibujar_chispa(ojos="^ ^", boca="v")
    print()
    print("=========== BLACKJACK ===========")
    print(f"Tienes {jugador.saldo} pejecoins. Se juegan maximo {MAX_RONDAS} rondas.")
    print(f"La mesa cuesta {COSTO_MESA} pejecoins por ronda.")
    print("Cada ronda Chispa puede regalarte un COMODIN... usalo con cuidado.")
    print("Quieres jugar? (S/N)")
    seguir = leer().upper() == "S"

    mazo = None
    if seguir:
        mazo = Mazo()
        anim_barajando("BARAJANDO 2 BARAJAS (104 CARTAS)...", "MAZO LISTO. A JUGAR!")

    while seguir:
        ronda += 1

        # Si quedan menos de 20 cartas, se vuelve a barajar
        if mazo.restantes() < 20:
            mazo.barajar()
            anim_barajando("QUEDAN POCAS CARTAS: REBARAJANDO...", "MAZO NUEVO LISTO")

        # ---- Comodines: 20% por ronda (maximo 2 guardados) ----
        if len(jugador.inventario) < 2 and azar(20):
            tipo = random.randint(1, 5)
            # El radiactivo se disfraza de un comodin normal
            visible = random.randint(1, 4) if tipo == RADIACTIVO else tipo
            jugador.inventario.append((tipo, visible))
            anim_comodin("CHISPA ENCONTRO UN COMODIN", f"RECIBISTE: {NOMBRES_COMODIN[visible]}")
            print(f"     {DESC_COMODIN[visible]}")
            esperar_ms(3000)

        # ---- Pacto con el DIAVLO: solo en la ronda sorteada ----
        if ronda == ronda_pacto:
            jugador.tiene_pacto = True
            anim_comodin("!!! COMODIN LEGENDARIO !!!", "RECIBISTE: PACTO CON EL DIAVLO")
            print("     65% tu mano se vuelve BLACKJACK y ganas la ronda")
            print("     35% pierdes TODA la partida. Tu decides cuando usarlo...")
            esperar_ms(3000)

        jugador.saldo -= apuesta
        print()
        print(f"------ RONDA {ronda} de {MAX_RONDAS} | Apuesta: {apuesta} pejecoins ------")
        if all_in:
            print("************ ALL IN ************")
        print(f"Saldo despues de apostar: {jugador.saldo} pejecoins | "
              f"Cartas en el mazo: {mazo.restantes()}")

        resultado = jugar_ronda(mazo, jugador)

        # Pausa automatica para que el jugador vea las cartas antes de la animacion
        print()
        print("Chispa esta revisando la mano...")
        esperar_ms(2000)

        if resultado == PIERDE:
            anim_derrota("EL DEALER GANA LA MANO", "EL DEALER TE GANO ESTA VEZ")
            print()
            print(f"Perdiste {apuesta} pejecoins.")
        elif resultado == EMPATE:
            anim_empate("EMPATE CON EL DEALER", "NADIE GANA, NADIE PIERDE")
            print()
            print(f"Empate. Recuperas tus {apuesta} pejecoins.")
            jugador.saldo += apuesta
        elif resultado == GANA:
            anim_pulgar_arriba("VICTORIA", "BIEN JUGADO! GANASTE LA MANO")
            print()
            print(f"Le ganaste al dealer! La casa te paga {apuesta} pejecoins.")
            jugador.saldo += apuesta * 2
        elif resultado == BLACKJACK:
            anim_blackjack("!!! BLACKJACK !!!", "BLACKJACK! LA CASA PAGA 3 A 2")
            premio = apuesta * 3 // 2
            print()
            print(f"Ganaste con Blackjack! La casa te paga {premio} pejecoins.")
            jugador.saldo += apuesta + premio
        elif resultado == BUST:
            anim_bust("ERROR: VALOR > 21", "BUST! TE PASASTE DE 21")
            print()
            print(f"Perdiste {apuesta} pejecoins.")
        elif resultado == PACTO_FALLIDO:
            anim_bust("PACTO FALLIDO", "EL DIAVLO SE LLEVO TODOS TUS PEJECOINS")
            print()
            print("Pierdes TODA la partida.")
            jugador.saldo = 0
        elif resultado == CACHADO:
            anim_derrota("TE CACHARON HACIENDO TRAMPA", "EL DEALER VIO EL AS EN TU MANGA")
            print()
            print(f"Perdiste {apuesta} pejecoins y pagas una multa de 20:")
            cobrar_multa(jugador, 20)

        print(f"Saldo actual: {jugador.saldo} pejecoins.")
        all_in = False

        if resultado == PACTO_FALLIDO:
            motivo = 4
            seguir = False
        elif ronda == MAX_RONDAS:
            motivo = 3
            seguir = False
        else:
            # Si no alcanza para pagar la mesa: prestamo (una sola vez) o pierdes
            if jugador.saldo < COSTO_MESA:
                if not prestamo_usado:
                    print(f"No te alcanza para pagar la mesa ({COSTO_MESA} pejecoins).")
                    print(f"Quieres un PRESTAMO de {PRESTAMO} pejecoins? (S/N)")
                    if leer().upper() == "S":
                        jugador.saldo += PRESTAMO
                        prestamo_usado = True
                        print(f"Recibes {PRESTAMO} pejecoins prestados. Ahora tienes "
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
                    print(f"Quieres DUPLICAR la apuesta ({apuesta * 2} pejecoins) para la ronda 2? (S/N)")
                    if leer().upper() == "S":
                        apuesta *= 2
                    else:
                        motivo = 1
                        seguir = False
                else:
                    # Rondas 3 a 5: apuesta libre o ALL IN
                    print(f"Quieres jugar la ronda {ronda + 1}? (S/N)")
                    if leer().upper() == "S":
                        if jugador.saldo == COSTO_MESA:
                            # Solo alcanza para la apuesta minima: se apuesta todo
                            print(f"Solo te alcanza para la mesa: vas ALL IN con {jugador.saldo} pejecoins.")
                            apuesta = jugador.saldo
                            all_in = True
                        else:
                            # Apuesta normal: de 25 a (saldo - 1); ALL IN = todo el saldo
                            maximo = jugador.saldo - 1
                            while True:
                                print(f"Cuantos pejecoins quieres apostar? ({COSTO_MESA} a {maximo}) "
                                      f"o escribe ALL IN para apostar tus {jugador.saldo} pejecoins")
                                texto = leer()
                                if texto.upper() == "ALL IN":
                                    all_in = True
                                    apuesta = jugador.saldo
                                    break
                                if es_numero(texto):
                                    apuesta = int(texto)
                                    if COSTO_MESA <= apuesta <= maximo:
                                        break
                                    print(f"Cantidad no valida. La mesa cuesta minimo {COSTO_MESA} pejecoins.")
                                else:
                                    print("Escribe una cifra o ALL IN.")
                    else:
                        motivo = 1
                        seguir = False

    # Mensaje final
    print()
    if motivo == 0:
        print("Hasta luego.")
        return

    print()
    print("Calculando el resultado final...")
    esperar_ms(2000)
    if motivo in (2, 4) or jugador.saldo < COSTO_MESA:
        anim_bust("FIN DEL JUEGO: SIN PEJECOINS", "")
        print()
        print("================================")
        print("        JUJUJU perdiste")
        print("================================")
        if motivo == 4:
            print("  (El DIAVLO cobro su pacto)")
    elif jugador.saldo > SALDO_INICIAL:
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
    if prestamo_usado:
        print(f"(Usaste el prestamo de {PRESTAMO} pejecoins)")
    print(f"Comodines usados: {jugador.usados}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("Juego interrumpido. Hasta luego.")
        sys.exit(0)
