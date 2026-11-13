// =====================================================
//  BLACKJACK en PSeInt (2 barajas = 104 cartas)
//  - Saldo inicial: 100 pejecoins
//  - La mesa cuesta 25 pejecoins por ronda (apuesta minima)
//  - Ronda 1: apuesta de 25 pejecoins
//  - Ronda 2: opcion de DUPLICAR la apuesta (50 pejecoins) o retirarse
//  - Rondas 3 a 5: el jugador escribe cuanto apostar,
//    de 25 hasta (saldo - 1) para no quedar en ceros
//  - ALL IN: al escribir "ALL IN" apuestas TODO tu saldo
//    de una vez, sin importar cuantos pejecoins tengas
//  - Cada apuesta se resta del saldo; si le ganas al dealer,
//    la casa te paga y tu saldo aumenta
//  - Si te quedan menos de 25 pejecoins (lo que cuesta la mesa),
//    pierdes: "jijiji perdiste"
//  - Segunda oportunidad: la primera vez que te quedes con
//    menos de 25 pejecoins puedes pedir UN prestamo de 25 pejecoins
//  - Si terminas el juego con mas de 100 pejecoins, ganaste:
//    "EL DIAVLO ERE MUY BUENO"
//  - Empate: se devuelve la apuesta
//  - Victoria normal paga 1 a 1, Blackjack paga 3 a 2
//  - NUEVO (v1.5): cada carta se DIBUJA en pantalla con su
//    valor y su palo (picas, corazones, diamantes, treboles)
//  - NUEVO (v1.8): CHISPA, el robot crupier, reacciona con
//    una animacion a lo que pasa en el juego:
//      * Barajando  -> al inicio y cuando se rebaraja el mazo
//      * Pulgar     -> le ganas al dealer
//      * Salto      -> sacas Blackjack / terminas con mas de 100
//      * Bust       -> te pasas de 21 / te quedas sin pejecoins
//      * Derrota    -> el dealer te gana / te retiras
//      * Empate     -> empatas / completas las 5 rondas sin ganancia
//  - NUEVO (v1.9): intro de presentacion de EIBIYI al abrir el
//    juego (arranque de terminal + logo que va emergiendo)
//  - NUEVO (v2.0): COMODINES. 20% por ronda de recibir uno
//    (Rayos X, Cambio de carta, Vistazo, As bajo la manga o uno
//    Radiactivo disfrazado) y 30% por partida del legendario
//    PACTO CON EL DIAVLO. Se usan con (U) durante tu turno.
// =====================================================


// =====================================================
//  ANIMACIONES DE CHISPA
//  Todas reciben (estado, mensaje):
//    estado  -> texto que aparece arriba, en la "terminal"
//    mensaje -> texto final debajo de Chispa ("" = ninguno)
// =====================================================

SubProceso Pantalla(titulo)
	Borrar Pantalla
	Escribir "+----------------------------------------+"
	Escribir "|  EIBIYI :: BLACKJACK :: CHISPA v2.0    |"
	Escribir "+----------------------------------------+"
	Escribir "  ESTADO: ", titulo
	Escribir "------------------------------------------"
	Escribir ""
FinSubProceso

SubProceso LineasVacias(n)
	Definir k Como Entero
	Para k <- 1 Hasta n Hacer
		Escribir ""
	FinPara
FinSubProceso

SubProceso MensajeFinal(mensaje)
	Si mensaje <> "" Entonces
		Escribir ""
		Escribir "     >> ", mensaje, " <<"
	FinSi
FinSubProceso

// Dibujo base de Chispa
//  margen : espacios a la izquierda (para moverlo de lado)
//  antena : linea superior de la antena
//  ojos   : 3 caracteres, ej. "o o", "^ ^", "x x"
//  boca   : 1 caracter, ej. "-", "v", "~", "o"
//  brazos : 2 caracteres a cada lado del cuerpo, ej. "--", "__", "^^"
SubProceso DibujarChispa(margen, antena, ojos, boca, brazos)
	Escribir margen, antena
	Escribir margen, "         |"
	Escribir margen, "      +-----+"
	Escribir margen, "      | ", ojos, " |"
	Escribir margen, "      |  ", boca, "  |"
	Escribir margen, "      +-----+"
	Escribir margen, "    +---------+"
	Escribir margen, "  ", brazos, "|  [ $ ]  |", brazos
	Escribir margen, "    +---------+"
	Escribir margen, "       |   |"
	Escribir margen, "      _|   |_"
FinSubProceso

SubProceso FrameBrazoMedio
	Escribir "         *"
	Escribir "         |"
	Escribir "      +-----+"
	Escribir "      | o o |"
	Escribir "      |  o  |"
	Escribir "      +-----+"
	Escribir "    +---------+   //"
	Escribir "  --|  [ $ ]  |--//"
	Escribir "    +---------+"
	Escribir "       |   |"
	Escribir "      _|   |_"
FinSubProceso

SubProceso FramePulgar(ojos, brillo)
	Escribir "         *        ", brillo
	Escribir "         |          _"
	Escribir "      +-----+      | |"
	Escribir "      | ", ojos, " |    __| |"
	Escribir "      |  v  |   |    |"
	Escribir "      +-----+   |____|"
	Escribir "    +---------+    |"
	Escribir "  --|  [ $ ]  |----+"
	Escribir "    +---------+"
	Escribir "       |   |"
	Escribir "      _|   |_"
FinSubProceso

// ---- Pulgar arriba: le ganaste al dealer ----
SubProceso AnimPulgarArriba(estado, mensaje)
	Pantalla(estado)
	DibujarChispa("", "         *", "o o", "-", "--")
	Esperar 500 Milisegundos
	Pantalla(estado)
	FrameBrazoMedio()
	Esperar 300 Milisegundos
	Pantalla(estado)
	FramePulgar("^ ^", "")
	Esperar 400 Milisegundos
	Pantalla(estado)
	FramePulgar("^ -", "  *")
	Esperar 350 Milisegundos
	Pantalla(estado)
	FramePulgar("^ ^", "*   *")
	Esperar 350 Milisegundos
	Pantalla(estado)
	FramePulgar("^ ^", "  *")
	MensajeFinal(mensaje)
FinSubProceso

