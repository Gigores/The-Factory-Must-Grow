from scripts.constants import *
from scripts.Entities.ABC.Building import Building
import pygame as pg


TEXTURE_OFFSET = WALL_SIZE * Vector(-0.5, -0.75)
TOUCH_HITBOX_SIZE = TILE_SIZE
TOUCH_HITBOX_OFFSET = WALL_SIZE * Vector(0, 0.5)
HITBOX_SIZE = TILE_SIZE
HITBOX_OFFSET = WALL_SIZE * Vector(0, 0.5)

OUTLINE_TEXTURES = {
    (False, False, False, False): load_texture("assets/wall_outline/single.png", WALL_SIZE),
    (False, False, False, True): load_texture("assets/wall_outline/down end.png", WALL_SIZE),
    (False, False, True, False): load_texture("assets/wall_outline/right end.png", WALL_SIZE),
    (False, False, True, True): load_texture("assets/wall_outline/down right corner.png", WALL_SIZE),
    (False, True, False, False): load_texture("assets/wall_outline/up end.png", WALL_SIZE),
    (False, True, False, True): load_texture("assets/wall_outline/ver.png", WALL_SIZE),
    (False, True, True, False): load_texture("assets/wall_outline/up right corner.png", WALL_SIZE),
    (False, True, True, True): load_texture("assets/wall_outline/t-right.png", WALL_SIZE),
    (True, False, False, False): load_texture("assets/wall_outline/left end.png", WALL_SIZE),
    (True, False, False, True): load_texture("assets/wall_outline/down left corner.png", WALL_SIZE),
    (True, False, True, False): load_texture("assets/wall_outline/hor.png", WALL_SIZE),
    (True, False, True, True): load_texture("assets/wall_outline/t-down.png", WALL_SIZE),
    (True, True, False, False): load_texture("assets/wall_outline/up left corner.png", WALL_SIZE),
    (True, True, False, True): load_texture("assets/wall_outline/t-left.png", WALL_SIZE),
    (True, True, True, False): load_texture("assets/wall_outline/t-up.png", WALL_SIZE),
    (True, True, True, True): load_texture("assets/wall_outline/x section.png", WALL_SIZE),
}


class Wall(Building):

    def __init__(self, code, pos, parent, textures: tuple[pg.Surface, pg.Surface], hp: int, loot: tuple[str, int],
                 tool_type: str, class_id: any, punch_sound: pg.mixer.Sound = None, break_sound: pg.mixer.Sound = None):

        rpos = Vector(pos.x // TILE_SIZE.x * TILE_SIZE.x + TILE_SIZE.x / 2,
                      pos.y // TILE_SIZE.y * TILE_SIZE.y + TILE_SIZE.y / 2)
        super().__init__(code, rpos, parent, textures, hp, TEXTURE_OFFSET, loot, tool_type, class_id,
                         collider_hitbox_offset=TOUCH_HITBOX_OFFSET, collider_hitbox_size=TOUCH_HITBOX_SIZE,
                         punch_sound=punch_sound, break_sound=break_sound, hitbox_offset=HITBOX_OFFSET, hitbox_size=HITBOX_SIZE)
        self.connect_down = False
        self.connect_up = False
        self.connect_left = False
        self.connect_right = False

    def drop_items(self):

        self.parent.drop_items(self.pos, self.item[0], self.item[1])

    def select_texture(self) -> pg.Surface:

        texture = pg.Surface(WALL_SIZE.as_tuple())
        texture.blit(self.texture[int(self.connect_down)], (0, 0))
        # texture.fill("#ffffff")
        texture.blit(OUTLINE_TEXTURES[(self.connect_right, self.connect_down, self.connect_left, self.connect_up)], (0, 0))

        return texture

    def draw(self):

        super().draw()

        # pg.draw.rect(screen, "#ff0000", self.rect, 10)

        # pg.draw.circle(screen, "#ff0000", (self.pos + self.parent.offset + Vector(0, TILE_SIZE.y * 0.60)).as_tuple(), 5)
        # pg.draw.circle(screen, "#00ff00", (self.pos + self.parent.offset + Vector(0, -TILE_SIZE.y * 0.60)).as_tuple(), 5)
        # pg.draw.circle(screen, "#ff00ff", (self.pos + self.parent.offset + Vector(TILE_SIZE.x * 0.60, 0)).as_tuple(), 5)
        # pg.draw.circle(screen, "#ffff00", (self.pos + self.parent.offset + Vector(TILE_SIZE.x * -0.60, 0)).as_tuple(), 5)

    def update(self, preview_mode: bool = False):

        super().update(preview_mode)

        walls_list = list(filter(lambda e: isinstance(e, Wall) and e.code != self.code, self.parent.buildings))
        point_to_check = (self.pos + self.parent.offset + Vector(0, TILE_SIZE.y * 0.60)).as_tuple()
        self.connect_down = any(ent.hitbox.collidepoint(point_to_check) for ent in walls_list)
        point_to_check2 = (self.pos + self.parent.offset + Vector(0, -TILE_SIZE.y * 0.60)).as_tuple()
        self.connect_up = any(ent.hitbox.collidepoint(point_to_check2) for ent in walls_list)
        point_to_check3 = (self.pos + self.parent.offset + Vector(TILE_SIZE.x * 0.60, 0)).as_tuple()
        self.connect_right = any(ent.hitbox.collidepoint(point_to_check3) for ent in walls_list)
        point_to_check4 = (self.pos + self.parent.offset + Vector(TILE_SIZE.x * -0.60, 0)).as_tuple()
        self.connect_left = any(ent.hitbox.collidepoint(point_to_check4) for ent in walls_list)

        # if self.touching:
        #    print((self.connect_right, self.connect_down, self.connect_left, self.connect_up))
        #    pprint.pprint([ent.hitbox.collidepoint(point_to_check2) for ent in walls_list])

    def __repr__(self):

        return f"Wall at {Vector(self.pos.x // TILE_SIZE.x, self.pos.y // TILE_SIZE.y)}"
