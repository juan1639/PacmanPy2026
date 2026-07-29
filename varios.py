import pygame
from fantasmas import Fantasma, EstadoFantasmas

# ====================================================================================
#   varios.py (modulo de varias clases pequeñas que requieren poca logica)
#   class --> LaberintoTile, Puntitos, PuntosGordos, Textos, ItemFrutas
#
# ------------------------------------------------------------------------------------
class LaberintoTile(pygame.sprite.Sprite):
    """Funcion constructora"""
    def __init__(self, game, x, y, valor_tile):
        super().__init__()
        self.game = game
        self.TX = self.game.CO.TX
        self.TY = self.game.CO.TY

        nivel = 1   # bloquepac1
        self.image = self.game.obtener_grafico(f'bloquepac{nivel}.png', 1)[0]
        self.rect = self.game.obtener_grafico(f'bloquepac{nivel}.png', 1)[1]
        self.rect.x, self.rect.y = x * self.TX, y * self.TY
        self.valor = valor_tile

    def update(self):
        pass  # El laberinto no necesita actualización dinámica

# ====================================================================================
class LaberintoOrigTile(pygame.sprite.Sprite):
    """Funcion constructora"""
    def __init__(self, game, x, y, valor_tile):
        super().__init__()
        self.game = game
        self.TX = self.game.CO.TX
        self.TY = self.game.CO.TY

        if valor_tile == 8:
            self.image = self.game.obtener_grafico('tile-pac-rect.png', 1)[0]
            self.rect = self.game.obtener_grafico('tile-pac-rect.png', 1)[1]
        
        elif valor_tile == 7:
            self.image = self.game.obtener_grafico('tile-pac-circle-down-fondo.png', 1)[0]
            self.rect = self.game.obtener_grafico('tile-pac-circle-down-fondo.png', 1)[1]
        
        elif valor_tile == 6:
            self.image = self.game.obtener_grafico('tile-pac-circle-up-fondo.png', 1)[0]
            self.rect = self.game.obtener_grafico('tile-pac-circle-up-fondo.png', 1)[1]
        
        elif valor_tile == 4:
            self.image = self.game.obtener_grafico('tile-pac-circle-right-fondo.png', 1)[0]
            self.rect = self.game.obtener_grafico('tile-pac-circle-right-fondo.png', 1)[1]
        
        elif valor_tile == 3:
            self.image = self.game.obtener_grafico('tile-pac-circle-left-fondo.png', 1)[0]
            self.rect = self.game.obtener_grafico('tile-pac-circle-left-fondo.png', 1)[1]

        self.rect.x, self.rect.y = x * self.TX, y * self.TY
        self.valor = valor_tile

    def update(self):
        pass