// ---- Salto: Blackjack o gran victoria ----
SubProceso AnimBlackjack(estado, mensaje)
	Definir salto Como Entero
	Para salto <- 1 Hasta 3 Hacer
		Pantalla(estado)
		Escribir "     *  YEAH!  *"
		DibujarChispa("", "         *", "^ ^", "O", "^^")
		LineasVacias(2)
		Escribir "  ~~~~~~~~~~~~~~~~~~~~~~"
		Esperar 250 Milisegundos
		Pantalla(estado)
		LineasVacias(3)
		DibujarChispa("", "         *", "^ ^", "v", "--")
		Escribir "  ~~~~~~~~~~~~~~~~~~~~~~"
		Esperar 250 Milisegundos
	FinPara
	MensajeFinal(mensaje)
FinSubProceso

// ---- Bust: te pasaste de 21 o te quedaste sin pejecoins ----
SubProceso AnimBust(estado, mensaje)
	Definir i Como Entero
	Definir margen Como Caracter
	Pantalla("CALCULANDO...")
	DibujarChispa("", "         *", "o o", "o", "--")
	Esperar 500 Milisegundos
	Para i <- 1 Hasta 6 Hacer
		Si i MOD 2 = 0 Entonces
			margen <- "   "
		SiNo
			margen <- ""
		FinSi
		Pantalla(estado)
		DibujarChispa(margen, "         *", "@ @", "O", "--")
		Esperar 120 Milisegundos
	FinPara
	Pantalla(estado)
	DibujarChispa("", "       *_", "x x", "~", "__")
	MensajeFinal(mensaje)
FinSubProceso

// ---- Derrota: el dealer gana o te retiras ----
SubProceso AnimDerrota(estado, mensaje)
	Pantalla(estado)
	DibujarChispa("", "         *", "o o", "-", "--")
	Esperar 400 Milisegundos
	Pantalla(estado)
	DibujarChispa("", "         *", "o o", "~", "--")
	Esperar 350 Milisegundos
	Pantalla(estado)
	DibujarChispa("", "        *", ". .", "~", "__")
	Esperar 350 Milisegundos
	Pantalla(estado)
	DibujarChispa("", "       *_", ". ,", "n", "__")
	MensajeFinal(mensaje)
FinSubProceso

// ---- Empate: Chispa mira a los lados y se encoge de hombros ----
SubProceso AnimEmpate(estado, mensaje)
	Definir i Como Entero
	Para i <- 1 Hasta 4 Hacer
		Pantalla(estado)
		Si i MOD 2 = 0 Entonces
			DibujarChispa("", "         *", " oo", "-", "--")
		SiNo
			DibujarChispa("", "         *", "oo ", "-", "--")
		FinSi
		Esperar 250 Milisegundos
	FinPara
	Pantalla(estado)
	DibujarChispa("", "         *", "o o", "-", "~~")
	MensajeFinal(mensaje)
FinSubProceso

// ---- Barajando: inicio del juego y cuando se rebaraja ----
SubProceso AnimBarajando(estado, mensaje)
	Definir paso, j Como Entero
	Definir barra, cartas, figuras Como Caracter
	Dimension figuras[5]
	figuras[1] <- "[A]"
	figuras[2] <- "[K]"
	figuras[3] <- "[Q]"
	figuras[4] <- "[J]"
	figuras[5] <- "[10]"
	Para paso <- 1 Hasta 10 Hacer
		barra <- ""
		Para j <- 1 Hasta 10 Hacer
			Si j <= paso Entonces
				barra <- Concatenar(barra, "#")
			SiNo
				barra <- Concatenar(barra, ".")
			FinSi
		FinPara
		cartas <- ""
		Para j <- 0 Hasta 4 Hacer
			cartas <- Concatenar(cartas, figuras[((paso + j) MOD 5) + 1])
			cartas <- Concatenar(cartas, " ")
		FinPara
		Pantalla(estado)
		Si paso MOD 2 = 0 Entonces
			DibujarChispa("", "         *", "o o", "-", "--")
		SiNo
			DibujarChispa("", "         *", "- -", "-", "~~")
		FinSi
		Escribir ""
		Escribir "     ", cartas
		Escribir ""
		Escribir "     [", barra, "] ", paso * 10, "%"
		Esperar 200 Milisegundos
	FinPara
	MensajeFinal(mensaje)
FinSubProceso

// =====================================================
//  INTRO DE EMPRESA: EIBIYI (estilo terminal retro)
//  1) La terminal "arranca" escribiendo letra por letra
//  2) Aparecen los dos hermanos chibi bajo las estrellas
//  3) Abren los ojos y miran hacia arriba (con brillo)
//  4) El nombre EIBIYI va emergiendo:  .  ->  :  ->  =  ->  #
//  5) "PRESENTA" y el copyright
// =====================================================

// Efecto maquina de escribir: muestra el texto letra por letra
SubProceso Teclear(texto)
	Definir i, primera, n Como Entero
	// Detecta si Subcadena cuenta desde 0 o desde 1 (igual que EsNumero)
	Si Subcadena("AB", 1, 1) = "B" Entonces
		primera <- 0
	SiNo
		primera <- 1
	FinSi
	n <- Longitud(texto)
	Para i <- primera Hasta primera + n - 1 Hacer
		Escribir Sin Saltar Subcadena(texto, i, i)
		Esperar 15 Milisegundos
	FinPara
	Escribir ""
FinSubProceso

// Cambia cada "#" de la linea por el caracter c
// (asi el logo va "emergiendo" de tenue a solido)
Funcion r <- Revelar(linea, c)
	Definir r, car Como Caracter
	Definir i, primera, n Como Entero
	// Detecta si Subcadena cuenta desde 0 o desde 1 (igual que EsNumero)
	Si Subcadena("AB", 1, 1) = "B" Entonces
		primera <- 0
	SiNo
		primera <- 1
	FinSi
	n <- Longitud(linea)
	r <- ""
	Para i <- primera Hasta primera + n - 1 Hacer
		car <- Subcadena(linea, i, i)
		Si car = "#" Entonces
			r <- Concatenar(r, c)
		SiNo
			r <- Concatenar(r, car)
		FinSi
	FinPara
FinFuncion

// Letras grandes del nombre EIBIYI (5 filas)
Funcion fila <- LogoFila(f)
	Definir fila Como Caracter
	Segun f Hacer
		1:
			fila <- "######  ######  #####   ######  ##  ##  ######"
		2:
			fila <- "##        ##    ##  ##    ##    ##  ##    ##  "
		3:
			fila <- "#####     ##    #####     ##     ####     ##  "
		4:
			fila <- "##        ##    ##  ##    ##      ##      ##  "
		De Otro Modo:
			fila <- "######  ######  #####   ######    ##    ######"
	FinSegun
FinFuncion

// Cielo con estrellas que parpadean (3 variantes)
Funcion e <- Estrellas(n)
	Definir e Como Caracter
	Segun n Hacer
		1:
			e <- "     .         *          .     "
		2:
			e <- "     *         .          +     "
		De Otro Modo:
			e <- "     +         *          *     "
	FinSegun
