import pygame.transform

from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.UI.Entities.BaseUI import BaseUI
from scripts.constants import *
from scripts.Managers.GameAssets import tiles
from scripts.UI.Components.Bg import Bg


class MapUI(BaseUI, metaclass=UIRegistry):

    def __init__(self, parent):

        super().__init__(parent)

        self.map_surface = pg.Surface((CHUNK_SIZE * MAP_SIZE).as_tuple())
        self.map_pos = RESOLUTION // 2 - CHUNK_SIZE * MAP_SIZE * MAPUI_TILE_SIZE // 2
        self.bg = Bg()

        self.player_texture = load_texture("assets/player/down.png", Vector(32, 32))

        self.update_map_texture()

    def update_map_texture(self):

        self.map_surface = pg.Surface((CHUNK_SIZE * MAP_SIZE).as_tuple())

        for x in range(len(self.parent.world.data)):
            for y in range(len(self.parent.world.data[x])):

                tile = self.parent.world.data[x][y]
                color = tiles[tile].minimap_color

                self.map_surface.set_at((x, y), color)

        self.map_surface = pygame.transform.scale_by(self.map_surface, MAPUI_TILE_SIZE)

        self.bg.blit(self.map_surface, self.map_pos.as_tuple())

    def when_opened(self):

        self.update_map_texture()

    def draw(self, display):

        self.bg.draw()
        player_pos = self.parent.player.pos
        player_pos_tile = (player_pos // TILE_SIZE) * MAPUI_TILE_SIZE
        player_pos_on_map = self.map_pos + player_pos_tile
        screen.blit(self.player_texture, (player_pos_on_map - Vector(self.player_texture.get_size()) // 2).as_tuple())

    def update(self, obj):

        pass

    def events(self, events):

        pass
