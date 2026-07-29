import pygame
import sys
from jugador import PacMan, PacmanShowVidas
from fantasmas import Fantasma, EstadoFantasmas
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
                self.listas_sprites["laberinto"].add(tileOrig)

            elif valor_tile == TileType.WALL_DOWN.value:
                tileOrig = LaberintoOrigTile(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(tileOrig)
                self.listas_sprites["laberinto"].add(tileOrig)
            
            elif valor_tile == TileType.WALL_UP.value:
                tileOrig = LaberintoOrigTile(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(tileOrig)
                self.listas_sprites["laberinto"].add(tileOrig)
            
            elif valor_tile == TileType.WALL_RIGHT.value:
                tileOrig = LaberintoOrigTile(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(tileOrig)
                self.listas_sprites["laberinto"].add(tileOrig)
            
            elif valor_tile == TileType.WALL_LEFT.value:
                tileOrig = LaberintoOrigTile(self, ii, i, valor_tile)
                self.listas_sprites["all_sprites"].add(tileOrig)
                self.listas_sprites["laberinto"].add(tileOrig)

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

    #print(f"{self.index_estado_fantasmas}:{Fantasma.estado_fantasmas}")
    #print(len(self.listas_sprites["puntitos"]))
    
    check_temporizador_azules(self)
    check_temporizador_estados_fantasmas(self)
    checkNivelSuperado(self)
    checkDelayNextLevel(self)
    self.instanciar_fruta_periodicamente()
    check_showbonus_fant_kill(self)

    if self.estado_juego["menu_presentacion"] and not self.pantalla_info:
        self.listas_sprites["textos"].update()
        self.listas_sprites['pacman_intro'].update()
    elif self.estado_juego["menu_presentacion"] and self.pantalla_info:
        pass
    
    elif self.estado_juego["preparado"]:
        calculo = pygame.time.get_ticks()
        if calculo - self.ultimo_update["preparado"] > self.CO.DURACION_PREPARADO:
            self.ultimo_update["preparado"] = calculo
            self.ultimo_update["estado_fantasmas"] = pygame.time.get_ticks()
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
def check_temporizador_estados_fantasmas(self):
    """Gestionar el tiempo de duracion (scatter, chase, scatter...)"""

    # max nivel 5 ... a partir de ahi siempre 5:
    nivel_conf = self.nivel if self.nivel <= 5 else 5

    if not self.estado_juego['en_juego']:
        return

    if self.index_estado_fantasmas >= len(self.CO.DURACION_ESTADO[nivel_conf]):
        return
    
    calculo = pygame.time.get_ticks()
    if calculo - self.ultimo_update['estado_fantasmas'] > self.CO.DURACION_ESTADO[nivel_conf][self.index_estado_fantasmas]:
        self.index_estado_fantasmas += 1
        self.ultimo_update["estado_fantasmas"] = calculo

        if self.index_estado_fantasmas % 2 == 0:
            Fantasma.estado_fantasmas = EstadoFantasmas.SCATTER
        else:
            Fantasma.estado_fantasmas = EstadoFantasmas.CHASE

# ===================================================================================
def checkNivelSuperado(self):
    """Checkear si hemos comido todos los puntitos"""

    if self.estado_juego["nivel_superado"]:
        return
     
    if len(self.listas_sprites["puntitos"]) <= 0 and self.estado_juego["en_juego"]:
        # *** Vida extra al llegar a los niveles: 2, 5 y 10 ***
        if self.nivel == 1 or self.nivel == 4 or self.nivel == 9:
            self.instanciar_texto(" Vida", 64, self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES, self.CO.RESOLUCION[1] - 190, self.COL.NARANJA_EXTRA, negrita=True, centrado=False)
            self.instanciar_texto("Extra!", 64, self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES, self.CO.RESOLUCION[1] - 124, self.COL.NARANJA_EXTRA, negrita=True, centrado=False)
            self.vidas += 1
        
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
        self.index_estado_fantasmas = 0
        self.ultimo_update['estado_fantasmas'] = pygame.time.get_ticks()
        self.resetear_estados_juego()
        self.estado_juego["preparado"] = True
        self.ultimo_update["preparado"] = pygame.time.get_ticks()
        self.new_game()

# ===================================================================================
def draw_listas_sprites(self):
    """Renderizar las listas-sprites"""

    if self.estado_juego["menu_presentacion"] and not self.pantalla_info:
        self.renderizar_boton_info()
        self.listas_sprites['pacman_intro'].draw(self.pantalla)
    elif self.estado_juego["menu_presentacion"] and self.pantalla_info:
        self.renderizar_boton_info()
        renderizar_explain(self)

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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.estado_juego['menu_presentacion'] and event.button == 1: # Botón izquierdo
                mouse_x, mouse_y = event.pos
                print(mouse_x, mouse_y)

            if self.boton_settings.collidepoint(event.pos):
                print("info")
                self.sonidos.reproducir("eating_ghost")
                self.pantalla_info = True if not self.pantalla_info else False

                if not self.pantalla_info:
                    self.listas_sprites['textos'].empty()
                    self.instanciar_texto(self.CO.TXT_TITULO, 135, self.CO.RESOLUCION[0] // 2, 200, self.COL.NARANJA, negrita=True)
                    self.instanciar_texto(self.CO.TXT_BUTTON_INFO, 48, self.CO.RESOLUCION[0] // 2, self.CO.RESOLUCION[1] - 200, self.COL.AMARILLENTO, negrita=True)
                    self.instanciar_texto("Pulse ENTER para comenzar...", 32, self.CO.RESOLUCION[0] // 2, self.CO.RESOLUCION[1] - 80, self.COL.AMARILLENTO)

                elif self.pantalla_info:
                    self.listas_sprites["textos"].empty()
                    MARGIN_LEFT = self.CO.RESOLUCION[0] // 2.15
                    MARGIN_TOP = 12
                    INTERLINEAS = 24
                    pos_y = MARGIN_TOP

                    self.instanciar_texto(" Volver ", 40, self.CO.RESOLUCION[0] // 2, self.CO.RESOLUCION[1] - 200, self.COL.BLANCO, negrita=True)

                    self.instanciar_texto("Al igual que en el juego original, cada fantasma", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("tiene un comportamiento propio como se puede", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("ver en el gráfico.", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("                                            ", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("El rojo tiene como objetivo la posición exacta", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("de Pacman, mientras que el verde apunta cuatro", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("posiciones por delante.", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("                                              ", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("El azul calcula un vector intermedio entre Pacman", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("y el fantasma rojo.", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("                                             ", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("Por último, el fantasma llamado tonto, en realidad", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("tiene el mismo comportamiento que el rojo, salvo", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("que parece asustarse cuando se acerca mucho", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("ya que está programado para alejarse en tal caso.", 24, MARGIN_LEFT, pos_y, self.COL.BLANCO, negrita=False, centrado=False)

                    pos_y += INTERLINEAS * 2
                    self.instanciar_texto("Pueden cambiarse algunos settings del juego", 24, MARGIN_LEFT, pos_y, self.COL.AMARILLENTO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("editando el archivo config.ini", 24, MARGIN_LEFT, pos_y, self.COL.AMARILLENTO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("(Para restaurar los valores default bastará con", 24, MARGIN_LEFT, pos_y, self.COL.AMARILLENTO, negrita=False, centrado=False)
                    pos_y += INTERLINEAS
                    self.instanciar_texto("borrar dicho archivo. Se creará uno nuevo).", 24, MARGIN_LEFT, pos_y, self.COL.AMARILLENTO, negrita=False, centrado=False)
                    self.instanciar_texto(" Programmed in python by Juan Eguía, 2026 ", 28, self.CO.RESOLUCION[0] // 2, self.CO.RESOLUCION[1] - 60, self.COL.NARANJA_ROJIZO, negrita=False, centrado=True)

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
                    self.index_estado_fantasmas = 0
                    self.vidas = 3
                    self.puntos = 0
                    self.nivel = 1
                
                # ************** Comenzar partida (Pulsando ENTER) ***********************
                self.new_game()

            if event.key == pygame.K_TAB:
                for clave in self.estado_juego:
                    print(clave, self.estado_juego[clave])

# ===================================================================================
def renderizar_boton_info_hover(self):
    self.boton_settings = pygame.Rect(self.CO.RESOLUCION[0] // 2, self.CO.RESOLUCION[1] - 200 + 4, 200, 90)
    self.boton_settings.center = (self.CO.RESOLUCION[0] // 2, self.CO.RESOLUCION[1] - 200 + 4)

    mouse = pygame.mouse.get_pos()

    if self.boton_settings.collidepoint(mouse):
        color = self.COL.AZUL_C
    else:
        color = self.COL.VERDE_FONDO

    pygame.draw.rect(self.pantalla, color, self.boton_settings, border_radius=8)
    
# ===================================================================================
def renderizar_explain(self):
    #self.explain_rect.center = (self.CO.RESOLUCION[0] // 2, self.CO.RESOLUCION[1] // 2)
    self.pantalla.blit(self.explain_img, (0, 0))

# ===================================================================================
def eliminar_elemento_de_lista(self, lista, elemento):
    """Eliminar un elemento de una lista de sprites en la que se encontraba"""
    for sprite in self.listas_sprites[lista]:
        if isinstance(sprite, Textos) and sprite.tipo == elemento:
            self.listas_sprites["textos"].remove(sprite)
            break