FinFuncion

// Los dos hermanos chibi mirando hacia arriba
//  p = pupila:  "-" ojos cerrados,  "^" mirando arriba,  "*" brillo
SubProceso DibujarHermanos(margen, p)
	Escribir margen, "    _/\/\/\_    ", "   _/\/\/\/\_   "
	Escribir margen, "   /        \   ", "   /        \   "
	Escribir margen, "  |          |  ", "  |          |  "
	Escribir margen, "  | (", p, ")  (", p, ") |  ", "  | (", p, ")  (", p, ") |  "
	Escribir margen, "  |     o    |  ", "  | ~   o  ~ |  "
	Escribir margen, "   \________/   ", "   \________/   "
	Escribir margen, "    /|    |\    ", "    /|    |\    "
	Escribir margen, "     |_/\_|     ", "     |_/\_|     "
FinSubProceso

// Dibuja una escena completa del logo
//  nEstr     : variante de estrellas (1 a 3)
//  pupila    : ojos de los hermanos
//  etapa     : 0 = sin nombre, 1 a 4 = el nombre va emergiendo
SubProceso EscenaLogo(nEstr, pupila, etapa)
	Definir f Como Entero
	Definir c Como Caracter
	Borrar Pantalla
	LineasVacias(2)
	Escribir "               ", Estrellas(nEstr)
	Escribir ""
	DibujarHermanos("               ", pupila)
	Escribir ""
	Si etapa = 0 Entonces
		LineasVacias(5)
	SiNo
		Segun etapa Hacer
			1:
				c <- "."
			2:
				c <- ":"
			3:
				c <- "="
			De Otro Modo:
				c <- "#"
		FinSegun
		Para f <- 1 Hasta 5 Hacer
			Escribir "        ", Revelar(LogoFila(f), c)
		FinPara
	FinSi
	Escribir ""
FinSubProceso

// Animacion completa de presentacion
SubProceso IntroEIBIYI
	Definir i Como Entero

	// 1) Arranque de la terminal
	Borrar Pantalla
	Teclear("EIBIYI SYSTEMS (R)  ::  TERMINAL DE JUEGO v2.0")
	Teclear("==============================================")
	Esperar 300 Milisegundos
	Teclear("> Verificando memoria .............. 64K OK")
	Teclear("> Cargando CHISPA.SYS .................. OK")
	Teclear("> Preparando 2 barajas (104 cartas) .... OK")
	Teclear("> Calibrando pejecoins ................. OK")
	Teclear("> Cargando COMODINES.DAT ............... OK")
	Teclear("> Iniciando BLACKJACK.EXE ...")
	Esperar 800 Milisegundos

	// 2) Estrellas parpadeando y los hermanos con los ojos cerrados
	Para i <- 1 Hasta 4 Hacer
		EscenaLogo((i MOD 2) + 1, "-", 0)
		Esperar 300 Milisegundos
	FinPara

	// 3) Abren los ojos, miran hacia arriba y les brillan
	EscenaLogo(1, "^", 0)
	Esperar 500 Milisegundos
	EscenaLogo(3, "*", 0)
	Esperar 300 Milisegundos
	EscenaLogo(2, "^", 0)
	Esperar 400 Milisegundos

	// 4) El nombre EIBIYI emerge poco a poco
	Para i <- 1 Hasta 4 Hacer
		EscenaLogo((i MOD 3) + 1, "^", i)
		Esperar 250 Milisegundos
	FinPara

	// 5) Texto de presentacion
	Escribir Sin Saltar "                     "
	Teclear("-  P R E S E N T A  -")
	Esperar 700 Milisegundos
	Escribir Sin Saltar "        "
	Teclear("(C) 2026 EIBIYI. Todos los derechos reservados.")
	Esperar 1500 Milisegundos
FinSubProceso

// Cada carta del mazo es un numero del 1 al 52:
//    1 a 13 = picas       14 a 26 = corazones
//   27 a 39 = diamantes   40 a 52 = treboles

// Devuelve el valor de la carta (1 = A, 2..10, 11 = J, 12 = Q, 13 = K)
Funcion v <- ValorCarta(carta)
	Definir v Como Entero
	v <- ((carta - 1) MOD 13) + 1
FinFuncion

// Devuelve el palo de la carta (1 = picas, 2 = corazones, 3 = diamantes, 4 = treboles)
Funcion p <- PaloCarta(carta)
	Definir p Como Entero
	p <- Trunc((carta - 1) / 13) + 1
FinFuncion

// Devuelve el nombre de la carta (A, 2..10, J, Q, K)
Funcion nombre <- NombreCarta(c)
	Definir nombre Como Caracter
	Segun c Hacer
		1:
			nombre <- "A"
		11:
			nombre <- "J"
		12:
			nombre <- "Q"
		13:
			nombre <- "K"
		De Otro Modo:
			nombre <- ConvertirATexto(c)
	FinSegun
FinFuncion

// Devuelve una fila (1 a 4) del dibujo del palo
//    picas     corazones   diamantes   treboles
//      .         _ _          ^           _
//     /.\       ( v )        / \         ( )
//    (_._)       \ /         \ /        (_|_)
//      |          v           v           |
Funcion arte <- ArtePalo(palo, fila)
	Definir arte Como Caracter
	Segun palo Hacer
		1:
			Segun fila Hacer
				1:
					arte <- "  .  "
				2:
					arte <- " /.\ "
				3:
					arte <- "(_._)"
				De Otro Modo:
					arte <- "  |  "
			FinSegun
		2:
			Segun fila Hacer
				1:
					arte <- " _ _ "
				2:
					arte <- "( v )"
				3:
					arte <- " \ / "
				De Otro Modo:
					arte <- "  v  "
			FinSegun
		3:
			Segun fila Hacer
				1:
					arte <- "  ^  "
				2:
					arte <- " / \ "
				3:
					arte <- " \ / "
				De Otro Modo:
					arte <- "  v  "
			FinSegun
		De Otro Modo:
			Segun fila Hacer
				1:
					arte <- "  _  "
				2:
					arte <- " ( ) "
				3:
					arte <- "(_|_)"
				De Otro Modo:
					arte <- "  |  "
			FinSegun
	FinSegun
FinFuncion

