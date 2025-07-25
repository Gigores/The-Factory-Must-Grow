import numpy as np
from scripts.Managers.GameAssets import *


class Map:
    
    class Chunk(pg.Surface):

        def __init__(self, parent, pos: Vector):

            super().__init__((CHUNK_SIZE * TILE_SIZE).as_tuple())
            self.parent = parent
            self.pos = pos

        def update(self):

            for x in range(CHUNK_SIZE.x):
                for y in range(CHUNK_SIZE.y):
                    tile_x = x + self.pos.x * CHUNK_SIZE.x
                    tile_y = y + self.pos.y * CHUNK_SIZE.y

                    screen_x = x * TILE_SIZE.x
                    screen_y = y * TILE_SIZE.y

                    self.blit(tiles[self.parent.data[tile_x, tile_y]].texture, (screen_x, screen_y))

                    # pg.draw.rect(self, "#ff0000", (0, 0, CHUNK_SIZE.x * TILE_SIZE.x, CHUNK_SIZE.y * TILE_SIZE.y), 5)

        def __repr__(self):

            return f"chunk at {self.pos}"

    def __init__(self, parent):

        self.parent = parent
        self.data = np.full((MAP_SIZE * CHUNK_SIZE).as_tuple(), 255, dtype=np.uint8)
        self.chunks = \
            np.array([[self.Chunk(self, Vector(x, y)) for y in range(MAP_SIZE.y)] for x in range(MAP_SIZE.x)])

        # self.update_chunks()

    def update_chunks(self):

        for x in range(len(self.chunks)):
            for chunk in self.chunks[x]:
                chunk.update()

    def update_chunk(self, x, y):

        self.chunks[x][y].update()

    def set(self, pos: Vector, tile_id: int):

        self.data[pos.x][pos.y] = tile_id

    def get(self, pos: Vector) -> np.uint8 | None:

        try:
            return self.data[pos.x][pos.y]
        except:
            return None

    def draw(self):

        # chunk_x = int(self.parent.player.pos.x // TILE_SIZE.x // CHUNK_SIZE.x)
        # chunk_y = int(self.parent.player.pos.y // TILE_SIZE.y // CHUNK_SIZE.y)

        entity_manager = self.parent.entity_manager
        offset_x, offset_y = self.parent.offset.as_tuple()
        chunk_size_x_tile_size_x = CHUNK_SIZE.x * TILE_SIZE.x
        chunk_size_y_tile_size_y = CHUNK_SIZE.y * TILE_SIZE.y

        blit = self.parent.screen.blit
        chunks = self.chunks

        for chunk_pos in entity_manager.chunks:

            screen_x = (chunk_pos.x * chunk_size_x_tile_size_x) + offset_x
            screen_y = (chunk_pos.y * chunk_size_y_tile_size_y) + offset_y
            blit(chunks[chunk_pos.x][chunk_pos.y], (screen_x, screen_y))

        # for x in range(len(self.chunks)):
        #     for y, chunk in enumerate(self.chunks[x]):
        #         screen_x = (x * CHUNK_SIZE.x * TILE_SIZE.x) + self.parent.offset.x
        #         screen_y = (y * CHUNK_SIZE.y * TILE_SIZE.y) + self.parent.offset.y

        #         self.parent.screen.blit(chunk, (screen_x, screen_y))

    def dumb(self) -> list:

        return [[int(item) for item in ray] for ray in self.data]

    def load(self, data: str):

        self.data = np.array(data)
        self.update_chunks()