# ====================================================================================
class Puntitos(pygame.sprite.Sprite):
    SUMA_PUNTOS = 10

    """Funcion constructora"""
    def __init__(self, game, x, y, valor_tile):
        super().__init__()
        self.game = game
        self.TX = self.game.CO.TX
        self.TY = self.game.CO.TY

        self.image = self.game.obtener_grafico('pildopac.png', 0.2)[0]
        self.rect = self.game.obtener_grafico('pildopac.png', 0.2)[1]
        self.rect.center = (x * self.TX + self.TX // 2, y * self.TY + self.TY // 2)
        self.valor = valor_tile

    def update(self):
        """Funcion que actualizara esta instancia en el main"""
        if pygame.sprite.spritecollide(self, self.game.listas_sprites["pacman"], False):
            self.kill()
            self.game.puntos += Puntitos.SUMA_PUNTOS
            #self.game.sonido_sirena.stop()
            self.game.sonidos.reproducir("wakawaka", duracion=450)

# ====================================================================================
class PuntosGordos(pygame.sprite.Sprite):
    """Funcion constructora"""
    def __init__(self, game, x, y, valor_tile):
        super().__init__()
        self.game = game
        self.TX = self.game.CO.TX
        self.TY = self.game.CO.TY

        self.escala = 0.5
        self.vel_anima = 150
        self.ultimo_update = pygame.time.get_ticks()

        self.image = self._cargar_imagen()[0]
        self.rect = self._cargar_imagen()[1]
        self.rect.center = (x * self.TX + self.TX // 2, y * self.TY + self.TY // 2)
        self.centerXY = self.rect.center
        self.valor = valor_tile
    
    # -------------------------------------------------------------------
    def _cargar_imagen(self):
        """Carga la imagen del punto gordo con la escala actual."""
        return self.game.obtener_grafico('puntoGordo.png', self.escala)
    
    # -------------------------------------------------------------------
    def _alternar_escala(self):
        """Alternar la escala entre 0.3 y 0.5."""
        self.escala = 0.3 if self.escala == 0.5 else 0.5
        self.image = self._cargar_imagen()[0]
        self.rect = self._cargar_imagen()[1]
    
    # -------------------------------------------------------------------
    def update(self):
        """Funcion que actualizara esta instancia en el main"""
        # Animación de escala
        if pygame.time.get_ticks() - self.ultimo_update > self.vel_anima:
            self.ultimo_update = pygame.time.get_ticks()
            self._alternar_escala()
            self.rect.center = self.centerXY

        # Colisión con PacMan
        if pygame.sprite.spritecollide(self, self.game.listas_sprites["pacman"], False) and not self.game.temporizadorAzules:
            self.kill()
            self.game.sonidos.reproducir("eating_ghost")
            self.game.sonidos.reproducir("fantasmas_azules")

            self.game.temporizadorAzules = True
            self.game.ultimo_update["azules"] = pygame.time.get_ticks()

            for fantasma in self.game.listas_sprites["fantasmas"]:
                fantasma.kill()
                x, y = int(fantasma.rect.x / self.game.CO.TX), int(fantasma.rect.y / self.game.CO.TY)
                self.game.instanciar_fantasma(x, y, fantasma.id_fantasma, fantasma.direccion, azul=True, ojos=False)

# =========================================================================================================
class Textos(pygame.sprite.Sprite):
    """Funcion constructora"""
    def __init__(self, game, texto, size, x, y, color, fondo=None, negrita=False, centrado=True, tipo=None):
        super().__init__()
        self.game = game
        self.texto = texto
        self.size = size
        self.color = color
        self.fondo = fondo
        self.centrado = centrado
        self.tipo = tipo
        self.font = pygame.font.SysFont('verdana', self.size)
        self.font.set_bold(negrita)
        self.image = self.font.render(self.texto, True, self.color, self.fondo)

        if self.centrado:
            self.rect = self.image.get_rect(center=(x, y))
        else:
            self.rect = self.image.get_rect(topleft=(x, y))
        
        # Identificar si se trata de un texto dinámico (puntos o nivel)
        #self.render_nivel = self.texto = str(self.game.nivel)

    def update(self):
        """Funcion que actualizara esta instancia en el main"""
        if self.tipo == "dinamico-puntos":
            self.image = self.font.render(f'{self.game.puntos}', True, self.color, self.fondo)
        if self.tipo == "dinamico-nivel":
            self.image = self.font.render(f'{self.game.nivel}', True, self.color, self.fondo)

        if self.tipo != None:
            if self.tipo.startswith("show-bonus"):
                self.rect.y -= 1

        """if Fantasma.estado_fantasmas == EstadoFantasmas.CHASE:
            self.image = self.font.render('Chase', True, self.color, self.fondo)
        elif Fantasma.estado_fantasmas == EstadoFantasmas.SCATTER:
            self.image = self.font.render('Scatter', True, self.color, self.fondo)"""

# ==================================================================================================
class ItemFrutas(pygame.sprite.Sprite):
    X, Y = 9, 11

    """Funcion constructora"""
    def __init__(self, game):
        super().__init__()
        self.game = game

        # Limitar el número máximo de niveles para la fruta
        item_nivel = min(self.game.nivel, 5)
        self.image, self.rect = self.game.obtener_grafico(f'item{item_nivel}.png', 1)
        self.rect.x, self.rect.y = ItemFrutas.X * self.game.CO.TX, ItemFrutas.Y * self.game.CO.TY

    def update(self):
        """Funcion que actualizara esta instancia en el main"""
        if pygame.sprite.spritecollide(self, self.game.listas_sprites["pacman"], False):
            self.kill()
            self.game.sonidos.reproducir("eating_cherry")
            puntos_fruta = (self.game.nivel * 10) ** 2
            self.game.puntos += puntos_fruta
            self.game.ultimo_update["item-fruta"] = pygame.time.get_ticks()
            
            self.game.instanciar_texto(str(puntos_fruta), 48, self.rect.x, self.rect.y, self.game.COL.NARANJA_ROJIZO_2,
                centrado=False, negrita=True, tipo="show-bonus-fruta")
            
            self.game.ultimo_update["show-bonus-fruta"] = pygame.time.get_ticks()