// Devuelve una linea (1 a 8) del dibujo de una carta
// Si oculta es Verdadero, dibuja la carta boca abajo
Funcion seg <- LineaCarta(linea, carta, oculta)
	Definir seg, valor, izq, der Como Caracter
	Si oculta Entonces
		Segun linea Hacer
			1, 8:
				seg <- "+---------+"
			2, 4, 6:
				seg <- "|/\/\/\/\/|"
			De Otro Modo:
				seg <- "|\/\/\/\/\|"
		FinSegun
	SiNo
		valor <- NombreCarta(ValorCarta(carta))
		// El 10 ocupa dos letras; a las demas se les agrega un espacio
		Si Longitud(valor) = 1 Entonces
			izq <- Concatenar(valor, " ")
			der <- Concatenar(" ", valor)
		SiNo
			izq <- valor
			der <- valor
		FinSi
		Segun linea Hacer
			1, 8:
				seg <- "+---------+"
			2:
				seg <- Concatenar(Concatenar("|", izq), "       |")
			7:
				seg <- Concatenar(Concatenar("|       ", der), "|")
			De Otro Modo:
				seg <- Concatenar(Concatenar("|  ", ArtePalo(PaloCarta(carta), linea - 2)), "  |")
		FinSegun
	FinSi
FinFuncion

// Dibuja las n cartas de una mano, una al lado de la otra
// Si conOculta es Verdadero, agrega al final una carta boca abajo
// (la carta oculta del dealer). Maximo 6 cartas por renglon.
SubProceso DibujarMano(cartas Por Referencia, n, conOculta)
	Definir total, primera, ultima, linea, i Como Entero
	Definir oculta Como Logico
	total <- n
	Si conOculta Entonces
		total <- n + 1
	FinSi
	Para primera <- 1 Hasta total Con Paso 6 Hacer
		ultima <- primera + 5
		Si ultima > total Entonces
			ultima <- total
		FinSi
		Para linea <- 1 Hasta 8 Hacer
			Para i <- primera Hasta ultima Hacer
				Si i > n Entonces
					oculta <- Verdadero
					Escribir Sin Saltar LineaCarta(linea, 1, oculta), "  "
				SiNo
					oculta <- Falso
					Escribir Sin Saltar LineaCarta(linea, cartas[i], oculta), "  "
				FinSi
			FinPara
			Escribir ""
		FinPara
	FinPara
FinSubProceso

// Revisa que el texto escrito sea un numero entero positivo
// (sirve para que el programa no truene si se escribe algo raro)
Funcion valido <- EsNumero(texto)
	Definir valido Como Logico
	Definir i, primera, n Como Entero
	Definir car Como Caracter
	// Detecta si el perfil de PSeInt cuenta las letras desde 0 o desde 1
	Si Subcadena("AB", 1, 1) = "B" Entonces
		primera <- 0
	SiNo
		primera <- 1
	FinSi
	n <- Longitud(texto)
	Si n > 0 Y n <= 9 Entonces
		valido <- Verdadero
		Para i <- primera Hasta primera + n - 1 Hacer
			car <- Subcadena(texto, i, i)
			Si car < "0" O car > "9" Entonces
				valido <- Falso
			FinSi
		FinPara
	SiNo
		valido <- Falso
	FinSi
FinFuncion

// Arma el mazo con 2 barajas (104 cartas, sin jokers) y lo revuelve
// Cada carta (valor + palo) aparece 2 veces: una por cada baraja
SubProceso Barajar(mazo Por Referencia)
	Definir i, j, temp Como Entero
	Para i <- 1 Hasta 104 Hacer
		mazo[i] <- ((i - 1) MOD 52) + 1
	FinPara
	// Revolver (algoritmo de Fisher-Yates)
	Para i <- 104 Hasta 2 Con Paso -1 Hacer
		j <- Azar(i) + 1
		temp <- mazo[i]
		mazo[i] <- mazo[j]
		mazo[j] <- temp
	FinPara
	Escribir "*** Se barajan las 2 barajas (104 cartas) ***"
FinSubProceso

// Saca la siguiente carta del mazo, la guarda en la mano (cartas)
// y la suma a los puntos
// El As vale 11, pero baja a 1 si la mano se pasa de 21
SubProceso RobarCarta(mazo Por Referencia, pos Por Referencia, suma Por Referencia, ases Por Referencia, cartas Por Referencia, n Por Referencia)
	Definir c, v Como Entero
	Si pos > 104 Entonces
		Barajar(mazo)
		pos <- 1
	FinSi
	c <- mazo[pos]
	pos <- pos + 1
	n <- n + 1
	cartas[n] <- c
	v <- ValorCarta(c)
	Si v = 1 Entonces
		suma <- suma + 11
		ases <- ases + 1
	SiNo
		Si v > 10 Entonces
			suma <- suma + 10
		SiNo
			suma <- suma + v
		FinSi
	FinSi
	Mientras suma > 21 Y ases > 0 Hacer
		suma <- suma - 10
		ases <- ases - 1
	FinMientras
FinSubProceso

// =====================================================
//  COMODINES (v2.0)
//  Normales (20% de que te toque uno por ronda, maximo 2):
//    1 = RAYOS X           ves la carta oculta del dealer
//                          (30% falla: -10 pejecoins)
//    2 = CAMBIO DE CARTA   descartas tu ultima carta y sacas otra
//    3 = VISTAZO           ves la siguiente carta del mazo
//                          (35% Chispa te cacha y revuelve el mazo)
//    4 = AS BAJO LA MANGA  conviertes una carta en As
//                          (40% te cachan: pierdes la mano y -20 de multa)
//    5 = RADIACTIVO        se disfraza de uno de los 4 anteriores;
//                          al usarlo te quita 15 pejecoins
//  Legendario (30% de que aparezca UNA vez por partida):
//    PACTO CON EL DIAVLO   65% tu mano se vuelve BLACKJACK y ganas
//                          la ronda / 35% pierdes TODA la partida
// =====================================================

Funcion nombre <- NombreComodin(t)
	Definir nombre Como Caracter
	Segun t Hacer
		1:
			nombre <- "RAYOS X"
		2:
			nombre <- "CAMBIO DE CARTA"
		3:
			nombre <- "VISTAZO"
		4:
			nombre <- "AS BAJO LA MANGA"
		De Otro Modo:
			nombre <- "COMODIN RADIACTIVO"
	FinSegun
FinFuncion

Funcion desc <- DescComodin(t)
	Definir desc Como Caracter
	Segun t Hacer
		1:
			desc <- "Ves la carta oculta del dealer (30% falla: -10 pejecoins)"
		2:
			desc <- "Descartas tu ultima carta y sacas otra (puede salir peor)"
		3:
			desc <- "Ves la siguiente carta del mazo (35% Chispa revuelve el mazo)"
		De Otro Modo:
			desc <- "Conviertes una carta en As (40% te cachan: pierdes y -20 de multa)"
	FinSegun
