import pygame
import configparser
import os

# ====================================================================================
#	settings.py (modulo de configuraciones)
# 
# ------------------------------------------------------------------------------------
class ConfigIni:
    @staticmethod
    def crear_configini_si_no_existe():
        NOMBRE = 'config.ini'

        CONTENIDO = """
            [general]
            titulo=PacClon
            nivel_inicial=1
            vidas_iniciales=3
            pacman_ini_pos_x=9
            pacman_ini_pos_y=4
            invulnerable=false
            [video]
            size_tile_x=50
            size_tile_y=50
            zona_scores=200
            fps=100
            """
        
        if not os.path.exists(NOMBRE):
            with open(NOMBRE, "w") as f:
                f.write(CONTENIDO.strip())
            print(f"Archivo {NOMBRE} creado.")
        else:
            print(f"Usando archivo {NOMBRE} existente.")

# ====================================================================================
class Colores:
    AMARILLO = (220, 190, 0)
    AMARILLENTO = (250, 245, 130)
    NARANJA = (250, 142, 12)
    NARANJA_ROJIZO = (255, 100, 12)
    NARANJA_ROJIZO_2 = (255, 45, 12)
    BLANCO = (240, 240, 240)
    GRIS_FONDO = (59, 59, 59)
    BG_GRIS_OSCURO = (49, 49, 50)
    ROJO = (230, 30, 20)
    VERDE_FONDO = (20, 240, 30)
    AZUL_C = (144, 205, 205)

# ====================================================================================
class Constantes:
    ConfigIni.crear_configini_si_no_existe()

    CONFIG = configparser.ConfigParser()
    CONFIG.read('config.ini')

    NIVEL_INICIAL = CONFIG.getint('general', 'nivel_inicial')
    VIDAS_INICIALES = CONFIG.getint('general', 'vidas_iniciales')

    TX, TY = CONFIG.getint('video', 'size_tile_x'), CONFIG.getint('video', 'size_tile_y') # Tamano de los Tiles
    FILAS, COLUMNAS = 15, 19 # Filas x Columnas
    PACMAN_INI_POS = (CONFIG.getint('general', 'pacman_ini_pos_x'), CONFIG.getint('general', 'pacman_ini_pos_y'))
    VIDAS_COOR_X = COLUMNAS # CoorX showvidas
    VIDAS_COOR_Y = 7 # CoorY Inicial showvidas
    INVULNERABLE = CONFIG.getboolean('general', 'invulnerable')
    N_FANTASMAS = 4
    # Duracion de los 'fantasmas-azules' en el nivel 1
    DURACION_AZULES = [8000, 8000, 7000, 6000, 5500, 5000, 4700, 4500, 4250, 4000, 3750, 3500, 3000, 2750, 2500]
    # Duracion de los estados-fantasmas (scatter-chase) en los niveles: (1, 1, 2, 3, 4, (5 en adelante))
    DURACION_ESTADO = [
        (7000, 20000, 7000, 20000, 5000, 20000, 5000),
        (7000, 20000, 7000, 20000, 5000, 20000, 5000),
        (7000, 20000, 7000, 20000, 5000, 1033000, 1000),
        (7000, 20000, 7000, 20000, 5000, 1033000, 1000),
        (7000, 20000, 7000, 20000, 5000, 1033000, 1000),
        (5000, 20000, 5000, 20000, 5000, 1033000, 1000)
    ]
    DURACION_PREPARADO = 4200
    INTERVALO_FRUTA = 12000
    DURACION_SHOW_BONUS_FRUTA = 2400
    DELAY_NEXT_LEVEL = 7200
    TXT_TITULO = " Pac Clon "
    TXT_PREPARADO = " Preparado! "
    ZONA_SCORES = CONFIG.getint('video', 'zona_scores')
    RESOLUCION = (TX * COLUMNAS + ZONA_SCORES, TY * FILAS)
    FPS = CONFIG.getint('video', 'fps')

    # (x, y, id, direccion, scatterX, scatterY):
    LISTA_ARGS_FANTASMAS = [
        (5, 8, 0, 'le', 1, 1),
        (8, 8, 1, 'le', 17, 1),
        (10, 8, 2, 'ri', 1, 13),
        (13, 8, 3, 'ri', 17, 13)
    ]

# ====================================================================================
class Sonidos:
    """Funcion constructora"""
    def __init__(self):
        pygame.mixer.init()
        self.sonidos = self.cargar_sonidos()
    
    # -------------------------------------------------------------------------
    def cargar_sonidos(self):
        """Cargar todos los sonidos en un diccionario."""
        return {
            "wakawaka": self.cargar_sonido("sonido/pacmanwakawaka.ogg", 0.9),
            "sirena": self.cargar_sonido("sonido/pacmansirena.ogg", 0.2),
            "eating_cherry": self.cargar_sonido("sonido/pacmaneatingcherry.ogg"),
            "pacman_dies": self.cargar_sonido("sonido/pacmandies.ogg"),
            "gameover_retro": self.cargar_sonido("sonido/gameoveretro.ogg"),
            "fantasmas_azules": self.cargar_sonido("sonido/pacmanazules.ogg"),
            "eating_ghost": self.cargar_sonido("sonido/pacmaneatinghost.ogg"),
            "inicio_nivel": self.cargar_sonido("sonido/pacmaninicionivel.ogg"),
            "intermision": self.cargar_sonido("sonido/pacmanintermision.ogg")
        }
    
    # -------------------------------------------------------------------------
    def cargar_sonido(self, ruta, volumen=1.0):
        """Carga un sonido específico con el volumen indicado."""
        sonido = pygame.mixer.Sound(ruta)
        sonido.set_volume(volumen)
        return sonido
    
    # -------------------------------------------------------------------------
    def reproducir(self, nombre, duracion=None):
        """Reproduce un sonido si está en el diccionario."""
        if nombre in self.sonidos and nombre == "fantasmas_azules":
            self.sonidos[nombre].play(loops=-1)
        
        elif nombre in self.sonidos:
            if duracion == None:
                self.sonidos[nombre].play()
            else:
                self.sonidos[nombre].play(maxtime=duracion)


