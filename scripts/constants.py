from PgHelp import *
import random
import math
import os
import logging
from scripts.Classes.Font import Font
from scripts.Classes.MoleculeRenderer import MoleculeRenderer
from functools import cache

logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w",
                    format="[%(asctime)s] [%(name)s/%(filename)s/%(levelname)s]: %(message)s")

APPDATA_PATH = os.getenv('LOCALAPPDATA')
APPDATA_FOLDER = "TheFactoryMustGrow"
APPDATA_FOLDER_PATH = os.path.join(APPDATA_PATH, APPDATA_FOLDER)
SAVES_FOLDER = "saves"
SCREENSHOT_FOLDER = "screenshots"
PROGRAMS_FOLDER = "programs"

pg.init()

display_info = pg.display.Info()

# RESOLUTION = pg.Vector(800, 600)
RESOLUTION = Vector(1600, 1200)  # 1600 1200
WINDOW_SIZE = Vector(display_info.current_w, display_info.current_h)
FPS = 60
GAME_VERSION = "V0.8p10"

screen = pg.Surface(RESOLUTION.as_tuple())
actual_screen = pg.display.set_mode(WINDOW_SIZE.as_tuple(), pg.FULLSCREEN | pg.DOUBLEBUF | pg.SCALED)

MAPUI_TILE_SIZE = 4
MAP_SIZE = Vector(8, 8)
CHUNK_SIZE = Vector(32, 32)
TILE_SIZE = Vector(64, 64)  # 64 64 / 96 96
PARTICLE_SIZE = TILE_SIZE / Vector(8, 8)
ACHIEVENT_SIZE = TILE_SIZE * Vector(0.75, 0.75)

CAMERA_BOX_SIZE = RESOLUTION / Vector(3, 3)

items: dict = dict()
liquids: dict = dict()

HUGE_FONT = Font("assets/Extended Pixeltype.ttf", 162)  # 160
HUGEISH_FONT = Font("assets/Extended Pixeltype.ttf", 126)  # 100
BIG_FONT = Font("assets/Extended Pixeltype.ttf", 90)
FONT = Font("assets/Extended Pixeltype.ttf", 54)  # 56
SMALL_FONT = Font("assets/Extended Pixeltype.ttf", 35)  # 36
TINY_FONT = Font("assets/Extended Pixeltype.ttf", 26)

MOLECULE_RENDERER = MoleculeRenderer()

LOGO_FONT = pg.font.Font("assets/upheavtt.ttf", 100)

PLAYER_SIZE = Vector(1, 1)
PLAYER_SPEED = TILE_SIZE.x / 16
MAX_PLAYER_HEALTH = 100
MAX_PLAYER_HUNGER = 100

UI_PADDING = 10

INVENTORY_SIZE = 10
# INVENTORY_SCREEN_SIZE = Vector(64, 64)
INVENTORY_SCREEN_SIZE = Vector(128, 128)
INVENTORY_POS = Vector(RESOLUTION.x / 2 - INVENTORY_SCREEN_SIZE.x * INVENTORY_SIZE / 2, RESOLUTION.y - INVENTORY_SCREEN_SIZE.y - UI_PADDING)

BAR_BORDER_WIDTH = 10

HEALTH_SIZE = Vector(MAX_PLAYER_HEALTH * 4 + BAR_BORDER_WIDTH * 2, 70)
HEALTH_POS = INVENTORY_POS + Vector(UI_PADDING, -(HEALTH_SIZE.y + UI_PADDING * 2))

HUNGER_SIZE = Vector(MAX_PLAYER_HEALTH * 4 + BAR_BORDER_WIDTH * 2, 70)
HUNGER_POS = INVENTORY_POS + Vector(INVENTORY_SCREEN_SIZE.x * INVENTORY_SIZE, 0) + Vector(-(UI_PADDING + HUNGER_SIZE.x), -(HUNGER_SIZE.y + UI_PADDING * 2))

TREE_SIZE = Vector(TILE_SIZE.x, TILE_SIZE.y * 2)
WALL_SIZE = TILE_SIZE * Vector(1, 2)

