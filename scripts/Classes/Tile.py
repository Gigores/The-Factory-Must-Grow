from dataclasses import dataclass, field
import pygame as pg
from scripts.constants import *


@dataclass
class Tile:

    texture_path: str
    name: str
    walk_speed: float
    walkable: bool
    minimap_color: str = None

    texture: pg.Surface = field(init=False, default=pg.Surface((1, 1)))

    def __post_init__(self):

        self.texture = load_texture(self.texture_path, TILE_SIZE)

        if not self.minimap_color:
            self.minimap_color = rgb_to_hex(calculate_average_color(self.texture, False))

    def get_data(self) -> dict:

        return {
            "name": self.name,
            "movement_speed": f"{int(self.walk_speed * 100)} %",
            "walkable": self.walkable,
        }
