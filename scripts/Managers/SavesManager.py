import logging
import os.path
import json

from scripts.Entities.Player import Player
from scripts.Entities.Buildings.IronChest import IronChest
from scripts.Managers.IngameManagers.AchievementsVisualsManager import AchievementsVisualsManager
from scripts.Managers.IngameManagers.Inventory import Inventory
from copy import deepcopy
from pickle import dump, load
from shutil import rmtree
from scripts.Managers.GameAssets import *


class SavesManager:

    def __init__(self, parent):

        self.parent = parent

        self.init_thread = None
        self.starting_items = starting_items

    def reset_game_state(self):

        self.parent.trees = []
        self.parent.ores = []
        self.parent.buildings = []
        self.parent.pebbles = []
        self.parent.bushes = []
        self.parent.wires = []
        self.parent.items = []
        self.parent.particles = []
        self.parent.all_got_items = []
        self.parent.all_placed_buildings = []
        self.parent.unlocked_achievements = []
        self.parent.achievements_visuals_manager = AchievementsVisualsManager(self.parent)
        self.parent.inventory = Inventory(self.parent, main=True)
        self.parent.backpack = Inventory(self, INVENTORY_SIZE * 2)
        self.parent.player = Player(self.parent)

        for ui in self.parent.UIs.values():
            ui.mouse_slot = [None, 0]

    def new_game(self, file_name, seed: int, island_type: int):

        self.reset_game_state()
        self.init_game(file_name, island_type, seed)

    def update_game_state(self):

        self.parent.entity_manager.update_entities_by_chunks()
        self.parent.world.update_chunks()
        self.parent.offset = Vector(-1, -1) * self.parent.player.pos + RESOLUTION / Vector(2, 2) - TILE_SIZE * Vector(
            1.5, 1.5) / Vector(2, 2)
        # self.parent.birds.play(-1, fade_ms=1000)

    def new_polygon_game(self, file_name: str):

        self.parent.current_save_name = file_name
        self.parent.world_generator.generate_flat()

        pos = deepcopy(self.parent.player.pos) + Vector(0, -(TILE_SIZE.y * 2))
        chest = IronChest(self.parent.generate_id(), Vector(0, 0), self.parent)
        for item in items:
            dasdsa = items[item]
            if dasdsa and chest.inventory.can_fit(item, dasdsa.stack_size):
                chest.inventory.append(item, dasdsa.stack_size)
            else:
                chest.pos = deepcopy(pos)
                self.parent.buildings.append(chest)
                pos.x += TILE_SIZE.x
                chest = IronChest(self.parent.generate_id(), Vector(0, 0), self.parent)
                chest.inventory.append(item, dasdsa.stack_size)
        chest.pos = deepcopy(pos)
        self.parent.buildings.append(chest)

        self.update_game_state()

    def init_game(self, file_name: str, island_type, seed):

        self.parent.current_save_name = file_name
        self.parent.world_generator.generate_world(seed, island_type)

        logging.debug(self.starting_items)
        #for item, item_amount in self.starting_items:

        #    self.parent.backpack.append(item, item_amount)

        self.update_game_state()

    def load_game(self, file_name):

        self.parent.main_menu.submenu_id = 6
        self.parent.main_menu.message = "Loading"
        self.parent.main_menu.draw()
        actual_screen.blit(pg.transform.scale(screen, (screen_width, screen_height)), (screen_x, 0))
        pg.display.update()

        self.parent.trees = []
        self.parent.ores = []
        self.parent.buildings = []
        self.parent.pebbles = []
        self.parent.bushes = []
        self.parent.items = []
        self.parent.wires = []
        self.parent.inventory = Inventory(self.parent)
        self.parent.backpack = Inventory(self, INVENTORY_SIZE * 2)

        for ui in self.parent.UIs.values():
            ui.mouse_slot = [None, 0]

        self.load(file_name)
        self.parent.current_save_name = file_name

        self.parent.entity_manager.update_entities_by_chunks()
        self.parent.world.update_chunks()
        self.parent.offset = Vector(-1, -1) * self.parent.player.pos + RESOLUTION / Vector(2, 2) - TILE_SIZE * Vector(1.5, 1.5) / Vector(2, 2)
        # self.parent.birds.play(-1, fade_ms=1000)
        self.parent.achievements_visuals_manager.reset()

    def dumb_entities(self, entities_list: list, target_list: list):

        for entity in entities_list:
            try:
                target_list.append(entity.dumb())
                json.dumps(target_list[-1])
            except:
                print(f"cannot dumb entity '{entity.__repr__()}'")

    def load_entities(self, entities_datas_list: list, target_entity_list: list):

        for entity_data in entities_datas_list:
            try:
                # if isinstance(entity_class, type): _class = entity_class
                # elif isinstance(entity_class, list): _class = entity_class[entity_data["class"]]
                _class = self.parent.str_to_entity[entity_data["class"]]
                target_entity_list.append(_class(self.parent.generate_id(), Vector(0, 0), self.parent))
                target_entity_list[-1].load(entity_data)
            except Exception as e:
                logging.exception(f"cannot load entity class '{entity_data}' because")

    def load_entities_from_file(self, file_path):

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                target = []
                self.load_entities(load(f), target)
                return target
        else:
            logging.warning(f"Couldn't load {file_path} because file '{file_path}' not found")
            return []

    def save(self, file_name=None):

        save_folder_path = os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER, file_name if file_name else self.parent.current_save_name)
        entities_folder_path = os.path.join(save_folder_path, "entities")

        if os.path.exists(save_folder_path):
            rmtree(save_folder_path)

        os.mkdir(save_folder_path)
        os.mkdir(entities_folder_path)

        with open(os.path.join(save_folder_path, "world.pkl"), "wb") as f:
            dump(self.parent.world.dumb(), f)
        with open(os.path.join(save_folder_path, "inventory.pkl"), "wb") as f:
            dump(self.parent.inventory.dumb(), f)
        with open(os.path.join(save_folder_path, "backpack.pkl"), "wb") as f:
            dump(self.parent.backpack.dumb(), f)
        with open(os.path.join(save_folder_path, "player.pkl"), "wb") as f:
            dump(self.parent.player.dumb(), f)
        with open(os.path.join(save_folder_path, "achievements.pkl"), "wb") as f:
            dump((self.parent.unlocked_achievements, self.parent.all_got_items, self.parent.all_placed_buildings), f)

        with open(os.path.join(entities_folder_path, "trees.pkl"), "wb") as f:
            data = []
            self.dumb_entities(self.parent.trees, data)
            dump(data, f)
        with open(os.path.join(entities_folder_path, "ores.pkl"), "wb") as f:
            data = []
            self.dumb_entities(self.parent.ores, data)
            dump(data, f)
        with open(os.path.join(entities_folder_path, "buildings.pkl"), "wb") as f:
            data = []
            self.dumb_entities(self.parent.buildings, data)
            dump(data, f)
        with open(os.path.join(entities_folder_path, "pebbles.pkl"), "wb") as f:
            data = []
            self.dumb_entities(self.parent.pebbles, data)
            dump(data, f)
        with open(os.path.join(entities_folder_path, "bushes.pkl"), "wb") as f:
            data = []
            self.dumb_entities(self.parent.bushes, data)
            dump(data, f)
        with open(os.path.join(entities_folder_path, "items.pkl"), "wb") as f:
            data = []
            self.dumb_entities(self.parent.items, data)
            dump(data, f)
        with open(os.path.join(entities_folder_path, "wires.pkl"), "wb") as f:
            data = []
            self.dumb_entities(self.parent.wires, data)
            dump(data, f)

        pg.image.save(self.parent.scenes["GameScene"].take_thumbnail(), os.path.join(save_folder_path, "screenshot.png"))

