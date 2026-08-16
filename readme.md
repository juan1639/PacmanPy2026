# PAC CLON 2026
## Recreación del juego clásico Pacman en Python
## El comportamiento de los fantasmas es casi
## igual que en el arcade original

- Como se puede ver en el gráfico, el fantasma rojo tiene como objetivo la posición exacta de Pacman.
- El verde tiene como objetivo, 4 casillas delante de Pacman.
- En cuanto al azul, el objetivo es un vector entre Pacman y el fantasma rojo.
- El naranja es igual que el rojo, pero al igual que el juego original, al acercarse mucho se 'asusta'.

<img src="pacGraf/pac-explain-ghosts.png" alt="game img"/>
<img src="miniatura-pacClon2025-1.png" alt="game img"/>
<img src="pacman-diagrama-1.png" alt="game img"/>
**Coordinación (Game Manager):**
- main.py
Game
 ├── estado
 ├── puntuación
 ├── vidas
 ├── nivel
 ├── sprites
 └── game loop
**Módulos de lógica:**
- jugador.py    → Pac-Man
- fantasmas.py  → IA/enemigos
- funciones.py  → lógica de juego
**Módulos de soporte:**
- laberintos.py → mapas
- tiles.py      → tipos de casillas
- varios.py     → objetos auxiliares
- settings.py   → configuración
- utils.py      → recursos/PyInstaller
---------------------------------------------------------
Game()
  │
  ▼
bucle_principal()
  │
  └────── mientras program_running ──────┐
                                         │
                 ┌───────────────────────┘
                 ▼
          check_event()
                 │
                 ▼
        Eventos teclado/ratón
                 │
                 ▼
             update()
                 │
                 ▼
       updates_segun_estado()
                 │
          ┌──────┴──────┐
          ▼             ▼
      Pac-Man       Fantasmas
          │             │
          ▼             ▼
      Colisiones      IA/movimiento
          │             │
          └──────┬──────┘
                 ▼
              draw()
                 │
                 ▼
          pygame.display.flip()
                 │
                 ▼
             siguiente
              frame
---------------------------------------------------------
              Tecla pulsada
                    │
                    ▼
          direccion_actual
                    │
                    ▼
       ¿Estoy en centro de tile?
             /           \
           NO             SÍ
           │               │
           │               ▼
           │      ¿La dirección deseada
           │       está libre?
           │          /          \
           │        SÍ            NO
           │        │              │
           │        ▼              ▼
           │   Cambiar dirección   Mantener
           │                       dirección
           │
           └───────────┬────────────
                       ▼
                 Mover Pac-Man
--------------------------------------------------------
Fantasma
   │
   ▼
¿Centro de tile?
   │
   ├── NO ──► seguir dirección
   │
   └── SÍ
         │
         ▼
   obtener objetivo
         │
         ▼
   mirar direcciones posibles
         │
         ├── ¿hay pared? ──► descartar
         │
         ├── ¿es dirección opuesta? ──► descartar
         │
         └── dirección válida
                    │
                    ▼
          calcular distancia²
             al objetivo
                    │
                    ▼
          elegir la menor
                    │
                    ▼
             mover fantasma
---------------------------------------------------------
                 ┌───────────────┐
                 │  PRESENTACIÓN │
                 └───────┬───────┘
                         │ ENTER
                         ▼
                 ┌───────────────┐
                 │   PREPARADO   │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │    EN JUEGO   │
                 └───────┬───────┘
                    ┌────┴────┐
                    │         │
              Pac-Man muere   │
                    │         │
                    ▼         │
              ¿vidas > 0?     │
                /      \      │
              SÍ        NO    │
              │          │    │
              ▼          ▼    │
          continuar   GAME OVER
                             │
                             ▼
                           ENTER

       EN JUEGO
          │
          ▼
   ¿quedan puntos?
      /       \
    SÍ         NO
    │           │
    │           ▼
    │      NIVEL SUPERADO
    │           │
    │           ▼
    │      siguiente nivel
    │           │
    └───────────┘
