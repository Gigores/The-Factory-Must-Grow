import logging

from faker import Faker
from datetime import *
from numpy import zeros
from random import randint
from math import sin, cos
import importlib

from scripts.Managers.GameAssets import *
from scripts.UI.MainMenuScreen import MainMenu
from scripts.Managers.IngameManagers.GameMap import Map
from scripts.Managers.IngameManagers.Inventory import Inventory
from scripts.Managers.IngameManagers.AchievementsVisualsManager import AchievementsVisualsManager
from scripts.Generators.WorldGenerator import WorldGenerator
from scripts.Managers.EntityManager import EntityManager
from scripts.Managers.SavesManager import SavesManager
from scripts.Managers.SettingsManager import SettingsManager
from scripts.Classes.ItemClasses import *

from scripts.Entities.Player import Player
from scripts.Entities.ItemEntity import ItemEntity

import scripts.Scenes.MainMenuScene
import scripts.Scenes.GameScene

pg.init()
pg.mixer.init(frequency=44100, size=16, channels=1000, buffer=512)


pallete = [
    (0, 0, 0, 0),
    (0, 32, 0, 255),
    (0, 64, 0, 255),
    (0, 96, 0, 255),
    (0, 128, 0, 255),
    (0, 160, 0, 255),
    (0, 192, 0, 255),
    (0, 224, 0, 255),
    (0, 255, 0, 255),
]


# aplle ][
pallete_a = [
    (0, 0, 0, 0),
    (81, 92, 22, 255),
    (132, 61, 82, 255),
    (234, 125, 39, 255),
    (81, 72, 136, 255),
    (232, 93, 239, 255),
    (245, 183, 201, 255),
    (0, 103, 82, 255),
    (0, 200, 44, 255),
    (145, 145, 145, 255),
    (201, 209, 153, 255),
    (0, 166, 240, 255),
    (152, 219, 201, 255),
    (200, 193, 247, 255),
    (255, 255, 255, 255)
]

# commodore 64
pallete_c = [
    (0, 0, 0, 0),
    (98, 98, 98, 255),
    (137, 137, 137, 255),
    (173, 173, 173, 255),
    (255, 255, 255, 255),
    (159, 78, 68, 255),
    (203, 126, 117, 255),
    (109, 84, 18, 255),
    (161, 104, 60, 255),
    (201, 212, 135, 255),
    (154, 226, 155, 255),
    (92, 171, 94, 255),
    (106, 191, 198, 255),
    (136, 126, 203, 255),
    (80, 69, 155, 255),
    (160, 87, 163, 255)
]


