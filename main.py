import pygame
from jugador import *
from fantasmas import *
from varios import *
from laberintos import Pantallas
from settings import *
from tiles import TileType
from funciones import *

# ====================================================================================
#   main.py (modulo principal) ... clase principal --> class Game
#  
#   ( contiene funcion bucle_principal() )
# ------------------------------------------------------------------------------------
class Game:
    def __init__(self):
        pygame.init()

        # Colores y constantes
        self.COL = Colores()
        self.CO = Constantes()

        # Marcadores: ptos, nivel, vidas...
        self.nivel = self.CO.NIVEL_INICIAL
        self.puntos = 0
        self.vidas = self.CO.VIDAS_INICIALES

        # Relativos a fantasmas
        self.sumaPtosComeFantasmas = 100	# 200 -> 400 -> 800 -> 1600
        self.temporizadorAzules = False

        # Listas updates (tomas de tiempo/temporizadores)
        self.ultimo_update = {
            "azules": pygame.time.get_ticks(),
            "preparado": pygame.time.get_ticks(),
            "item-fruta": pygame.time.get_ticks(),
            "show-bonus-fruta": pygame.time.get_ticks(),
            "show-bonus-fantasma0": pygame.time.get_ticks(),
            "show-bonus-fantasma1": pygame.time.get_ticks(),
            "show-bonus-fantasma2": pygame.time.get_ticks(),
            "show-bonus-fantasma3": pygame.time.get_ticks(),
            "nivel_superado_delay": pygame.time.get_ticks()
        }

        # True= Se ejecuta el bucle Principal | False= no se ejecuta
        self.program_running = True

        # Estados del juego
        self.estado_juego = {
            "menu_presentacion": True,
            "preparado": False,
            "en_juego": False,
            "game_over": False,
            "nivel_superado": False
        }

        # Inicializar listas con sprites
        self.listas_sprites = {
            "all_sprites": pygame.sprite.Group(),
            "pacman": pygame.sprite.Group(),
            "vidas": pygame.sprite.Group(),
            "laberinto": pygame.sprite.Group(),
            "puntitos": pygame.sprite.Group(),
            "puntos_gordos": pygame.sprite.Group(),
            "items": pygame.sprite.Group(),
            "textos": pygame.sprite.Group(),
            "bonus_come_fantasmas": pygame.sprite.Group(),
            "fantasmas": pygame.sprite.Group()
        }

        # Instanciar textos en 'Menu-presentacion
        self.instanciar_texto(self.CO.TXT_TITULO, 135, self.CO.RESOLUCION[0] // 2, 220, self.COL.NARANJA, negrita=True)
        self.instanciar_texto("Pulse ENTER para comenzar...", 32, self.CO.RESOLUCION[0] // 2, self.CO.RESOLUCION[1] - 80, 
            self.COL.AMARILLENTO)

        # Pantalla y reloj
        self.pantalla = pygame.display.set_mode(self.CO.RESOLUCION)
        self.reloj = pygame.time.Clock()

        # Cargar sonidos del modulo settings
        self.sonidos = Sonidos()
    
    # ===============================================================================
    def obtener_indice(self, x, y):
        """Obtener índice en el laberinto 1D basado en coordenadas 2D."""
        return y * self.CO.COLUMNAS + x if 0 <= x < self.CO.COLUMNAS and 0 <= y < self.CO.FILAS else None
    
    # ===============================================================================
    def crear_pantalla_nivel(self):
        """Crear el laberinto y los tiles correspondientes."""
        crear_escenario(self)
    
    # ===============================================================================
    def vaciar_listas(self):
        """Vaciar todas las listas de sprites."""
        for grupo in self.listas_sprites.values():
            grupo.empty()
    
    # ===============================================================================
    def resetear_estados_juego(self):
        self.estado_juego = {clave: False for clave in self.estado_juego}
    
    # ===============================================================================
    def new_game(self):
        """Preparar un nuevo nivel o juego."""
        self.vaciar_listas()
        self.crear_pantalla_nivel()
        self.instanciar_objetos()
        self.instanciar_textos_iniciales()
        self.sonidos.reproducir("inicio_nivel")
    
    # ===============================================================================
    def obtener_grafico(self, nombrePng, escala):
        """Devolver una imagen y un rectangulo."""
        return obtener_grafico_img_rect(self, nombrePng, escala)
    
    # ===============================================================================
    def instanciar_objetos(self):
        """Instanciar/re-instanciar Pacman, fantasmas, etc..."""

        if self.vidas < 0:
            self.ir_gameover()
            return
        
        instanciar_pacman(self)
        instanciar_showvidas(self)
        instanciar_fantasmas(self)
    
    # ===============================================================================
    def instanciar_fantasma(self, coorX, coorY, i, direc, azul, ojos):
        fantasma = Fantasma(self, coorX, coorY, i, direc, azul, ojos)
        self.listas_sprites["fantasmas"].add(fantasma)
    
    # ===============================================================================
    def instanciar_pacman_dies(self, x, y):
        pacman_dies = PacManDies(self, x, y)
        self.listas_sprites["all_sprites"].add(pacman_dies)
    
    # ===============================================================================
    def instanciar_fruta_periodicamente(self):
        """Instanciar/re-instanciar Item-Fruta periodicamente..."""
        instanciar_fruta(self)
        check_showbonus_kill(self)
    
    # ===============================================================================
    def instanciar_textos_iniciales(self):
        """Instanciar textos marcadores, Preparado..."""
        instanciar_textos(self)
    
    # ===============================================================================
    def instanciar_texto(self, txt, size, x, y, color, fondo=None, negrita=False, centrado=True, tipo=None):
        """Instanciar un texto y agregarlo a su lista correspondiente..."""
        newTxt = Textos(self, txt, size, x, y, color, fondo, negrita, centrado, tipo)
        self.listas_sprites["textos"].add(newTxt)
    
    # ===============================================================================
    def ir_gameover(self):
        """Pantalla de *** Game Over *** """
        self.resetear_estados_juego()
        pantalla_gameover(self)
    
    # ===============================================================================
    def update(self):
        pygame.display.set_caption(str(int(self.reloj.get_fps())))

        updates_segun_estado(self)

        pygame.display.flip()
        self.reloj.tick(self.CO.FPS)
    
    # ===============================================================================
    def draw(self):
        self.pantalla.fill(self.COL.GRIS_FONDO)
        draw_listas_sprites(self)
    
    # ===============================================================================
    def check_event(self):
        """Eventos (Quit/Comenzar...)"""
        eventos_comenzar_quit_etc(self)
    
    # ===============================================================================
    #   M A I N   L O O P
    #  
    # -------------------------------------------------------------------------------
    def bucle_principal(self):
        """BUCLE PRINCIPAL del Juego"""
        while self.program_running:
            self.check_event()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.bucle_principal()

