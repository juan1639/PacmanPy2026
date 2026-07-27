# ----------------------------------------------------------
def manejar_colisiones_NOVALE(self):
    """Verificar y manejar colisiones del fantasma."""

    if self.rect.x % self.game.CO.TX == 0 and self.rect.y % self.game.CO.TY == 0:
        x, y = self.rect.x // self.game.CO.TX, self.rect.y // self.game.CO.TY

        if (x, y) in self.ptos_clave:
            self.perseguir_pacman()
        
        if not self.colision_laberinto(x, y):
            self.vel_xy = self.dic_direccion[self.direccion][:2]
        else:
            self.elegir_direccion_alternativa()
            return

    self.rect.x += self.vel_xy[0] * self.velocidad
    self.rect.y += self.vel_xy[1] * self.velocidad

# ----------------------------------------------------------
def elegir_direccion_alternativa(self):
    """Elegir otra dirección al encontrar un obstáculo."""

    opciones = self.dic_direccion[self.direccion][3]
    aleatorio = random.randrange(0, 3) * 2
    nueva_direccion = opciones[aleatorio: aleatorio + 2]
    self.direccion = nueva_direccion
    self.vel_xy = self.dic_direccion[self.direccion][:2]

# ----------------------------------------------------------
def colision_laberinto(self, x, y):
    """Determinar si hay colisión con el laberinto."""

    if self.es_teletransporte(x, y, self.vel_xy[0]):
        return False
    
    indice = self.game.obtener_indice(x + self.vel_xy[0], y + self.vel_xy[1])
    
    if indice is None:
        return False
    
    return Pantallas.get_laberinto(self.game.nivel)[indice] in paredes

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
"""def colision_laberinto_dir_validas(self, x, y, offset_x, offset_y):
    if self.es_teletransporte(x, y, offset_x):
        return True
    
    indice = self.game.obtener_indice(x + offset_x, y + offset_y)
            
    if indice is None:
        return False

    return Pantallas.get_laberinto(self.game.nivel)[indice] in paredes"""

# ----------------------------------------------------------
"""def es_teletransporte(self, x, y, vel_x):
    if y == 11:  # Línea especial para teletransporte
        if x + vel_x > self.game.CO.COLUMNAS:
            self.rect.x = -self.game.CO.TX
            return True
        elif x + vel_x < -1:
            self.rect.x = self.game.CO.COLUMNAS * self.game.CO.TX
            return True
    return False"""