FinFuncion

// Quita pejecoins sin dejar el saldo en negativo
SubProceso CobrarMulta(saldo Por Referencia, cantidad)
	Definir cobro Como Entero
	cobro <- cantidad
	Si saldo < cobro Entonces
		cobro <- saldo
	FinSi
	saldo <- saldo - cobro
	Escribir "  -", cobro, " pejecoins. Saldo: ", saldo, " pejecoins."
FinSubProceso

// Recalcula la suma y los ases de una mano completa
SubProceso RecalcularMano(cartas Por Referencia, n, suma Por Referencia, ases Por Referencia)
	Definir i, v Como Entero
	suma <- 0
	ases <- 0
	Para i <- 1 Hasta n Hacer
		v <- ValorCarta(cartas[i])
		Si v = 1 Entonces
			suma <- suma + 11
			ases <- ases + 1
		SiNo
			Si v > 10 Entonces
				suma <- suma + 10
			SiNo
				suma <- suma + v
			FinSi
		FinSi
	FinPara
	Mientras suma > 21 Y ases > 0 Hacer
		suma <- suma - 10
		ases <- ases - 1
	FinMientras
FinSubProceso

// Revuelve solo las cartas que quedan en el mazo (de pos a 104)
SubProceso RevolverResto(mazo Por Referencia, pos)
	Definir i, j, temp Como Entero
	Para i <- 104 Hasta pos + 1 Con Paso -1 Hacer
		j <- pos + Azar(i - pos + 1)
		temp <- mazo[i]
		mazo[i] <- mazo[j]
		mazo[j] <- temp
	FinPara
FinSubProceso

// Quita el comodin k del inventario y recorre los demas
SubProceso QuitarComodin(invReal Por Referencia, invVisible Por Referencia, nInv Por Referencia, k)
	Definir i Como Entero
	Para i <- k Hasta nInv - 1 Hacer
		invReal[i] <- invReal[i + 1]
		invVisible[i] <- invVisible[i + 1]
	FinPara
	nInv <- nInv - 1
FinSubProceso

// Muestra en una linea los comodines que tienes
SubProceso MostrarComodines(invVisible Por Referencia, nInv, tienePacto)
	Definir i Como Entero
	Escribir Sin Saltar "Comodines: "
	Para i <- 1 Hasta nInv Hacer
		Escribir Sin Saltar "[", NombreComodin(invVisible[i]), "] "
	FinPara
	Si tienePacto Entonces
		Escribir Sin Saltar "[PACTO CON EL DIAVLO]"
	FinSi
	Escribir ""
FinSubProceso

// Pide elegir un comodin. Devuelve 0 si cancela, 1 a nInv para
// un comodin normal, o nInv + 1 para el Pacto con el DIAVLO
Funcion op <- ElegirComodin(invVisible Por Referencia, nInv, tienePacto)
	Definir op, i, maxOp Como Entero
	Definir texto Como Caracter
	Escribir ""
	Escribir "--------- TUS COMODINES ---------"
	Para i <- 1 Hasta nInv Hacer
		Escribir "  ", i, ". ", NombreComodin(invVisible[i]), ": ", DescComodin(invVisible[i])
	FinPara
	maxOp <- nInv
	Si tienePacto Entonces
		maxOp <- nInv + 1
		Escribir "  ", maxOp, ". PACTO CON EL DIAVLO: 65% BLACKJACK / 35% pierdes TODA la partida"
	FinSi
	Escribir "  0. Cancelar"
	Repetir
		Escribir Sin Saltar "Elige: "
		Leer texto
		Si EsNumero(texto) Entonces
			op <- ConvertirANumero(texto)
		SiNo
			op <- -1
		FinSi
		Si op < 0 O op > maxOp Entonces
			Escribir "Opcion no valida."
		FinSi
	Hasta Que op >= 0 Y op <= maxOp
FinFuncion

// Muestra la mesa: dealer con su carta oculta y tus cartas
SubProceso MostrarMesa(cartasD Por Referencia, cartasJ Por Referencia, nJ, sumaJ)
	Escribir ""
	Escribir "DEALER (una carta oculta):"
	DibujarMano(cartasD, 1, Verdadero)
	Escribir ""
	Escribir "TUS CARTAS:"
	DibujarMano(cartasJ, nJ, Falso)
	Escribir "Tus cartas suman: ", sumaJ
FinSubProceso

// ---- Animacion: Chispa te entrega un comodin ----
SubProceso AnimComodin(estado, mensaje)
	Definir k Como Entero
	Para k <- 3 Hasta 0 Con Paso -1 Hacer
		Pantalla(estado)
		LineasVacias(k)
		Escribir "            [?]"
		LineasVacias(3 - k)
		DibujarChispa("", "         *", "o o", "o", "^^")
		Esperar 250 Milisegundos
	FinPara
	Pantalla(estado)
	Escribir "          * [?] *"
	LineasVacias(3)
	DibujarChispa("", "         *", "^ ^", "v", "^^")
	MensajeFinal(mensaje)
FinSubProceso

// ---- Animacion: Chispa se rie de ti (comodin radiactivo) ----
SubProceso AnimRisa(estado, mensaje)
	Definir i Como Entero
	Para i <- 1 Hasta 6 Hacer
		Pantalla(estado)
		Si i MOD 2 = 0 Entonces
			Escribir "          JA  JA  JA"
			DibujarChispa("", "         *", "^ ^", "D", "^^")
		SiNo
			Escribir "       JA  JA  JA"
			DibujarChispa("  ", "         *", "> <", "O", "--")
		FinSi
		Esperar 200 Milisegundos
	FinPara
	MensajeFinal(mensaje)
FinSubProceso

// ---- Animacion: se sella el Pacto con el DIAVLO (suspenso) ----
SubProceso AnimPacto
	Definir i Como Entero
	Para i <- 1 Hasta 10 Hacer
		Pantalla("PACTO CON EL DIAVLO: SELLANDO TU DESTINO...")
		Si i MOD 2 = 0 Entonces
			Escribir "      >>>  B L A C K J A C K  <<<"
			DibujarChispa("", "         *", "O O", "o", "--")
		SiNo
			Escribir "      >>>  P E R D E R  T O D O  <<<"
			DibujarChispa("", "         *", "o o", "o", "--")
		FinSi
		Esperar 220 Milisegundos
	FinPara
FinSubProceso