DEPOSIT_SIZE = TILE_SIZE * Vector(3, 3)
VEIN_SIZE = TILE_SIZE * Vector(1.5, 1.5)

SELECT_DOWN_LEFT = load_texture("assets/select_down_left.png", TILE_SIZE)
SELECT_DOWN_RIGHT = load_texture("assets/select_down_right.png", TILE_SIZE)
SELECT_UP_LEFT = load_texture("assets/select_up_left.png", TILE_SIZE)
SELECT_UP_RIGHT = load_texture("assets/select_up_right.png", TILE_SIZE)

CURSOR_TEXTURE = load_texture("assets/cursor.png", Vector(64, 64))

screen_height = display_info.current_h
screen_width = display_info.current_h * 4 / 3
screen_x = display_info.current_w / 2 - screen_width / 2

ENTITIES = []
ENTITY_UI = []
SCENES = []
MODULES = []
SUBMENUS = []

# PARTICLES = {f.split('.')[0]: load_texture("assets/particles/" + f, PARTICLE_SIZE) for f in os.listdir("assets/particles")}

biome_to_name: dict[int, str] = {
    0: "plains",
    1: "forest",
    2: "ocean",
    3: "rocks",
    4: "desert",
    5: "beach",
    6: "void",
}
UNCHANGEABLE_TILES = [4, 5]

FOOTSTEP_SOUNDS = [
    pg.mixer.Sound("sound/footstep_1.wav"),
    pg.mixer.Sound("sound/footstep_2.wav"),
    pg.mixer.Sound("sound/footstep_3.wav"),
    pg.mixer.Sound("sound/footstep_4.wav"),
    pg.mixer.Sound("sound/footstep_5.wav"),
    pg.mixer.Sound("sound/footstep_6.wav"),
    pg.mixer.Sound("sound/footstep_7.wav"),
    pg.mixer.Sound("sound/footstep_8.wav"),
]
PLACING_SOUND = pg.mixer.Sound("sound/placing.wav")
SCREENSHOT_SOUND = pg.mixer.Sound("sound/screenshot.wav")
CHAINSAW_SOUND = pg.mixer.Sound("sound/chainsaw.wav")
DRILL_SOUND = pg.mixer.Sound("sound/crusher.mp3")
EATING_SOUND = pg.mixer.Sound("sound/eating.wav")
MUSIC_LIST = [os.path.join("sound/music", file_name) for file_name in os.listdir("sound/music")]
random.shuffle(MUSIC_LIST)
MUSIC_VOLUME = 0  # 20 #############################################################


def draw_brackets(screen: pg.Surface, rect: pg.Rect):

    screen.blit(SELECT_UP_LEFT, (rect.x, rect.y))
    screen.blit(SELECT_UP_RIGHT, (rect.x+rect.width-TILE_SIZE.x, rect.y))
    screen.blit(SELECT_DOWN_LEFT, (rect.x, rect.y+rect.height-TILE_SIZE.y))
    screen.blit(SELECT_DOWN_RIGHT, (rect.x+rect.width-TILE_SIZE.x, rect.y+rect.height-TILE_SIZE.y))


def percent(integer: int, percnt: int) -> float:

    return integer / 100 * percnt


def distance(a: Vector, b: Vector) -> float:

    return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)


def get_average(n: list[float | int]):
    return sum(n) / len(n)


