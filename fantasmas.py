import pygame
import random
from enum import Enum
from laberintos import Pantallas
from tiles import TileType, paredes

# ====================================================================================
#   fantasmas.py (modulo logica de los fantasmas/enemigos)
#   class --> Fantasma, Direccion
#
# ------------------------------------------------------------------------------------
class Direccion(Enum):
    RIGHT = "ri"
    LEFT = "le"
    UP = "up"
    DOWN = "do"

class Fantasma(pygame.sprite.Sprite):
    def __init__(self, game, x, y, id_fantasma, dir_defecto, azul=False, ojos=False):
        super().__init__()
        self.game = game
        self.id_fantasma = id_fantasma
        self.direccion = dir_defecto
        self.azul = azul
        self.ojos = ojos
        self.velocidad = 2
        self.DISTANCIA_EXAGERADA = 9900

        # Diccionario de direcciones
        self.dic_direccion = self.generar_direcciones()

        # Puntos clave
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
        self.manejar_colisiones()
        self.verificar_colision_pacman()
    
    # ----------------------------------------------------------
    def generar_direcciones(self):
        """Generar las direcciones y configuraciones."""

        # Animacion-base (cuando estan azules/ojos hay menos graficos):
        anim_base = [0, 2, 4, 6] if self.azul or self.ojos else [0, 8, 16, 24]
        
        # Cuando estan azules/ojos hay menos graficos (no importa el color), entonces multiplicar=0
        multiplicar = 0 if self.azul or self.ojos else 2

        return {
            Direccion.RIGHT.value: [1, 0, anim_base[0] + self.id_fantasma * multiplicar, "updole", "ri", "le"],
            Direccion.LEFT.value: [-1, 0, anim_base[1] + self.id_fantasma * multiplicar, "updori", "le", "ri"],
            Direccion.UP.value: [0, -1, anim_base[2] + self.id_fantasma * multiplicar, "riledo", "up", "do"],
            Direccion.DOWN.value: [0, 1, anim_base[3] + self.id_fantasma * multiplicar, "rileup", "do", "up"]
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

    # ----------------------------------------------------------
    def manejar_colisiones(self):
        """Verificar y manejar colisiones del fantasma."""

        if self.rect.x % self.game.CO.TX == 0 and self.rect.y % self.game.CO.TY == 0:
            x, y = self.rect.x // self.game.CO.TX, self.rect.y // self.game.CO.TY

            lista_dir_posibles = self.obtener_direcciones_posibles(x, y)

            lista_distancias = []

            for posible in lista_dir_posibles:
                if posible:
                    calc_distancia = pow(abs(self.rect.x - self.game.pacman.rect.x), 2) + pow(abs(self.rect.y - self.game.pacman.rect.y), 2)
                    lista_distancias.append(calc_distancia)
                else:
                    lista_distancias.append(self.DISTANCIA_EXAGERADA)

            menor_distancia = min(lista_distancias)
            flag_elegir = False

            for idx in range(len(lista_distancias)):
                if lista_distancias[idx] == menor_distancia and not flag_elegir:
                    flag_elegir = True
                    if idx == 0:
                        self.direccion = "ri"
                    elif idx == 1:
                        self.direccion = "le"
                    elif idx == 2:
                        self.direccion = "up"
                    else:
                        self.direccion = "do"
            
            """if not self.colision_laberinto(x, y):
                self.vel_xy = self.dic_direccion[self.direccion][:2]
            else:
                self.elegir_direccion_alternativa()
                return"""

        self.vel_xy = self.dic_direccion[self.direccion][:2]
        self.rect.x += self.vel_xy[0] * self.velocidad
        self.rect.y += self.vel_xy[1] * self.velocidad
    
    # ----------------------------------------------------------
    def obtener_direcciones_posibles(self, x, y):
        lista_direcciones = []

        for direcciones in self.dic_direccion.values():
            if self.colision_laberinto_dir_validas(x, y, direcciones[0], direcciones[1]):
                lista_direcciones.append(False)
            else:
                if direcciones[5] == self.direccion:
                    lista_direcciones.append(False)
                else:
                    lista_direcciones.append(True)

        return lista_direcciones
    
    # ----------------------------------------------------------
    def colision_laberinto_dir_validas(self, x, y, offset_x, offset_y):
        if self.es_teletransporte(x, y, offset_x):
            return True
        
        indice = self.game.obtener_indice(x + offset_x, y + offset_y)
                
        if indice is None:
            return False

        return Pantallas.get_laberinto(self.game.nivel)[indice] in paredes
    
    # ----------------------------------------------------------
    def es_teletransporte(self, x, y, vel_x):
        if y == 11:  # Línea especial para teletransporte
            if x + vel_x > self.game.CO.COLUMNAS:
                self.rect.x = -self.game.CO.TX
                return True
            elif x + vel_x < -1:
                self.rect.x = self.game.CO.COLUMNAS * self.game.CO.TX
                return True
        return False
    
    # ----------------------------------------------------------
    def perseguir_pacman(self):
        """Actualizar dirección para perseguir a PacMan."""

        if random.randrange(100) > self.game.nivel * 30:
            return
        if random.randrange(10) < 5:  # Decisión horizontal/vertical
            self.direccion = Direccion.UP.value if self.game.pacman.rect.y < self.rect.y else Direccion.DOWN.value
        else:
            self.direccion = Direccion.LEFT.value if self.game.pacman.rect.x < self.rect.x else Direccion.RIGHT.value
        
        self.vel_xy = self.dic_direccion[self.direccion][:2]
    
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

