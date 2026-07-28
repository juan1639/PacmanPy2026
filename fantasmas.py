import pygame
from enum import Enum
from laberintos import Pantallas
from tiles import TileType, paredes
import random

# ====================================================================================
#   fantasmas.py (modulo logica de los fantasmas/enemigos)
#   class --> Fantasma, Direccion
#
# ------------------------------------------------------------------------------------
class Direccion(Enum):
    UP = "up"
    LEFT = "le"
    DOWN = "do"
    RIGHT = "ri"

class EstadoFantasmas(Enum):
    CHASE = "chase"
    SCATTER = "scatter"
    AZULES = "azules"
    OJOS = "ojos"

class Fantasma(pygame.sprite.Sprite):
    estado_fantasmas = EstadoFantasmas.SCATTER

    """Funcion constructora"""
    def __init__(self, game, x, y, id_fantasma, dir_defecto, azul=False, ojos=False, scatterX=random.randint(2, 12), scatterY=8):
        super().__init__()
        self.game = game
        self.id_fantasma = id_fantasma
        self.direccion = dir_defecto
        self.azul = azul
        self.ojos = ojos
        self.velocidad = 2
        self.scatter_x = scatterX
        self.scatter_y = scatterY
        self.set_estado_fantasmas_default_al_instanciar()

        # dict_movimientos:
        self.DICT_MOVIMIENTOS = {
            "up": (0, -1),
            "le": (-1, 0),
            "do": (0, 1),
            "ri": (1, 0)
        }

        self.DICT_OPUESTA = {
            "up": "do",
            "do": "up",
            "le": "ri",
            "ri": "le"
        }

        # Orden de prioridad EXACTO del arcade
        self.PRIORIDAD = ["up", "le", "do", "ri"]

        # Diccionario de direcciones
        self.dic_direccion = self.generar_direcciones()

        # Puntos clave *** NO UTILIZADA, debido a la IA fantasmas ***
        self.ptos_clave = self.procesar_puntos_clave([
            (75, 425), (225, 225), (225, 425), (225, 675), (225, 575),
            (325, 575), (225, 75), (425, 425), (325, 225),
            (875, 425), (725, 225), (725, 425), (725, 675), (725, 575),
            (625, 575), (725, 75), (525, 425), (625, 225)
        ])

        # Animaciones
        self.lista_imagenes = self.cargar_imagenes()
        self.indice_animacion = 0
        self.image = self.lista_imagenes[0 + self.id_fantasma * 2]
        self.rect = self.image.get_rect()
        self.rect.x = x * self.game.CO.TX
        self.rect.y = y * self.game.CO.TY

        # Radius (reducir el radio, para hacer mas permisiva la colision)...
        # ... y mas jugable... radius= 25 (default) --> reducido a 15
        self.radius = 20

        # Estados
        self.vel_xy = self.dic_direccion[self.direccion][:2]
        self.ultimo_update = pygame.time.get_ticks()
        self.fotograma_vel = 100  # Velocidad de animación
    
    # ----------------------------------------------------------
    def update(self):
        if not self.game.estado_juego["en_juego"]:
            return
        
        self.actualizar_animacion()
        self.mover_fantasmas()
        self.verificar_colision_pacman()
    
    # ----------------------------------------------------------
    def set_estado_fantasmas_default_al_instanciar(self):
        if self.ojos:
            Fantasma.estado_fantasmas = EstadoFantasmas.SCATTER
        elif self.azul:
            Fantasma.estado_fantasmas = EstadoFantasmas.SCATTER
        else:
            self.game.ultimo_update["estado_fantasmas"] = pygame.time.get_ticks()

            if self.game.index_estado_fantasmas % 2 == 0:
                Fantasma.estado_fantasmas = EstadoFantasmas.SCATTER
            else:
                Fantasma.estado_fantasmas = EstadoFantasmas.CHASE
    
    # ----------------------------------------------------------
    def generar_direcciones(self):
        """Generar las direcciones y configuraciones."""

        # Animacion-base (cuando estan azules/ojos hay menos graficos):
        anim_base = [0, 2, 4, 6] if self.azul or self.ojos else [0, 8, 16, 24]
        
        # Cuando estan azules/ojos hay menos graficos (no importa el color), entonces multiplicar=0
        multiplicar = 0 if self.azul or self.ojos else 2

        return {
            Direccion.UP.value: [0, -1, anim_base[2] + self.id_fantasma * multiplicar, "riledo", "up", "do"],
            Direccion.LEFT.value: [-1, 0, anim_base[1] + self.id_fantasma * multiplicar, "updori", "le", "ri"],
            Direccion.DOWN.value: [0, 1, anim_base[3] + self.id_fantasma * multiplicar, "rileup", "do", "up"],
            Direccion.RIGHT.value: [1, 0, anim_base[0] + self.id_fantasma * multiplicar, "updole", "ri", "le"]
        }
    
    # ----------------------------------------------------------
    def procesar_puntos_clave(self, puntos_crudos):
        """Convertir puntos clave a coordenadas del tablero."""
        return [(int((pcx - 25) // 50), int((pcy - 25) // 50)) for pcx, pcy in puntos_crudos]

    # ----------------------------------------------------------
    def cargar_imagenes(self):
        """Cargar imágenes según el estado del fantasma."""

        if self.ojos:
            return [self.game.obtener_grafico(f"fantasma{i + 51}.png", 1)[0] for i in range(8)]
        elif self.azul:
            return [self.game.obtener_grafico(f"fantasmaAzul{i + 1}.png", 1)[0] for i in range(8)]
        else:
            return [
                self.game.obtener_grafico(f"fantasma{i + 1}.png", 1)[0]
                for i in range(38) if i not in [8, 9, 18, 19, 28, 29]
            ]
    
    # ---------------------------------------------------------
    def mover_fantasmas(self):
        """Movimiento de los fantasmas."""

        if self.rect.x % self.game.CO.TX == 0 and self.rect.y % self.game.CO.TY == 0:

            tile_x = self.rect.x // self.game.CO.TX
            tile_y = self.rect.y // self.game.CO.TY

            self.elegir_direccion(tile_x, tile_y)

        # obtener los offset y mover pacman:
        self.vel_xy = self.dic_direccion[self.direccion][:2]

        self.rect.x += self.vel_xy[0] * self.velocidad
        self.rect.y += self.vel_xy[1] * self.velocidad
    
    # ----------------------------------------------------------
    def elegir_direccion(self, x, y):
        """Elegir una direccion (IA fantasmas)"""

        mejor_dir = None
        mejor_dist = float("inf")

        for direccion in self.PRIORIDAD:
            # No permitir media vuelta
            if direccion == self.DICT_OPUESTA[self.direccion]:
                continue

            # Hay pared
            if not self.direccion_valida(x, y, direccion):
                continue

            # Esta teletransportandose:
            if self.rect.x // self.game.CO.TX >= self.game.CO.COLUMNAS - 1 or self.rect.x <= 0:
                continue

            dx, dy = self.DICT_MOVIMIENTOS[direccion]

            nuevo_x = x + dx
            nuevo_y = y + dy

            objetivo_x, objetivo_y = self.obtener_objetivo()

            distancia = (nuevo_x - objetivo_x) ** 2 + (nuevo_y - objetivo_y) ** 2

            if distancia < mejor_dist:
                mejor_dist = distancia
                mejor_dir = direccion

        # Callejón sin salida
        if mejor_dir is None:
            mejor_dir = self.DICT_OPUESTA[self.direccion]

        self.direccion = mejor_dir
    
    # ----------------------------------------------------------
    def direccion_valida(self, x, y, direccion):
        """Verificar si una direccion es valida (que no haya pared)"""

        dx, dy = self.DICT_MOVIMIENTOS[direccion]

        if self.es_teletransporte(x, y, dx):
            return True

        indice = self.game.obtener_indice(x + dx, y + dy)

        if indice is None:
            return True

        return Pantallas.get_laberinto(self.game.nivel)[indice] not in paredes

    # ----------------------------------------------------------
    def es_teletransporte(self, x, y, vel_x):
        """11=Fila en la que puede haber teletransporte"""
        if y == 11:
            if x + vel_x > self.game.CO.COLUMNAS:
                self.rect.x = -self.game.CO.TX
                return True
            elif x + vel_x < -1:
                self.rect.x = self.game.CO.COLUMNAS * self.game.CO.TX
                return True
        return False
    
    # ----------------------------------------------------------
    def obtener_objetivo(self):
        """Devuelve las coord x,y de Pacman"""
        return self.obtener_objetivo_seleccionando_current_fantasma()
    
    # ----------------------------------------------------------
    def obtener_objetivo_seleccionando_current_fantasma(self):
        """El objetivo es diferente dependiendo del fantasma (cada fantasma IA diferente)"""

        if self.id_fantasma == 0:
            return self.objetivo_blinky()
        elif self.id_fantasma == 1:
            return self.objetivo_pinky()
        elif self.id_fantasma == 2:
            return self.objetivo_inky()
        else:
            return self.objetivo_clyde()

    # ----------------------------------------------------------
    def objetivo_blinky(self):
        """- Blinky - persigue DIRECTAMENTE a Pacman"""

        if Fantasma.estado_fantasmas == EstadoFantasmas.CHASE:
            return (self.game.pacman.rect.x // self.game.CO.TX, self.game.pacman.rect.y // self.game.CO.TY)
        
        elif Fantasma.estado_fantasmas == EstadoFantasmas.SCATTER:
            return (self.scatter_x, self.scatter_y)

    # ----------------------------------------------------------
    def objetivo_pinky(self):
        """- Pinky - tiene como objetivo 4 casillas de antelacion a Pacman"""

        if Fantasma.estado_fantasmas == EstadoFantasmas.CHASE:
            pac_x = self.game.pacman.rect.x // self.game.CO.TX
            pac_y = self.game.pacman.rect.y // self.game.CO.TY

            dx, dy = self.game.pacman.movimientos[self.game.pacman.direccion_confirmada][:2]

            CASILLAS_ANTELACION = 4

            objetivo_x = pac_x + dx * CASILLAS_ANTELACION
            objetivo_y = pac_y + dy * CASILLAS_ANTELACION

            return objetivo_x, objetivo_y

        elif Fantasma.estado_fantasmas == EstadoFantasmas.SCATTER:
            return (self.scatter_x, self.scatter_y)

    # ----------------------------------------------------------
    def objetivo_inky(self):
        """ - Inky - tiene como objetivo un VECTOR entre Pacman y Blinky"""

        if Fantasma.estado_fantasmas == EstadoFantasmas.CHASE:
            pac_x = self.game.pacman.rect.x // self.game.CO.TX
            pac_y = self.game.pacman.rect.y // self.game.CO.TY

            dx, dy = self.game.pacman.movimientos[self.game.pacman.direccion_confirmada][:2]

            # Dos casillas delante de Pac-Man
            punto_x = pac_x + dx * 2
            punto_y = pac_y + dy * 2

            # Buscar a Blinky
            blinky = None

            for fantasma in self.game.listas_sprites["fantasmas"]:
                if fantasma.id_fantasma == 0:
                    blinky = fantasma
                    break

            blinky_x = blinky.rect.x // self.game.CO.TX
            blinky_y = blinky.rect.y // self.game.CO.TY

            objetivo_x = 2 * punto_x - blinky_x
            objetivo_y = 2 * punto_y - blinky_y

            return objetivo_x, objetivo_y

        elif Fantasma.estado_fantasmas == EstadoFantasmas.SCATTER:
            return (self.scatter_x, self.scatter_y)

    # ----------------------------------------------------------
    def objetivo_clyde(self):
        """ - Clyde - tiene como objetivo Pacman, pero si se acerca, se - asusta -"""

        if Fantasma.estado_fantasmas == EstadoFantasmas.CHASE:
            pac_x = self.game.pacman.rect.x // self.game.CO.TX
            pac_y = self.game.pacman.rect.y // self.game.CO.TY

            clyde_x = self.rect.x // self.game.CO.TX
            clyde_y = self.rect.y // self.game.CO.TY

            distancia2 = (pac_x - clyde_x) ** 2 + (pac_y - clyde_y) ** 2

            # 8² = 64
            if distancia2 > 64:
                # Perseguir a Pac-Man
                return pac_x, pac_y
            else:
                # Esquina inferior izquierda
                return (self.scatter_x, self.scatter_y)

        elif Fantasma.estado_fantasmas == EstadoFantasmas.SCATTER:
            return (self.scatter_x, self.scatter_y)
    
    # ----------------------------------------------------------
    def actualizar_animacion(self):
        """Actualizar el fotograma actual del fantasma."""

        if pygame.time.get_ticks() - self.ultimo_update > self.fotograma_vel:
            self.ultimo_update = pygame.time.get_ticks()
            self.indice_animacion = 1 - self.indice_animacion  # Alterna entre 0 y 1
            base = self.dic_direccion[self.direccion][2]
            self.image = self.lista_imagenes[base + self.indice_animacion]

            """ if self.azul:
                self.image.set_alpha(100 if self.game.obtenerDuracionAzules() > 0 else 255) """
    
    # ----------------------------------------------------------
    def verificar_colision_pacman(self):
        """Verificar colisiones con PacMan."""

        if self.ojos or self.game.CO.INVULNERABLE:
            return
        
        colision = pygame.sprite.spritecollide(
            self, self.game.listas_sprites["pacman"], not self.azul, pygame.sprite.collide_circle
        )

        for impacto in colision:
            if self.azul:
                self.manejar_colision_comido()
            else:
                self.manejar_colision_atrapa_pacman(impacto)
    
    # ----------------------------------------------------------
    def manejar_colision_comido(self):
        """Manejar cuando PacMan come al fantasma azul."""

        self.game.sonidos.reproducir("eating_ghost")
        self.kill()

        coor_x = self.rect.x // self.game.CO.TX
        coor_y = self.rect.y // self.game.CO.TY
        self.game.sumaPtosComeFantasmas *= 2
        self.game.puntos += self.game.sumaPtosComeFantasmas
        #self.game.instanciaPtosComeFantasmas(self.game.sumaPtosComeFantasmas, coor_x, coor_y)
        self.game.instanciar_fantasma(coor_x, coor_y, self.id_fantasma, self.direccion, False, True)

        self.game.instanciar_texto(str(self.game.sumaPtosComeFantasmas), 48, self.rect.x, self.rect.y, self.game.COL.NARANJA_ROJIZO,
            centrado=False, negrita=True, tipo=f"show-bonus-fantasma{self.id_fantasma}")
        
        self.game.ultimo_update[f"show-bonus-fantasma{self.id_fantasma}"] = pygame.time.get_ticks()
    
    # ----------------------------------------------------------
    def manejar_colision_atrapa_pacman(self, impacto):
        """Manejar cuando el fantasma atrapa a PacMan."""
        self.game.sonidos.reproducir("pacman_dies")
        self.game.instanciar_pacman_dies(impacto.rect.x, impacto.rect.y)