def get_mouse_pos():

    mp = Vector(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
    mp.y = (mp.y / (screen_height / 1000)) * (RESOLUTION.y / 1000)
    mp.x = (mp.x / (screen_width / 1000)) * (RESOLUTION.x / 1000)
    if mp.x > RESOLUTION.x: mp.x = RESOLUTION.x
    return mp.as_tuple()


def from_iterable(i: tuple[int|float, int|float]) -> Vector:

    return Vector(i[0], i[1])


def find_closest_color(target_color, color_list) :
    closest_color = color_list[0]
    min_distance = float('inf')

    for color in color_list :
        distance = math.sqrt(
            (target_color[0] - color[0]) ** 2 +
            (target_color[1] - color[1]) ** 2 +
            (target_color[2] - color[2]) ** 2
        )
        if distance < min_distance :
            min_distance = distance
            closest_color = color

    return closest_color


def change_texture_palette(texture, new_palette) :
    new_texture = texture.copy()
    new_texture.lock()

    width, height = new_texture.get_size()
    for x in range(width) :
        for y in range(height) :
            current_color = new_texture.get_at((x, y))
            closest_color = find_closest_color(current_color, new_palette)
            new_texture.set_at((x, y), closest_color)

    new_texture.unlock()

    return new_texture


def replace_color(surface: pg.Surface, old_color: tuple, new_color: tuple) -> pg.Surface:
    surface = surface.copy()
    surface.lock()
    old_color = pg.Color(*old_color)
    new_color = pg.Color(*new_color)
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            if surface.get_at((x, y)) == old_color:
                surface.set_at((x, y), new_color)
    surface.unlock()
    return surface


def draw_wire(screen_pos_a: Vector, screen_pos_b: Vector):

    sag_amount = 70
    num_points = 30
    thickness = 2

    mid_x = (screen_pos_a.x + screen_pos_b.x) / 2
    mid_y = (screen_pos_a.y + screen_pos_b.y) / 2 + sag_amount

    start = screen_pos_a.as_tuple()
    control = (mid_x, mid_y)
    end = screen_pos_b.as_tuple()

    bezier_points = []
    for t in range(num_points + 1):
        t /= num_points
        x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t ** 2 * end[0]
        y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t ** 2 * end[1]
        bezier_points.append((x, y))

    thick_points_top = []
    thick_points_bottom = []
    for i in range(len(bezier_points) - 1):
        x1, y1 = bezier_points[i]
        x2, y2 = bezier_points[i + 1]
        dx, dy = x2 - x1, y2 - y1
        length = (dx ** 2 + dy ** 2) ** 0.5
        nx, ny = -dy / length, dx / length

        thick_points_top.append((x1 + nx * thickness / 2, y1 + ny * thickness / 2))
        thick_points_bottom.append((x1 - nx * thickness / 2, y1 - ny * thickness / 2))

    x1, y1 = bezier_points[-2]
    x2, y2 = bezier_points[-1]
    dx, dy = x2 - x1, y2 - y1
    length = (dx ** 2 + dy ** 2) ** 0.5
    nx, ny = -dy / length, dx / length

    thick_points_top.append((x2 + nx * thickness / 2, y2 + ny * thickness / 2))
    thick_points_bottom.append((x2 - nx * thickness / 2, y2 - ny * thickness / 2))

    thick_points = thick_points_top + thick_points_bottom[::-1]

    pg.draw.polygon(screen, "#000000", thick_points)


def hex_to_rgba(hex_color: str) -> tuple[int, int, int, int]:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 6:
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        a = 255
    elif len(hex_color) == 8:
        r, g, b, a = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4, 6))
    else:
        raise ValueError("Invalid hex color format. Use #rrggbb or #rrggbbaa.")

    return r, g, b, a


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def calculate_average_color(surface: pg.Surface, require_alpha: bool = True) -> \
        tuple[int, int, int, int] | tuple[int, int, int]:

    pixel_array = pg.surfarray.pixels_alpha(surface)
    rgba_array = pg.surfarray.pixels3d(surface)

    r_sum = rgba_array[:, :, 0].sum()
    g_sum = rgba_array[:, :, 1].sum()
    b_sum = rgba_array[:, :, 2].sum()
    a_sum = pixel_array.sum()

    num_pixels = surface.get_width() * surface.get_height()

    avg_r = r_sum // num_pixels
    avg_g = g_sum // num_pixels
    avg_b = b_sum // num_pixels
    avg_a = a_sum // num_pixels

    if require_alpha:
        return avg_r, avg_g, avg_b, avg_a
    else:
        return avg_r, avg_g, avg_b