// Juega una ronda completa contra el dealer
// Devuelve: 0 = pierde (el dealer gana), 1 = empate, 2 = gana,
//           3 = gana con Blackjack, 4 = pierde por pasarse de 21,
//           5 = pierde TODA la partida (Pacto con el DIAVLO fallido),
//           6 = lo cacharon con el As bajo la manga
Funcion resultado <- JugarRonda(mazo Por Referencia, pos Por Referencia, saldo Por Referencia, invReal Por Referencia, invVisible Por Referencia, nInv Por Referencia, tienePacto Por Referencia, usados Por Referencia)
	Definir resultado, sumaJ, asesJ, sumaD, asesD, nJ, nD, op, tipo, vis, k Como Entero
	Definir cartasJ, cartasD, vista Como Entero
	Dimension cartasJ[23], cartasD[23], vista[2]
	Definir eleccion, texto Como Caracter
	Definir terminada Como Logico

	sumaJ <- 0
	asesJ <- 0
	nJ <- 0
	sumaD <- 0
	asesD <- 0
	nD <- 0
	resultado <- 0
	terminada <- Falso

	// Reparto inicial: 2 cartas al jugador y 2 al dealer (una boca abajo)
	RobarCarta(mazo, pos, sumaJ, asesJ, cartasJ, nJ)
	RobarCarta(mazo, pos, sumaJ, asesJ, cartasJ, nJ)
	RobarCarta(mazo, pos, sumaD, asesD, cartasD, nD)
	RobarCarta(mazo, pos, sumaD, asesD, cartasD, nD)

	MostrarMesa(cartasD, cartasJ, nJ, sumaJ)

	Si sumaJ = 21 Entonces
		// Blackjack natural del jugador
		Escribir "BLACKJACK!"
		Escribir ""
		Escribir "Dealer voltea su carta:"
		DibujarMano(cartasD, nD, Falso)
		Escribir "El dealer suma: ", sumaD
		Si sumaD = 21 Entonces
			resultado <- 1
		SiNo
			resultado <- 3
		FinSi
	SiNo
		// Turno del jugador
		eleccion <- ""
		Mientras sumaJ < 21 Y eleccion <> "P" Y terminada = Falso Hacer
			Si nInv > 0 O tienePacto Entonces
				MostrarComodines(invVisible, nInv, tienePacto)
				Escribir "(C) Pedir carta,  (P) Plantarte  o  (U) Usar comodin:"
			SiNo
				Escribir "(C) Pedir carta  o  (P) Plantarte:"
			FinSi
			Leer eleccion
			eleccion <- Mayusculas(eleccion)
			Si eleccion = "C" Entonces
				RobarCarta(mazo, pos, sumaJ, asesJ, cartasJ, nJ)
				Escribir ""
				Escribir "TUS CARTAS:"
				DibujarMano(cartasJ, nJ, Falso)
				Escribir "Tus cartas suman: ", sumaJ
			SiNo
				Si eleccion = "U" Y (nInv > 0 O tienePacto) Entonces
					op <- ElegirComodin(invVisible, nInv, tienePacto)
					Si op > 0 Entonces
						usados <- usados + 1
						Si op > nInv Entonces
							// ====== PACTO CON EL DIAVLO ======
							tienePacto <- Falso
							AnimPacto()
							Si Azar(100) < 65 Entonces
								// Tu mano se convierte en A + K = BLACKJACK
								nJ <- 2
								cartasJ[1] <- 1
								cartasJ[2] <- 13
								RecalcularMano(cartasJ, nJ, sumaJ, asesJ)
								Pantalla("EL DIAVLO CUMPLIO SU PACTO")
								Escribir "TU MANO AHORA ES:"
								DibujarMano(cartasJ, nJ, Falso)
								Escribir "Tus cartas suman: ", sumaJ
								Escribir "BLACKJACK! Ganas la ronda automaticamente."
								resultado <- 3
							SiNo
								Pantalla("EL DIAVLO COBRA SU PACTO")
								DibujarChispa("", "       *_", "x x", "~", "__")
								Escribir ""
								Escribir "El pacto salio mal... pierdes TODA la partida."
								resultado <- 5
							FinSi
							terminada <- Verdadero
						SiNo
							// ====== COMODIN NORMAL ======
							tipo <- invReal[op]
							vis <- invVisible[op]
							QuitarComodin(invReal, invVisible, nInv, op)
							Escribir ""
							Escribir ">> Usas ", NombreComodin(vis), "..."
							Segun tipo Hacer
								1:
									// RAYOS X
									Si Azar(100) < 70 Entonces
										Escribir "La carta oculta del dealer es:"
										DibujarMano(cartasD, nD, Falso)
										Escribir "El dealer suma: ", sumaD
									SiNo
										Escribir "El escaner se sobrecalento! No viste nada."
										CobrarMulta(saldo, 10)
									FinSi
								2:
									// CAMBIO DE CARTA
									Escribir "Descartas tu ultima carta y sacas otra..."
									nJ <- nJ - 1
									RecalcularMano(cartasJ, nJ, sumaJ, asesJ)
									RobarCarta(mazo, pos, sumaJ, asesJ, cartasJ, nJ)
									MostrarMesa(cartasD, cartasJ, nJ, sumaJ)
								3:
									// VISTAZO
									Si pos > 104 Entonces
										Barajar(mazo)
										pos <- 1
									FinSi
									Si Azar(100) < 65 Entonces
										vista[1] <- mazo[pos]
										Escribir "La siguiente carta del mazo es:"
										DibujarMano(vista, 1, Falso)
									SiNo
										Escribir "Chispa te cacho espiando el mazo y lo revolvio!"
										RevolverResto(mazo, pos)
									FinSi
								4:
									// AS BAJO LA MANGA
									Escribir "Que carta quieres convertir en As? (1 a ", nJ, ")"
									Repetir
										Leer texto
										Si EsNumero(texto) Entonces
											k <- ConvertirANumero(texto)
										SiNo
											k <- 0
										FinSi
										Si k < 1 O k > nJ Entonces
											Escribir "Escribe un numero del 1 al ", nJ
										FinSi
									Hasta Que k >= 1 Y k <= nJ
									Si Azar(100) < 40 Entonces
										Escribir "EL DEALER TE CACHO CON EL AS EN LA MANGA!"
										resultado <- 6
										terminada <- Verdadero
									SiNo
										cartasJ[k] <- (PaloCarta(cartasJ[k]) - 1) * 13 + 1
										RecalcularMano(cartasJ, nJ, sumaJ, asesJ)
										Escribir "Nadie se dio cuenta..."
										MostrarMesa(cartasD, cartasJ, nJ, sumaJ)
									FinSi
								De Otro Modo:
									// RADIACTIVO (estaba disfrazado)
									AnimRisa("ERA UN COMODIN RADIACTIVO!", "CHISPA SE RIE DE TI")
									Escribir ""
									CobrarMulta(saldo, 15)
									MostrarMesa(cartasD, cartasJ, nJ, sumaJ)
							FinSegun
						FinSi
					FinSi
				SiNo
					Si eleccion <> "P" Entonces
						Escribir "Opcion no valida."
					FinSi
				FinSi
			FinSi
		FinMientras

		Si terminada = Falso Entonces
			Si sumaJ > 21 Entonces
				Escribir "Te pasaste de 21."
				resultado <- 4
			SiNo
				// Turno del dealer: voltea su carta y pide hasta tener 17 o mas
				Escribir ""
				Escribir "Dealer voltea su carta:"
				DibujarMano(cartasD, nD, Falso)
				Escribir "El dealer suma: ", sumaD
				Mientras sumaD < 17 Hacer
					RobarCarta(mazo, pos, sumaD, asesD, cartasD, nD)
					Escribir ""
					Escribir "Dealer pide carta:"
					DibujarMano(cartasD, nD, Falso)
					Escribir "El dealer suma: ", sumaD
				FinMientras

				Si sumaD > 21 Entonces
					Escribir "El dealer se paso de 21."
					resultado <- 2
				SiNo
					Si sumaJ > sumaD Entonces
						resultado <- 2
					SiNo
						Si sumaJ < sumaD Entonces
							resultado <- 0
						SiNo
							resultado <- 1
						FinSi
					FinSi
				FinSi
			FinSi
		FinSi
	FinSi
