from enum import Enum

class TileType(Enum):
    WALL = 9
    DOT = 1
    POWER_DOT = 5
    WALL_RECT = 8
    WALL_DOWN = 7
    WALL_UP = 6
    WALL_RIGHT = 4
    WALL_LEFT = 3

paredes = [
    TileType.WALL.value,
    TileType.WALL_RECT.value,
    TileType.WALL_DOWN.value,
    TileType.WALL_UP.value,
    TileType.WALL_RIGHT.value,
    TileType.WALL_LEFT.value
]
