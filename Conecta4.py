import pygame
import random
import sys

pygame.init()

# =========================
# PANTALLA COMPLETA
# =========================

pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

ANCHO = pantalla.get_width()
ALTO = pantalla.get_height()

pygame.display.set_caption("Conecta 4 con Ricky")

# =========================
# CONFIGURACIÓN
# =========================

FILAS = 6
COLUMNAS = 7

TAM = min(ANCHO // 10, ALTO // 9)

RADIO = TAM // 2 - 10

TABLERO_ANCHO = COLUMNAS * TAM
TABLERO_ALTO = FILAS * TAM

TABLERO_X = (ANCHO - TABLERO_ANCHO) // 2
TABLERO_Y = (ALTO - TABLERO_ALTO) // 2 + 40

# =========================
# COLORES
# =========================

FONDO = (8, 10, 28)

PANEL = (12, 18, 45)

TABLERO = (0, 70, 210)

BORDE = (0, 15, 70)

BLANCO = (255, 255, 255)

GRIS = (190, 190, 215)

CYAN = (0, 240, 255)

AZUL_NEON = (0, 130, 255)

AMARILLO = (255, 210, 0)

ROJO = (255, 55, 55)

VERDE = (70, 230, 140)

COLORES = {
    1: ROJO,
    2: AMARILLO,
    3: VERDE
}

# =========================
# FUENTES
# =========================

fuente_titulo = pygame.font.SysFont("Arial", 80, bold=True)

fuente_grande = pygame.font.SysFont("Arial", 55, bold=True)

fuente = pygame.font.SysFont("Arial", 32, bold=True)

fuente_peque = pygame.font.SysFont("Arial", 24, bold=True)

# =========================
# BOTONES
# =========================

def dibujar_boton(texto, x, y, w, h, color, hover, evento):

    mouse = pygame.mouse.get_pos()

    rect = pygame.Rect(x, y, w, h)

    if rect.collidepoint(mouse):
        pygame.draw.rect(pantalla, hover, rect, border_radius=20)
    else:
        pygame.draw.rect(pantalla, color, rect, border_radius=20)

    pygame.draw.rect(pantalla, CYAN, rect, 3, border_radius=20)

    texto_render = fuente.render(texto, True, BLANCO)

    pantalla.blit(
        texto_render,
        (
            x + (w - texto_render.get_width()) // 2,
            y + (h - texto_render.get_height()) // 2
        )
    )

    if evento.type == pygame.MOUSEBUTTONDOWN:
        if rect.collidepoint(evento.pos):
            return True

    return False

# =========================
# FONDO
# =========================

def dibujar_fondo():

    pantalla.fill(FONDO)

    pygame.draw.line(
        pantalla,
        AZUL_NEON,
        (0, 120),
        (350, 320),
        4
    )

    pygame.draw.line(
        pantalla,
        CYAN,
        (ANCHO, 180),
        (ANCHO - 450, 350),
        4
    )

    pygame.draw.circle(
        pantalla,
        ROJO,
        (ANCHO - 180, 250),
        60
    )

    pygame.draw.circle(
        pantalla,
        BLANCO,
        (ANCHO - 205, 225),
        10
    )

# =========================
# MENÚ PRINCIPAL
# =========================

def menu_principal():

    while True:

        dibujar_fondo()

        titulo1 = fuente_peque.render(
            "4. CONECTA 4 CON RICKY",
            True,
            BLANCO
        )

        titulo2 = fuente_titulo.render(
            "CONECTA 4",
            True,
            BLANCO
        )

        titulo3 = fuente_grande.render(
            "CON RICKY",
            True,
            AMARILLO
        )

        subtitulo = fuente.render(
            "PYTHON + INTELIGENCIA ARTIFICIAL",
            True,
            CYAN
        )

        pantalla.blit(titulo1, ((ANCHO - titulo1.get_width()) // 2, 40))

        pantalla.blit(titulo2, ((ANCHO - titulo2.get_width()) // 2, 90))

        pantalla.blit(titulo3, ((ANCHO - titulo3.get_width()) // 2, 170))

        pantalla.blit(subtitulo, ((ANCHO - subtitulo.get_width()) // 2, 260))

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if dibujar_boton(
                "Humano vs PC",
                (ANCHO - 420) // 2,
                370,
                420,
                70,
                PANEL,
                AZUL_NEON,
                evento
            ):
                return {1: "humano", 2: "pc"}

            if dibujar_boton(
                "PC vs PC",
                (ANCHO - 420) // 2,
                470,
                420,
                70,
                PANEL,
                AZUL_NEON,
                evento
            ):
                return {1: "pc", 2: "pc"}

            if dibujar_boton(
                "Humano vs PC vs PC",
                (ANCHO - 420) // 2,
                570,
                420,
                70,
                PANEL,
                AZUL_NEON,
                evento
            ):
                return {1: "humano", 2: "pc", 3: "pc"}

        evento_falso = pygame.event.Event(pygame.NOEVENT)

        dibujar_boton("Humano vs PC", (ANCHO - 420) // 2, 370, 420, 70, PANEL, AZUL_NEON, evento_falso)

        dibujar_boton("PC vs PC", (ANCHO - 420) // 2, 470, 420, 70, PANEL, AZUL_NEON, evento_falso)

        dibujar_boton("Humano vs PC vs PC", (ANCHO - 420) // 2, 570, 420, 70, PANEL, AZUL_NEON, evento_falso)

        pygame.display.update()

# =========================
# MENÚ DIFICULTAD
# =========================

def menu_dificultad():

    while True:

        dibujar_fondo()

        titulo = fuente_titulo.render(
            "ESCOGE DIFICULTAD",
            True,
            BLANCO
        )

        pantalla.blit(
            titulo,
            ((ANCHO - titulo.get_width()) // 2, 180)
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if dibujar_boton(
                "Fácil",
                (ANCHO - 350) // 2,
                340,
                350,
                70,
                PANEL,
                VERDE,
                evento
            ):
                return "FÁCIL"

            if dibujar_boton(
                "Normal",
                (ANCHO - 350) // 2,
                450,
                350,
                70,
                PANEL,
                AZUL_NEON,
                evento
            ):
                return "NORMAL"

            if dibujar_boton(
                "Difícil",
                (ANCHO - 350) // 2,
                560,
                350,
                70,
                PANEL,
                ROJO,
                evento
            ):
                return "DIFÍCIL"

        evento_falso = pygame.event.Event(pygame.NOEVENT)

        dibujar_boton("Fácil", (ANCHO - 350) // 2, 340, 350, 70, PANEL, VERDE, evento_falso)

        dibujar_boton("Normal", (ANCHO - 350) // 2, 450, 350, 70, PANEL, AZUL_NEON, evento_falso)

        dibujar_boton("Difícil", (ANCHO - 350) // 2, 560, 350, 70, PANEL, ROJO, evento_falso)

        pygame.display.update()

# =========================
# TABLERO
# =========================

def crear_tablero():
    return [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]

def columna_valida(tablero, col):
    return tablero[0][col] == 0

def obtener_fila(tablero, col):

    for fila in range(FILAS - 1, -1, -1):
        if tablero[fila][col] == 0:
            return fila

def colocar(tablero, fila, col, jugador):
    tablero[fila][col] = jugador

def columnas_validas(tablero):
    return [c for c in range(COLUMNAS) if columna_valida(tablero, c)]

def tablero_lleno(tablero):
    return len(columnas_validas(tablero)) == 0

# =========================
# GANADOR
# =========================

def ganador(tablero, jugador):

    for fila in range(FILAS):
        for col in range(COLUMNAS - 3):
            if all(tablero[fila][col+i] == jugador for i in range(4)):
                return True

    for col in range(COLUMNAS):
        for fila in range(FILAS - 3):
            if all(tablero[fila+i][col] == jugador for i in range(4)):
                return True

    for fila in range(FILAS - 3):
        for col in range(COLUMNAS - 3):
            if all(tablero[fila+i][col+i] == jugador for i in range(4)):
                return True

    for fila in range(3, FILAS):
        for col in range(COLUMNAS - 3):
            if all(tablero[fila-i][col+i] == jugador for i in range(4)):
                return True

    return False

# =========================
# IA
# =========================

def simular(tablero, col, jugador):

    copia = [fila[:] for fila in tablero]

    fila = obtener_fila(copia, col)

    if fila is not None:
        colocar(copia, fila, col, jugador)

    return copia

def ia_facil(tablero):
    return random.choice(columnas_validas(tablero))

def ia_normal(tablero, jugador, jugadores):

    validas = columnas_validas(tablero)

    for col in validas:
        if ganador(simular(tablero, col, jugador), jugador):
            return col

    for enemigo in jugadores:
        if enemigo != jugador:
            for col in validas:
                if ganador(simular(tablero, col, enemigo), enemigo):
                    return col

    return random.choice(validas)

def ia_dificil(tablero, jugador, jugadores):

    centro = COLUMNAS // 2

    if centro in columnas_validas(tablero):
        return centro

    return ia_normal(tablero, jugador, jugadores)

def elegir_ia(tablero, jugador, jugadores, dificultad):

    if dificultad == "FÁCIL":
        return ia_facil(tablero)

    if dificultad == "NORMAL":
        return ia_normal(tablero, jugador, jugadores)

    return ia_dificil(tablero, jugador, jugadores)

# =========================
# DIBUJAR TABLERO
# =========================

def dibujar_tablero(tablero, texto):

    pantalla.fill(FONDO)

    barra = fuente.render(texto, True, BLANCO)

    pantalla.blit(barra, (40, 40))

    pygame.draw.rect(
        pantalla,
        TABLERO,
        (
            TABLERO_X,
            TABLERO_Y,
            TABLERO_ANCHO,
            TABLERO_ALTO
        ),
        border_radius=25
    )

    for col in range(COLUMNAS):
        for fila in range(FILAS):

            x = TABLERO_X + col * TAM + TAM // 2

            y = TABLERO_Y + fila * TAM + TAM // 2

            pygame.draw.circle(
                pantalla,
                BORDE,
                (x, y),
                RADIO + 6
            )

            jugador = tablero[fila][col]

            color = FONDO if jugador == 0 else COLORES[jugador]

            pygame.draw.circle(
                pantalla,
                color,
                (x, y),
                RADIO
            )

            if jugador != 0:
                pygame.draw.circle(
                    pantalla,
                    BLANCO,
                    (x - 15, y - 15),
                    8
                )

    pygame.display.update()

# =========================
# JUEGO
# =========================

def jugar():

    jugadores = menu_principal()

    dificultad = menu_dificultad()

    tablero = crear_tablero()

    lista_jugadores = list(jugadores.keys())

    turno = 0

    terminado = False

    while not terminado:

        jugador = lista_jugadores[turno]

        tipo = jugadores[jugador]

        texto = f"Jugador {jugador} | {tipo.upper()} | Dificultad: {dificultad}"

        dibujar_tablero(tablero, texto)

        if tipo == "humano":

            esperando = True

            while esperando:

                for evento in pygame.event.get():

                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

                    if evento.type == pygame.MOUSEMOTION:

                        dibujar_tablero(tablero, texto)

                        x = evento.pos[0]

                        pygame.draw.circle(
                            pantalla,
                            COLORES[jugador],
                            (x, TABLERO_Y - 60),
                            RADIO
                        )

                        pygame.display.update()

                    if evento.type == pygame.MOUSEBUTTONDOWN:

                        x = evento.pos[0]

                        col = (x - TABLERO_X) // TAM

                        if 0 <= col < COLUMNAS:

                            if columna_valida(tablero, col):

                                fila = obtener_fila(tablero, col)

                                colocar(tablero, fila, col, jugador)

                                esperando = False

        else:

            pygame.time.wait(800)

            col = elegir_ia(
                tablero,
                jugador,
                lista_jugadores,
                dificultad
            )

            if columna_valida(tablero, col):

                fila = obtener_fila(tablero, col)

                colocar(tablero, fila, col, jugador)

        dibujar_tablero(tablero, texto)

        if ganador(tablero, jugador):

            dibujar_tablero(
                tablero,
                f"GANÓ JUGADOR {jugador}"
            )

            pygame.time.wait(4000)

            terminado = True

        elif tablero_lleno(tablero):

            dibujar_tablero(
                tablero,
                "EMPATE"
            )

            pygame.time.wait(4000)

            terminado = True

        turno = (turno + 1) % len(lista_jugadores)

    jugar()

# =========================
# INICIAR
# =========================

jugar()