FinFuncion

Algoritmo BlackJack
	Definir mazo Como Entero
	Dimension mazo[105]
	Definir saldo, apuesta, ronda, resultado, maximo, premio, pos, motivo, costoMesa Como Entero
	Definir respuesta, textoApuesta Como Caracter
	Definir seguir, prestamoUsado, allIn, apuestaValida Como Logico
	Definir invReal, invVisible Como Entero
	Dimension invReal[3], invVisible[3]
	Definir nInv, rondaPacto, usados, tipo Como Entero
	Definir tienePacto Como Logico

	costoMesa <- 25
	saldo <- 100
	apuesta <- costoMesa
	ronda <- 0
	prestamoUsado <- Falso
	allIn <- Falso
	motivo <- 0   // 0 = no jugo, 1 = se retiro, 2 = sin pejecoins para la mesa, 3 = completo 5 rondas, 4 = pacto fallido

	// Comodines
	nInv <- 0
	usados <- 0
	tienePacto <- Falso
	// El Pacto con el DIAVLO tiene 30% de aparecer UNA vez por partida,
	// en una ronda al azar (1 a 5). Si no sale, rondaPacto queda en 0.
	Si Azar(100) < 30 Entonces
		rondaPacto <- Azar(5) + 1
	SiNo
		rondaPacto <- 0
	FinSi

	pos <- 1

	// Intro de la empresa
	IntroEIBIYI()

	// Bienvenida con Chispa
	Pantalla("BIENVENIDO A LA MESA")
	DibujarChispa("", "         *", "^ ^", "v", "--")
	Escribir ""
	Escribir "=========== BLACKJACK ==========="
	Escribir "Tienes ", saldo, " pejecoins. Se juegan maximo 5 rondas."
	Escribir "La mesa cuesta ", costoMesa, " pejecoins por ronda."
	Escribir "Cada ronda Chispa puede regalarte un COMODIN... usalo con cuidado."
	Escribir "Quieres jugar? (S/N)"
	Leer respuesta
	Si Mayusculas(respuesta) = "S" Entonces
		seguir <- Verdadero
		Barajar(mazo)
		AnimBarajando("BARAJANDO 2 BARAJAS (104 CARTAS)...", "MAZO LISTO. A JUGAR!")
	SiNo
		seguir <- Falso
	FinSi

	Mientras seguir Hacer
		ronda <- ronda + 1

		// Si quedan menos de 20 cartas, se vuelve a barajar
		Si pos > 85 Entonces
			Barajar(mazo)
			pos <- 1
			AnimBarajando("QUEDAN POCAS CARTAS: REBARAJANDO...", "MAZO NUEVO LISTO")
		FinSi

		// ---- Comodines: 20% por ronda (maximo 2 guardados) ----
		Si nInv < 2 Y Azar(100) < 20 Entonces
			tipo <- Azar(5) + 1
			nInv <- nInv + 1
			invReal[nInv] <- tipo
			Si tipo = 5 Entonces
				// El radiactivo se disfraza de un comodin normal
				invVisible[nInv] <- Azar(4) + 1
			SiNo
				invVisible[nInv] <- tipo
			FinSi
			AnimComodin("CHISPA ENCONTRO UN COMODIN", Concatenar("RECIBISTE: ", NombreComodin(invVisible[nInv])))
			Escribir "     ", DescComodin(invVisible[nInv])
			Esperar 3 Segundos
		FinSi
		// ---- Pacto con el DIAVLO: solo en la ronda sorteada ----
		Si ronda = rondaPacto Entonces
			tienePacto <- Verdadero
			AnimComodin("!!! COMODIN LEGENDARIO !!!", "RECIBISTE: PACTO CON EL DIAVLO")
			Escribir "     65% tu mano se vuelve BLACKJACK y ganas la ronda"
			Escribir "     35% pierdes TODA la partida. Tu decides cuando usarlo..."
			Esperar 3 Segundos
		FinSi

		saldo <- saldo - apuesta
		Escribir ""
		Escribir "------ RONDA ", ronda, " de 5 | Apuesta: ", apuesta, " pejecoins ------"
		Si allIn Entonces
			Escribir "************ ALL IN ************"
		FinSi
		Escribir "Saldo despues de apostar: ", saldo, " pejecoins | Cartas en el mazo: ", 105 - pos

		resultado <- JugarRonda(mazo, pos, saldo, invReal, invVisible, nInv, tienePacto, usados)

		// Pausa automatica para que el jugador vea las cartas antes de la animacion
		Escribir ""
		Escribir "Chispa esta revisando la mano..."
		Esperar 2 Segundos

		Segun resultado Hacer
			0:
				AnimDerrota("EL DEALER GANA LA MANO", "EL DEALER TE GANO ESTA VEZ")
				Escribir ""
				Escribir "Perdiste ", apuesta, " pejecoins."
			1:
				AnimEmpate("EMPATE CON EL DEALER", "NADIE GANA, NADIE PIERDE")
				Escribir ""
				Escribir "Empate. Recuperas tus ", apuesta, " pejecoins."
				saldo <- saldo + apuesta
			2:
				AnimPulgarArriba("VICTORIA", "BIEN JUGADO! GANASTE LA MANO")
				Escribir ""
				Escribir "Le ganaste al dealer! La casa te paga ", apuesta, " pejecoins."
				saldo <- saldo + apuesta * 2
			3:
				AnimBlackjack("!!! BLACKJACK !!!", "BLACKJACK! LA CASA PAGA 3 A 2")
				premio <- Trunc(apuesta * 3 / 2)
				Escribir ""
				Escribir "Ganaste con Blackjack! La casa te paga ", premio, " pejecoins."
				saldo <- saldo + apuesta + premio
			4:
				AnimBust("ERROR: VALOR > 21", "BUST! TE PASASTE DE 21")
				Escribir ""
				Escribir "Perdiste ", apuesta, " pejecoins."
			5:
				AnimBust("PACTO FALLIDO", "EL DIAVLO SE LLEVO TODOS TUS PEJECOINS")
				Escribir ""
				Escribir "Pierdes TODA la partida."
				saldo <- 0
			6:
				AnimDerrota("TE CACHARON HACIENDO TRAMPA", "EL DEALER VIO EL AS EN TU MANGA")
				Escribir ""
				Escribir "Perdiste ", apuesta, " pejecoins y pagas una multa de 20:"
				CobrarMulta(saldo, 20)
		FinSegun
		Escribir "Saldo actual: ", saldo, " pejecoins."
		allIn <- Falso

		Si resultado = 5 Entonces
			motivo <- 4
			seguir <- Falso
		SiNo
			Si ronda = 5 Entonces
				motivo <- 3
				seguir <- Falso
			SiNo
				// Si no alcanza para pagar la mesa: prestamo (una sola vez) o pierdes
				Si saldo < costoMesa Entonces
					Si prestamoUsado = Falso Entonces
						Escribir "No te alcanza para pagar la mesa (", costoMesa, " pejecoins)."
						Escribir "Quieres un PRESTAMO de 25 pejecoins? (S/N)"
						Leer respuesta
						Si Mayusculas(respuesta) = "S" Entonces
							saldo <- saldo + 25
							prestamoUsado <- Verdadero
							Escribir "Recibes 25 pejecoins prestados. Ahora tienes ", saldo, " pejecoins. Es tu ultima oportunidad."
						SiNo
							motivo <- 2
							seguir <- Falso
						FinSi
					SiNo
						Escribir "No te alcanza para pagar la mesa y ya usaste tu prestamo."
						motivo <- 2
						seguir <- Falso
					FinSi
				FinSi

				Si seguir Entonces
					Si ronda = 1 Entonces
						// Despues de la ronda 1: duplicar la apuesta o terminar
						Escribir "Quieres DUPLICAR la apuesta (", apuesta * 2, " pejecoins) para la ronda 2? (S/N)"
						Leer respuesta
						Si Mayusculas(respuesta) = "S" Entonces
							apuesta <- apuesta * 2
						SiNo
							motivo <- 1
							seguir <- Falso
						FinSi
					SiNo
						// Rondas 3 a 5: apuesta libre o ALL IN
						Escribir "Quieres jugar la ronda ", ronda + 1, "? (S/N)"
						Leer respuesta
						Si Mayusculas(respuesta) = "S" Entonces
							Si saldo = costoMesa Entonces
								// Solo alcanza para la apuesta minima: se apuesta todo
								Escribir "Solo te alcanza para la mesa: vas ALL IN con ", saldo, " pejecoins."
								apuesta <- saldo
								allIn <- Verdadero
							SiNo
								// Apuesta normal: de 25 a (saldo - 1) para no quedar en ceros
								// ALL IN: apostar todo el saldo (disponible siempre)
								maximo <- saldo - 1
								apuestaValida <- Falso
								Repetir
									Escribir "Cuantos pejecoins quieres apostar? (", costoMesa, " a ", maximo, ") o escribe ALL IN para apostar tus ", saldo, " pejecoins"
									Leer textoApuesta
									Si Mayusculas(textoApuesta) = "ALL IN" Entonces
										allIn <- Verdadero
										apuesta <- saldo
										apuestaValida <- Verdadero
									SiNo
										Si EsNumero(textoApuesta) Entonces
											apuesta <- ConvertirANumero(textoApuesta)
											Si apuesta >= costoMesa Y apuesta <= maximo Entonces
												apuestaValida <- Verdadero
											SiNo
												Escribir "Cantidad no valida. La mesa cuesta minimo ", costoMesa, " pejecoins."
											FinSi
										SiNo
											Escribir "Escribe una cifra o ALL IN."
										FinSi
									FinSi
								Hasta Que apuestaValida
							FinSi
						SiNo
							motivo <- 1
							seguir <- Falso
						FinSi
					FinSi
				FinSi
			FinSi
		FinSi
	FinMientras

	// Mensaje final
	Escribir ""
	Si motivo = 0 Entonces
		Escribir "Hasta luego."
	SiNo
		Escribir ""
		Escribir "Calculando el resultado final..."
		Esperar 2 Segundos
		Si motivo = 2 O motivo = 4 O saldo < costoMesa Entonces
			AnimBust("FIN DEL JUEGO: SIN PEJECOINS", "")
			Escribir ""
			Escribir "================================"
			Escribir "        JUJUJU perdiste"
			Escribir "================================"
			Si motivo = 4 Entonces
				Escribir "  (El DIAVLO cobro su pacto)"
			FinSi
		SiNo
			Si saldo > 100 Entonces
				AnimBlackjack("!!! GANASTE EL JUEGO !!!", "")
				Escribir ""
				Escribir "================================"
				Escribir "   EL DIAVLO ERE MUY BUENO"
				Escribir "================================"
			SiNo
				Si motivo = 1 Entonces
					AnimDerrota("TE RETIRAS DE LA MESA", "")
					Escribir ""
					Escribir "======= TE RETIRAS DEL JUEGO POBRE? ======="
				SiNo
					AnimEmpate("FIN DE LAS 5 RONDAS", "")
					Escribir ""
					Escribir "======= COMPLETASTE LAS 5 RONDAS ======="
				FinSi
			FinSi
		FinSi
		Escribir "Puntuacion final: ", saldo, " pejecoins."
		Escribir "Comodines usados: ", usados
		Si prestamoUsado Entonces
			Escribir "(Usaste el prestamo de 25 pejecoins)"
		FinSi
	FinSi
FinAlgoritmo