#         file_data = {
#             "trees": [],
#             "ores": [],
#             "buildings": [],
#             "pebbles": [],
#             "bushes": [],
#             "items": [],
#             "unlocked_achievements": self.parent.unlocked_achievements,
#             "player": self.parent.player.dumb(),
#             "map": self.parent.world.dumb(),
#             "player_inventory": self.parent.inventory.dumb()
#         }
#         self.dumb_entities(self.parent.trees, file_data["trees"])
#         self.dumb_entities(self.parent.ores, file_data["ores"])
#         self.dumb_entities(self.parent.buildings, file_data["buildings"])
#         self.dumb_entities(self.parent.pebbles, file_data["pebbles"])
#         self.dumb_entities(self.parent.bushes, file_data["bushes"])
#         self.dumb_entities(self.parent.items, file_data["items"])

        # json.dumps(file_data["trees"])
        # json.dumps(file_data["ores"])
        # json.dumps(file_data["buildings"])
        # json.dumps(file_data["pebbles"])
        # json.dumps(file_data["bushes"])
        # json.dumps(file_data["items"])
        # json.dumps(file_data["player"])
        # json.dumps(file_data["map"])
        # json.dumps(file_data["player_inventory"])

        # pprint.pprint(file_data)

#         try:
#             with open(f"saves/{self.parent.current_save_name}.json", "w+") as f:
#                 f.write(json.dumps(file_data))
#         except Exception as e:
#             print(e)
#             with open(f"save_log.txt", "w+") as f:
#                 pprint.pprint(file_data, stream=f)

    def load(self, file_name):

        entities_folder = os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER, file_name, "entities")

        with open(os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER, file_name, "world.pkl"), "rb") as f:
            self.parent.world.load(load(f))
        with open(os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER, file_name, "player.pkl"), "rb") as f:
            self.parent.player.load(load(f))
        with open(os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER, file_name, "inventory.pkl"), "rb") as f:
            self.parent.inventory.load(load(f))
        if os.path.exists(os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER, file_name, "backpack.pkl")):
            with open(os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER, file_name, "backpack.pkl"), "rb") as f:
                self.parent.backpack.load(load(f))
        with open(os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER, file_name, "achievements.pkl"), "rb") as f:
            self.parent.unlocked_achievements, self.parent.all_got_items, self.parent.all_placed_buildings = load(f)

        self.parent.trees = self.load_entities_from_file(os.path.join(entities_folder, "trees.pkl"))
        self.parent.ores = self.load_entities_from_file(os.path.join(entities_folder, "ores.pkl"))
        self.parent.buildings = self.load_entities_from_file(os.path.join(entities_folder, "buildings.pkl"))
        self.parent.pebbles = self.load_entities_from_file(os.path.join(entities_folder, "pebbles.pkl"))
        self.parent.bushes = self.load_entities_from_file(os.path.join(entities_folder, "bushes.pkl"))
        if os.path.exists(os.path.join(entities_folder, "wires.pkl")):
            self.parent.wires = self.load_entities_from_file(os.path.join(entities_folder, "wires.pkl"))
        self.parent.items = self.load_entities_from_file(os.path.join(entities_folder, "items.pkl"))

        for wire in self.parent.wires:
            wire.post_init()

#         with open(os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER, f"{file_name}.json"), "r") as f:
#             data = json.loads(f.read())

#         self.parent.player.load(data["player"])
#         self.parent.world.load(data["map"])
#         self.parent.inventory.load(data["player_inventory"])
#         self.parent.unlocked_achievements = data["unlocked_achievements"]

#         self.load_entities(data["trees"], self.parent.trees, [Tree, Cactus, SmallCactus, Fungus])
#         self.load_entities(data["ores"], self.parent.ores, [Deposit, Vein])
#         self.load_entities(data["buildings"], self.parent.buildings, [Workbench, Furnace, WoodenChest, IronChest, Anvil, Crusher, BlastFurnace, MagneticCentrifuge])
#         self.load_entities(data["pebbles"], self.parent.pebbles, Pebble)
#         self.load_entities(data["bushes"], self.parent.bushes, Bush)
#         self.load_entities(data["items"], self.parent.items, ItemEntity)