class Game:

    def __init__(self):

        self.faker = Faker()
        self.screen = screen
        self.clock = pg.time.Clock()
        self.entity_manager = EntityManager(self)
        self.saves_manager = SavesManager(self)
        self.achievements_visuals_manager = AchievementsVisualsManager(self)
        self.settings_manager = SettingsManager(self)

        self.running = True

        self.offset = Vector(0, 0)

        self.go_up = False
        self.go_left = False
        self.go_down = False
        self.go_right = False

        self.trees = []
        self.ores = []
        self.buildings = []
        self.pebbles = []
        self.bushes = []
        self.items = []
        self.particles = []
        self.wires = []

        self.entities = []
        self.forced_entities = []
        self.entities_to_draw = []
        self.entities_by_chunks = [[[] for _ in range(MAP_SIZE.y)] for _ in range(MAP_SIZE.x)]
        self.subnetworks = []

        self.world = Map(self)
        self.biome_map = zeros((MAP_SIZE * CHUNK_SIZE).as_tuple(), dtype="uint8")
        self.inventory = Inventory(self)
        self.backpack = Inventory(self, INVENTORY_SIZE * 2)
        self.player = Player(self)
        self.world_generator = WorldGenerator(self)

        self.animation_counter = 0

        self.DARKNESS = pg.Surface(RESOLUTION.as_tuple())
        self.DARKNESS.fill("#000000")
        self.DARKNESS.set_alpha(200)

        self.birds = pg.mixer.Sound("sound/birdies.mp3")
        self.birds.set_volume(0.5)

        self.shift_pressed = False
        self.alt_pressed = False
        self.ctrl_pressed = False
        self.show_secret_data = False
        self.show_ui = True

        # self.UIs = [WorkbenchUI(self), FurnaceUI(self), WoodenChestUI(self), IronChestUI(self),
        #             ESCMenu(self), AnvilUI(self), CrusherUI(self), BlastFurnaceUI(self),
        #             MagneticCentrifugeUI(self), AchivemenMenu(self), WoodworkingMachineUI(self),
        #             TableUI(self), BedsideTableUI(self), ContainerUI(self), BigContainerUI(self),
        #             TerminalWindow(self)]
        self.UIs = {ui.__name__: ui(self) for ui in ENTITY_UI}
        self.str_to_entity = {en.__name__: en for en in ENTITIES}
        self.main_menu = MainMenu(self)
        self.active_object_ui = None
        self.active_ui_id = None

        self.world_center = MAP_SIZE * CHUNK_SIZE * TILE_SIZE / Vector(2, 2)

        self.current_scene = "MainMenuScene"
        self.scenes = {sc.__name__: sc(self) for sc in SCENES}

        self.current_save_name = ""

        self.all_got_items = []
        self.all_placed_buildings = []
        self.unlocked_achievements = []

    def loading(self):

        self.settings_manager.load_settings()

        def find_py_files(directory):
            py_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        dir_path = os.path.dirname(file_path).replace(os.sep, ".")
                        dir_path = dir_path.replace("..", ".")
                        py_files.append(f"{dir_path}.{file.split('.')[0]}")
            return py_files

        directory_paths = ["scripts\\Entities", "scripts\\UI"]

        for path in directory_paths:
            for file_name in find_py_files(path):
                logging.info(f"loading file {file_name}")
                importlib.import_module(file_name)

        self.UIs = {ui.__name__: ui(self) for ui in ENTITY_UI}
        self.str_to_entity = {en.__name__: en for en in ENTITIES}

        # import scripts.Entities.Natural.SmallCactus
        # import scripts.Entities.Natural.Vein
        # import scripts.Entities.Natural.Tree
        # import scripts.Entities.Natural.Bush
        # import scripts.Entities.Natural.Cactus
        # import scripts.Entities.Natural.Deposit
        # import scripts.Entities.Natural.Fungus
        # import scripts.Entities.Natural.Pebble

        # import scripts.Entities.Buildings.Crops.CarrotCrop
        # import scripts.Entities.Buildings.Crops.TomatoCrop
        # import scripts.Entities.Buildings.Crops.WheatCrop
        # import scripts.Entities.Buildings.Saplings.TreeSapling
        # import scripts.Entities.Buildings.Saplings.CactusSapling
        # import scripts.Entities.Buildings.Saplings.MushroomSapling
        # import scripts.Entities.Buildings.Furniture.Bed
        # import scripts.Entities.Buildings.Furniture.Stool
        # import scripts.Entities.Buildings.Furniture.Table
        # import scripts.Entities.Buildings.Furniture.BedsideTable
        # import scripts.Entities.Buildings.Furniture.PotWithPlant

    def generate_id(self) -> int:

        return self.faker.unique.random_int(min=0, max=4294967295)

    def drop_items(self, pos: Vector, item_name: str, item_amount: int, vel: Vector = Vector(0, 0),
                   animation_time: int = 0):

        if item_amount == 1:
            self.items.append(ItemEntity(self.generate_id(), pos, self, item_name, vel, animation_time))
        else:
            factor = int(item_amount * percent(TILE_SIZE.x, 5))
            for i in range(item_amount):
                item_pos = pos + Vector(randint(-factor, factor), randint(-factor, factor))
                self.items.append(ItemEntity(self.generate_id(), item_pos, self, item_name))

        self.entity_manager.update_entities_by_chunks()
        self.entity_manager.update_active_chunks()

    def update_achievements(self):

        all_placed_buildings_set = set(self.all_placed_buildings)
        all_got_items_set = set(self.all_got_items)

        for achievement_id, achievement in enumerate(achievements):

            req_type, req_target = achievement.req

            if achievement_id in self.unlocked_achievements or not req_target:
                continue

            do_unlock = False

            if req_type == "place":
                do_unlock = req_target in all_placed_buildings_set
            if req_type == "placeo":
                do_unlock = any(building in all_placed_buildings_set for building in req_target)
            elif req_type == "get":
                do_unlock = req_target in all_got_items_set
            elif req_type == "geto":
                do_unlock = any(item in all_got_items_set for item in req_target)
            elif req_type == "geta":
                do_unlock = all(item in all_got_items_set for item in req_target)

            if do_unlock:
                self.unlocked_achievements.append(achievement_id)
                self.achievements_visuals_manager.queue.append(achievement_id)

    def save_and_quit_to_title(self):

        # self.save()
        self.active_ui_id = None
        self.active_object_ui = None
        self.birds.stop()
        self.current_scene = "MainMenuScene"
        self.main_menu.submenu_id = 0

    def set_game_scene(self, id):

        self.current_scene = id

    def new_game(self, file_name, seed: int, island_type: int):

        def new_game_setup(file_name, seed, island_type):
            try:
                self.saves_manager.new_game(file_name, seed, island_type)
                self.set_game_scene("GameScene")
                self.entity_manager.update_active_chunks()
            except Exception as e:
                self.set_game_scene("MainMenuScene")
                logging.exception("Error Accured!")
                self.main_menu.submenu_id = 7

        self.main_menu.loading_menu("Generating", new_game_setup, (file_name, seed, island_type))

    def spawn(self, class_name, pos):

        unique_id = self.faker.unique.random_int(min=0, max=4294967295)
        self.buildings.append(self.str_to_entity[class_name](unique_id, pos, self))

    def run(self):

        pg.display.set_caption("TheFactoryMustGrow")

        pg.mouse.set_visible(False)

        if not os.path.exists(APPDATA_FOLDER_PATH):
            os.mkdir(APPDATA_FOLDER_PATH)

        if not os.path.exists(os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER)):
            os.mkdir(os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER))

        if not os.path.exists(os.path.join(APPDATA_FOLDER_PATH, SCREENSHOT_FOLDER)):
            os.mkdir(os.path.join(APPDATA_FOLDER_PATH, SCREENSHOT_FOLDER))

        if not os.path.exists(os.path.join(APPDATA_FOLDER_PATH, PROGRAMS_FOLDER)):
            os.mkdir(os.path.join(APPDATA_FOLDER_PATH, PROGRAMS_FOLDER))

        music_id = 0

        def loading():
            try:
                self.loading()
                self.main_menu.submenu_id = 0
            except Exception as e:
                self.set_game_scene("MainMenuScene")
                logging.exception("Error Accured!")
                self.main_menu.submenu_id = 7

        self.main_menu.loading_menu("Loading...", loading, ())

        while self.running:

            # screen.fill("#000000")
            self.animation_counter += 1

            try:

                self.scenes[self.current_scene].handle_events(pg.event.get())
                self.scenes[self.current_scene].update()
                self.scenes[self.current_scene].draw()

            except Exception as e:

                logging.exception("Error: ")

                self.saves_manager.save()
                self.set_game_scene("MainMenuScene")
                self.main_menu.get_submenu("error").exception = e
                self.main_menu.submenu_id = 7

            if not pg.mixer.music.get_busy():
                song = MUSIC_LIST[music_id]
                music_id += 1
                if music_id >= len(MUSIC_LIST):
                    music_id = 0
                pg.mixer.music.load(song)
                pg.mixer.music.set_volume(MUSIC_VOLUME / 100)
                pg.mixer.music.play(fade_ms=1000)

            cursor_texture = pg.transform.scale(CURSOR_TEXTURE, (sin(self.animation_counter / 20) * 10 + CURSOR_TEXTURE.get_width(), sin(self.animation_counter / 20) * 10 + CURSOR_TEXTURE.get_height()))

            screen.blit(cursor_texture, get_mouse_pos())
            actual_screen.blit(pg.transform.scale(screen, (screen_width, screen_height)), (screen_x, 0))

            pg.display.update()
            self.clock.tick(FPS)
            #self.clock.tick()


if __name__ == '__main__':
    Game().run()
