import pygame
import sys
from jugador import PacMan, PacmanShowVidas
from fantasmas import Fantasma
from varios import *
from laberintos import Pantallas
from tiles import TileType

# ========================================================================
#   Modulo de funciones (que no pertenecen a ninguna class)
#   
#   (La mayoria estaban ubicadas en el modulo main.py y han sido...
#    ... trasladadas aqui para reducir código en main.py)
# ------------------------------------------------------------------------
def crear_escenario(self):
    """Crear el laberinto y los tiles correspondientes."""
    
    contador = -1
    for i in range(self.CO.FILAS):
        for ii in range(self.CO.COLUMNAS):
            contador += 1
            valor_tile = Pantallas.get_laberinto(self.nivel)[contador]

            # Usar enumeración para los tipos de tiles
            if valor_tile == TileType.WALL.value:
                tile = LaberintoTile(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(tile)
                self.listas_sprites["laberinto"].add(tile)

            elif valor_tile == TileType.WALL_RECT.value:
                tileOrig = LaberintoOrigTile(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(tileOrig)
                self.listas_sprites["puntitos"].add(tileOrig)

            elif valor_tile == TileType.WALL_DOWN.value:
                tileOrig = LaberintoOrigTile(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(tileOrig)
                self.listas_sprites["puntitos"].add(tileOrig)
            
            elif valor_tile == TileType.WALL_UP.value:
                tileOrig = LaberintoOrigTile(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(tileOrig)
                self.listas_sprites["puntitos"].add(tileOrig)
            
            elif valor_tile == TileType.WALL_RIGHT.value:
                tileOrig = LaberintoOrigTile(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(tileOrig)
                self.listas_sprites["puntitos"].add(tileOrig)
            
            elif valor_tile == TileType.WALL_LEFT.value:
                tileOrig = LaberintoOrigTile(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(tileOrig)
                self.listas_sprites["puntitos"].add(tileOrig)

            elif valor_tile == TileType.DOT.value:
                dot = Puntitos(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(dot)
                self.listas_sprites["puntitos"].add(dot)

            elif valor_tile == TileType.POWER_DOT.value:
                power_dot = PuntosGordos(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(power_dot)
                self.listas_sprites["puntos_gordos"].add(power_dot)

# ===================================================================================
def obtener_grafico_img_rect(self, nombrePng, escala):
    """Devolver una imagen y un rectangulo."""

    img = pygame.image.load('pacGraf/' + nombrePng).convert()
    escalaX = self.CO.TX * escala
    escalaY = self.CO.TY * escala
    image = pygame.transform.scale(img, (escalaX, escalaY))
    image.set_colorkey((255, 255, 255))
    rect = image.get_rect()
    
    return (image, rect)

# ===================================================================================
def instanciar_pacman(self):
    self.pacman = PacMan(self, self.CO.PACMAN_INI_POS[0], self.CO.PACMAN_INI_POS[1])
    self.listas_sprites["all_sprites"].add(self.pacman)
    self.listas_sprites["pacman"].add(self.pacman)

# ===================================================================================
def instanciar_showvidas(self):
    for i in range(self.vidas):
        self.pacman_vidas = PacmanShowVidas(self, self.CO.VIDAS_COOR_X, self.CO.VIDAS_COOR_Y + i)
        self.listas_sprites["vidas"].add(self.pacman_vidas)

# ===================================================================================
def instanciar_fantasmas(self):
    for i in range(self.CO.N_FANTASMAS):
        datos = self.CO.LISTA_ARGS_FANTASMAS[i]
        coorX = datos[0]
        coorY = datos[1]
        instanciar_fantasma(self, coorX, coorY, i, datos[3], False, False, datos[4], datos[5])

# ===================================================================================
def instanciar_fantasma(self, coorX, coorY, i, direc, azul, ojos, scatterX, scatterY):
    fantasma = Fantasma(self, coorX, coorY, i, direc, azul, ojos, scatterX, scatterY)
    self.listas_sprites["fantasmas"].add(fantasma)

# ===================================================================================
def instanciar_fruta(self):
    """Cada cierto tiempo aparece la fruta"""

    if len(self.listas_sprites["items"]) != 0 or not self.estado_juego["en_juego"]:
        return
    
    calculo = pygame.time.get_ticks()
    if calculo - self.ultimo_update["item-fruta"] > self.CO.INTERVALO_FRUTA:
        self.ultimo_update["item-fruta"] = calculo
        print("Instanciada-Fruta")
        newFruta = ItemFrutas(self)
        self.listas_sprites["all_sprites"].add(newFruta)
        self.listas_sprites["items"].add(newFruta)

# ===================================================================================
def check_showbonus_kill(self):
    if len(self.listas_sprites["items"]) != 0 or not self.estado_juego["en_juego"]:
        return
    
    calculo = pygame.time.get_ticks()
    if calculo - self.ultimo_update["show-bonus-fruta"] > self.CO.DURACION_SHOW_BONUS_FRUTA:
        self.ultimo_update["show-bonus-fruta"] = calculo
        eliminar_elemento_de_lista(self, "textos", "show-bonus-fruta")

# ===================================================================================
def check_showbonus_fant_kill(self):
    if not self.estado_juego["en_juego"] or not self.temporizadorAzules:
        return
    
    for i in range(self.CO.N_FANTASMAS):
        calculo = pygame.time.get_ticks()
        if calculo - self.ultimo_update[f"show-bonus-fantasma{i}"] > self.CO.DURACION_SHOW_BONUS_FRUTA:
            self.ultimo_update[f"show-bonus-fantasma{i}"] = calculo
            eliminar_elemento_de_lista(self, "textos", f"show-bonus-fantasma{i}")

# ===================================================================================
def instanciar_textos(self):
    """Renderizar textos en pantalla"""
    MARGEN = 9

    self.instanciar_texto(self.CO.TXT_PREPARADO, 90, (self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES) // 2,
        300, self.COL.VERDE_FONDO, fondo=self.COL.BG_GRIS_OSCURO, negrita=True, tipo="txt-preparado")
    
    self.instanciar_texto("Puntos", 48, self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES + MARGEN,
        self.CO.TY, self.COL.AMARILLENTO, negrita=True, centrado=False)
    self.instanciar_texto("Nivel", 48, self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES + MARGEN,
        self.CO.TY * 4, self.COL.AMARILLENTO, negrita=True, centrado=False)
    self.instanciar_texto("0", 48, self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES + MARGEN,
        self.CO.TY * 2, self.COL.BLANCO, negrita=True, centrado=False, tipo="dinamico-puntos")
    self.instanciar_texto(str(self.nivel), 48, self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES + MARGEN,
        self.CO.TY * 5, self.COL.BLANCO, negrita=True, centrado=False, tipo="dinamico-nivel")

# ===================================================================================
def pantalla_gameover(self):
    """Pantalla de *** Game Over *** """

    print('game over')
    
    self.estado_juego["game_over"] = True

    self.instanciar_texto(' Game Over ', 120, (self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES) // 2,
        300, self.COL.NARANJA_ROJIZO_2, fondo=self.COL.BG_GRIS_OSCURO, negrita=True, tipo="gameover")

    self.instanciar_texto("  ENTER - Volver a jugar      ESC - Salir  ", 32, (self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES) // 2,
        self.CO.RESOLUCION[1] // 1.5, self.COL.VERDE_FONDO, fondo=self.COL.BG_GRIS_OSCURO, negrita=True, centrado=True)

    self.sonidos.reproducir("gameover_retro")

# ===================================================================================
def updates_segun_estado(self):
    """Updates condicionales (presentacion / preparado / en_juego...)"""

    check_temporizador_azules(self)
    checkNivelSuperado(self)
    checkDelayNextLevel(self)
    self.instanciar_fruta_periodicamente()
    check_showbonus_fant_kill(self)

    if self.estado_juego["menu_presentacion"]:
        self.listas_sprites["textos"].update()
    
    elif self.estado_juego["preparado"]:
        calculo = pygame.time.get_ticks()
        if calculo - self.ultimo_update["preparado"] > self.CO.DURACION_PREPARADO:
            self.ultimo_update["preparado"] = calculo
            self.resetear_estados_juego()
            self.estado_juego["preparado"] = False
            self.estado_juego["en_juego"] = True
            eliminar_elemento_de_lista(self, "textos", "txt-preparado")
    
    else:
        self.listas_sprites["all_sprites"].update()
        self.listas_sprites["fantasmas"].update()
        self.listas_sprites["vidas"].update()
        self.listas_sprites["textos"].update()
    
    #self.checkTransicion_gameOverRejugar()

# ===================================================================================
def check_temporizador_azules(self):
    """Gestionar el tiempo en que los fantasmas permancen azules"""

    calculo = pygame.time.get_ticks()
    if self.temporizadorAzules and calculo - self.ultimo_update["azules"] > self.CO.DURACION_AZULES[self.nivel]:
        self.ultimo_update["azules"] = calculo
        print("tiempo-azules-agotado")
        self.temporizadorAzules = False
        self.sonidos.sonidos["fantasmas_azules"].stop()
        self.sumaPtosComeFantasmas = 100

        for fantasma in self.listas_sprites["fantasmas"]:
            fantasma.kill()
            x, y = int(fantasma.rect.x / self.CO.TX), int(fantasma.rect.y / self.CO.TY)
            self.instanciar_fantasma(x, y, fantasma.id_fantasma, fantasma.direccion, azul=False, ojos=False)

# ===================================================================================
def checkNivelSuperado(self):
    """Checkear si hemos comido todos los puntitos"""

    if self.estado_juego["nivel_superado"]:
        return
     
    if len(self.listas_sprites["puntitos"]) <= 0 and self.estado_juego["en_juego"]:
        self.sonidos.sonidos["fantasmas_azules"].stop()
        self.estado_juego["en_juego"] = False
        self.estado_juego["nivel_superado"] = True
        self.ultimo_update["nivel_superado_delay"] = pygame.time.get_ticks()
        self.sonidos.reproducir("intermision")
        print("nivel superado!")

# ===================================================================================
def checkDelayNextLevel(self):
    """Pausa/delay antes de pasar al siguiente nivel"""

    if not self.estado_juego["nivel_superado"]:
        return
    
    calculo = pygame.time.get_ticks()
    if calculo - self.ultimo_update["nivel_superado_delay"] > self.CO.DELAY_NEXT_LEVEL:
        self.nivel += 1
        self.resetear_estados_juego()
        self.estado_juego["preparado"] = True
        self.ultimo_update["preparado"] = pygame.time.get_ticks()
        self.new_game()

# ===================================================================================
def draw_listas_sprites(self):
    """Renderizar las listas-sprites"""

    self.listas_sprites["all_sprites"].draw(self.pantalla)
    self.listas_sprites["fantasmas"].draw(self.pantalla)
    self.listas_sprites["vidas"].draw(self.pantalla)

    # dibujar rectangulo "transparente" escapatoria
    pygame.draw.rect(self.pantalla, self.COL.GRIS_FONDO, 
        (self.CO.COLUMNAS * self.CO.TX, 11 * self.CO.TY, self.CO.TX, self.CO.TY))
    
    self.listas_sprites["textos"].draw(self.pantalla)

# ===================================================================================
def eventos_comenzar_quit_etc(self):
    """Eventos de teclado/click (comenzar partida / salir)"""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.program_running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.program_running = False
                pygame.quit()
                sys.exit()
            
            if (event.key == pygame.K_RETURN and self.estado_juego["menu_presentacion"]) or (event.key == pygame.K_RETURN and self.estado_juego["game_over"]):
                pygame.mixer.music.stop()
                self.resetear_estados_juego()
                self.estado_juego["preparado"] = True
                self.estado_juego["en_juego"] = True
                self.ultimo_update["preparado"] = pygame.time.get_ticks()

                if self.vidas <= 0:
                    self.vidas = 3
                    self.puntos = 0
                    self.nivel = 1
                
                # ************** Comenzar partida (Pulsando ENTER) ***********************
                self.new_game()

            if event.key == pygame.K_TAB:
                for clave in self.estado_juego:
                    print(clave, self.estado_juego[clave])

# ===================================================================================
def eliminar_elemento_de_lista(self, lista, elemento):
    """Eliminar un elemento de una lista de sprites en la que se encontraba"""
    for sprite in self.listas_sprites[lista]:
        if isinstance(sprite, Textos) and sprite.tipo == elemento:
            self.listas_sprites["textos"].remove(sprite)
            break

