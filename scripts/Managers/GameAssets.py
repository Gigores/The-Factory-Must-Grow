import logging
import re
from copy import deepcopy
from asteval import Interpreter

from scripts.Classes.ItemClasses import *
from scripts.Classes.Achievement import *
from scripts.Classes.Tile import Tile
from scripts.constants import *
from scripts.Classes.Recipe import *
from scripts.UI.Components.BaseUIComponents import Text
import json
import os

addons = {}

addon_constants: dict[str, any] = dict()
tiles: dict[int, Tile] = dict()
workbench_recipies = WorkbenchRecipeManager()
engineering_workbench_recipes = EngineeringWorkbenchRecipeManager()
furnace_recipies = FurnaceRecipeManager()
anvil_recipies = AnvilRecipeManager()
crusher_recipies = CrusherRecipeManager()
centrifuge_recipies = MagneticCentrifugeManager()
woodworking_machine_recipies = WoodworkingMachineRecipeManager()
coke_oven_recipies = CokeOvenRecipeManager()
foundry_recipies = FoundryRecipeManager()
chemical_reactor_recipes = ChemicalReactorRecipeManager()

ORE_TYPES = []
achievements = []
starting_items = []

FUEL_WEIGHT = {}
TILE_TO_ITEM = {}
ORE_TYPE_TO_ITEM = {}
ORE_TYPE_TO_HP = {}
TILE_TO_ORE_TYPE = {}
ORE_TYPE_TO_TILE = {}
ORE_TEXTURES = {}
ITEM_TO_ORE_TYPE = {}
PARTICLE_TEXTURES = {}
LIQUID_TO_ITEM = {}
ITEM_TO_LIQUID = {}
TILE_TO_BUCKET = {}

TEXTUTURE_NULL = pg.Surface((64, 64))
TEXTUTURE_NULL.fill("#000000")
pg.draw.rect(TEXTUTURE_NULL, "#ff00ff", (0, 0, 32, 32))
pg.draw.rect(TEXTUTURE_NULL, "#ff00ff", (32, 32, 32, 32))


class AddonLoader:

    def __init__(self):

        self.current_addon = None
        self.tag_lexer = Text.Lexer("teho is gay")

    def evaluate_math_expression(self, expression: str) -> int:

        asteval = Interpreter()
        values = addon_constants[self.current_addon]

        def replacer(match_):
            var_name = match_.group(0)
            if var_name in values:
                return str(values[var_name])
            raise ValueError(f"Constant '{var_name}' does not exist.")

        pattern = r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'
        return asteval(re.sub(pattern, replacer, expression))

    def load_constants(self, file):

        global addon_constants

        data = json.load(file)
        addon_constants[self.current_addon] = data

    def load_file(self, function, path):

        file_name = path.split("/")[-1]
        logging.info(f"loading {file_name}")
        try:
            main_file = open(f"addons/{self.current_addon}/data/{path}", "r", encoding="utf-8")
            try:
                overrides = []
                for overriden_addon_name in os.listdir(f"addons/{self.current_addon}/overrides"):
                    try:
                        overrides.append(open(f"addons/{self.current_addon}/overrides/{overriden_addon_name}/{path}", "r", encoding="utf-8"))
                    except Exception as e:
                        print(e)
                        continue
            except Exception as e:
                print(e)
                overrides = []

            print(overrides)
            function(main_file, overrides)

            main_file.close()
            for file in overrides: file.close()
            logging.info(f"Success")
        except:
            logging.exception("Error:")

    @staticmethod
    def load_starting_items(file):

        global starting_items
        starting_items += json.load(file)["items"]

    def load_tiles(self, file):

        global tiles

        for tile_id, tile_data in json.load(file).items():
            if not ("texture_path" in tile_data):
                tile_data["texture_path"] = f"addons/{self.current_addon}/assets/tiles/{tile_data['name']}.png"
            tiles[int(tile_id)] = Tile(**tile_data)
            logging.info(f"tile loaded: '{tile_id}'")

    def load_items(self, file):

        global items

        data = json.load(file)
        for class_name, items_list in data.items():
            if class_name in globals() and isinstance(globals()[class_name], type):
                class_ = globals()[class_name]
                for item_name, item_data in items_list.items():
                    if not ("texture_path" in item_data):
                        item_data["texture_path"] = f"addons/{self.current_addon}/assets/items/{item_name}.png"
                    self.tag_lexer.text = addons[self.current_addon]['name']
                    tokens = self.tag_lexer.tokenize()
                    new_item_name = f"{self.current_addon}/{item_name}"
                    tooltip_text_to_add = f"<col hex='666666'>{new_item_name}<nl>"
                    if "tags" in item_data and len(item_data["tags"]) > 0:
                        tags_text = ""
                        for i, tag in enumerate(item_data["tags"]):
                            tags_text += tag
                            if i != len(item_data["tags"]) - 1:
                                tags_text += ", "
                        tooltip_text_to_add += f"<col hex='666666'>tags: {tags_text}<nl>"
                    if item_name in FUEL_WEIGHT:
                        tooltip_text_to_add = f"<item name='core/emoji_flame'> <col hex='FF9999'>Burnable <col hex='777777'>(<col hex='FF9999'>{FUEL_WEIGHT[item_name] * (1 / 20):.10g}s<col hex='777777'>)<col hex='FF9999'><nl>" + tooltip_text_to_add
                    if class_name == "PlaceableTile":
                        tooltip_text_to_add = f"<item name='core/emoji_placeable'> <col hex='CFE9EC'>Placeable Tile<nl>" + tooltip_text_to_add
                    if class_name == "BuildingItem":
                        tooltip_text_to_add = f"<item name='core/emoji_placeable2'> <col hex='CFE9EC'>Placeable Building<nl>" + tooltip_text_to_add
                    tooltip_text_to_add += f"<col hex='5555FF'>{self.tag_lexer.get_raw_text(tokens)}"
                    if (not ("tooltip" in item_data)) or len(item_data["tooltip"]) == 0:
                        item_data["tooltip"] = tooltip_text_to_add
                    else:
                        item_data["tooltip"] += f"<nl>{tooltip_text_to_add}"
                    item_data["stack_size"] = self.evaluate_math_expression(str(item_data["stack_size"]))
                    if class_name == "Tool":
                        item_data["damage"] = self.evaluate_math_expression(str(item_data["damage"]))
                    if class_name == "Food":
                        item_data["saturation_level"] = self.evaluate_math_expression(
                            str(item_data["saturation_level"]))
                    items[new_item_name] = class_(**item_data)
                    logging.info(f"item loaded: '{new_item_name}'")

    def load_liquids(self, file):

        global liquids
        global LIQUID_TO_ITEM
        global ITEM_TO_LIQUID

        data = json.load(file)

        for liquid_name, liquid_data in data.items():
            bucket_item = liquid_data["bucket"]
            new_liquid_name = f"{self.current_addon}/{liquid_name}"

            LIQUID_TO_ITEM[new_liquid_name] = bucket_item
            ITEM_TO_LIQUID[bucket_item] = new_liquid_name
            liquids[new_liquid_name] = liquid_data

            logging.info(f"liquid loaded: '{new_liquid_name}'")

    @staticmethod
    def load_workbench_recipes(file):

        global workbench_recipies

        data = json.load(file)
        for recipe in data["recipes"]:
            workbench_recipies.append(
                WorkbenchRecipe(recipe["ingredient1"], recipe["ingredient2"], recipe["result"]), recipe["category"],
                recipe["subcategory"])
            result = recipe["result"][0]
            logging.info(f"workbench recipe loaded: '{result}'")

    @staticmethod
    def load_engineering_workbench_recipes(file):

        global engineering_workbench_recipes
        global workbench_recipies

        for category_name, category in workbench_recipies.items():
            for subcategory_id, subcategory in category.items():
                for recipe in subcategory:
                    engineering_workbench_recipes.append(
                        EngineeringWorkbenchRecipe([recipe.ingredient1, recipe.ingredient2], recipe.result),
                        category_name, subcategory_id)

        data = json.load(file)
        for recipe in data["recipes"]:
            engineering_workbench_recipes.append(
                EngineeringWorkbenchRecipe(recipe["ingredients"], recipe["result"]),
                recipe["category"], recipe["subcategory"])
            result = recipe["result"][0]
            logging.info(f"engineering workbench recipe loaded: '{result}'")

    @staticmethod
    def load_furnace_recipes(file):

        global furnace_recipies

        data = json.load(file)
        for recipe in data["recipes"]:
            furnace_recipies.append(
                FurnaceRecipe(recipe["ingredient"], recipe["result"], recipe["weight"]))
            result = recipe["result"][0]
            logging.info(f"furnace recipe loaded: '{result}'")

    @staticmethod
    def load_anvil_recipes(file):

        global anvil_recipies

        data = json.load(file)
        for recipe in data["recipes"]:
            anvil_recipies.append(AnvilRecipe(recipe["ingredient"], recipe["result"]))
            result = recipe["result"][0]
            logging.info(f"anvil recipe loaded: '{result}'")

    @staticmethod
    def load_crusher_recipes(file):

        global crusher_recipies

        data = json.load(file)
        for recipe in data["recipes"]:
            crusher_recipies.append(
                CrusherRecipe(recipe["ingredient"], recipe["result"], recipe["time"], recipe["particle_type"]))
            result = recipe["result"][0]
            logging.info(f"crusher recipe loaded: '{result}'")

    @staticmethod
    def load_foundry_recipes(file):

        global foundry_recipies

        data = json.load(file)
        for recipe in data["recipes"]:
            foundry_recipies.append(
                FoundryRecipe(recipe["ingredient_tag"], recipe["mold"], recipe["result"], recipe["weight"]))
            result = recipe["result"][0]
            logging.info(f"foundry recipe loaded: '{result}'")

    @staticmethod
    def load_centrifuge_recipes(file):

        global centrifuge_recipies

        data = json.load(file)
        for recipe in data["recipes"]:
            centrifuge_recipies.append(
                MagneticCentrifugeRecipe(recipe["ingredient"], recipe["result1"], recipe["result2"], recipe["time"]))
            result1 = recipe["result1"][0]
            result2 = recipe["result2"][0]
            logging.info(f"centrifuge recipe loaded: '{result1}, {result2}'")

    @staticmethod
    def load_woodworking_machine_recipes(file):

        global woodworking_machine_recipies

        data = json.load(file)
        for recipe in data["recipes"]:
            woodworking_machine_recipies.append(
                WoodworkingMachineRecipe(recipe["ingredient"], recipe["result"], recipe["time"]))
            result = recipe["result"][0]
            logging.info(f"woodworking recipe loaded: '{result}'")

    def load_fuel_weight(self, file):

        global FUEL_WEIGHT

        data = json.load(file)

        for key, value in data.items():
            data[key] = self.evaluate_math_expression(str(value))

        FUEL_WEIGHT = FUEL_WEIGHT | data

    @staticmethod
    def load_tile_to_item(file):

        global TILE_TO_ITEM

        TILE_TO_ITEM = json.load(file)

    @staticmethod
    def load_tile_to_bucket(file):

        global TILE_TO_BUCKET

        TILE_TO_BUCKET = json.load(file)

    @staticmethod
    def load_achievements(file):

        global achievements

        for achievement in json.load(file)["data"]:

            try:

                name = achievement["name"]
                description = achievement["description"]
                pos = ACHIEVENT_SIZE * from_iterable(achievement["pos"])
                size = ACHIEVENT_SIZE * from_iterable(achievement["size"])
                parent = achievement["parent"]
                arrow = achievement["arrow_type"]

                icon_item = achievement["icon_item"]
                if icon_item not in items:
                    logging.warning(
                        f"Cant load achievement '{name}': Icon item '{icon_item}' not found in items: {achievement}")
                    continue
                icon = icon_item

                request = achievement["request"]
                if not isinstance(request, list):
                    logging.warning(f"Cant load achievement '{name}': Request field is not a list: {achievement}")
                    continue

                achievements.append(
                    Achievement(name, description, icon, request, AchievementVisualData(pos, size), parent, arrow))
                logging.info(f"achievement loaded: '{name}'")

            except Exception as e:

                logging.exception("Cant load achievement:")

    @staticmethod
    def load_coke_oven(file):

        global coke_oven_recipies

        data = json.load(file)
        for recipe in data["recipes"]:
            coke_oven_recipies.append(
                CokeOvenRecipe(recipe["ingredient"], recipe["result"], recipe["time"]))
            result = recipe["result"][0]
            logging.info(f"coke oven recipe loaded: '{result}'")

    def load_ores(self, file):

        global ORE_TYPES, ORE_TYPE_TO_ITEM, ORE_TYPE_TO_HP, TILE_TO_ORE_TYPE, ORE_TYPE_TO_TILE, ITEM_TO_ORE_TYPE, ORE_TEXTURES

        for ore_name, ore_data in json.load(file).items():
            ORE_TYPES.append(ore_name)
            ORE_TYPE_TO_ITEM[ore_name] = ore_data["item"]
            ORE_TYPE_TO_HP[ore_name] = self.evaluate_math_expression(str(ore_data["hardness"]))
            TILE_TO_ORE_TYPE[ore_data["tile"]] = ore_data["item"]
            ORE_TYPE_TO_TILE[ore_name] = ore_data["tile"]
            ITEM_TO_ORE_TYPE[ore_data["item"]] = ore_name
            ORE_TEXTURES[ore_name] = {}
            # ORE_TEXTURES[ore_name]["deposit"] = load_texture(ore_data["deposit_texture"], DEPOSIT_SIZE)
            ORE_TEXTURES[ore_name]["vein"] = load_texture(
                f"addons/{self.current_addon}/assets/entities/veins/{ore_name}.png", VEIN_SIZE)

    def load_particles(self):

        global PARTICLE_TEXTURES

        try:
            new_particles = {
                f.split('.')[0]: load_texture(f"addons/{self.current_addon}/assets/particles/{f}", PARTICLE_SIZE) for f
                in os.listdir(f"addons/{self.current_addon}/assets/particles")
            }
            PARTICLE_TEXTURES = PARTICLE_TEXTURES | new_particles
        except:
            pass

    @staticmethod
    def load_chemical_reactor_recipes(file, overrides):

        data = json.load(file)

        for recipe in data["recipes"]:

            if len(recipe["input_liquids"]) <= 2 and len(recipe["input_items"]) <= 4 and len(
                    recipe["output_liquids"]) <= 2 and len(recipe["output_items"]) <= 4:
                chemical_reactor_recipes.append(ChemicalReactorRecipe(**recipe))
                logging.info(f"chemical reactor recipe loaded: '{recipe['formula']}'")
            else:
                logging.error(f"cant load recipe '{recipe['formula']}': invalid components")

    def load_addon(self, addon_name):

        self.current_addon = addon_name

        logging.info(f"Loading '{addon_name}' addon")

        path = f"addons/{addon_name}"

        logging.info("loading info.json")
        try:
            with open(f"{path}/info.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if "name" not in data: data["name"] = addon_name
                if "description" not in data: data["description"] = addon_name
                addons[addon_name] = data
            logging.info(f"Success")
        except FileNotFoundError:
            addons[addon_name] = {"name": addon_name, "description": addon_name}
            logging.info(f"Success")
        except:
            logging.warning(f"Error")

        if os.path.exists(f"{path}/icon.png"):
            icon = pg.image.load(f"{path}/icon.png")
        else:
            icon = pg.image.load(f"assets/default_addon_icon.png")
        addons[addon_name]["icon"] = icon.copy()

        self.load_file(self.load_constants, "constants.json")
        self.load_file(self.load_starting_items, "misc/starting_items.json")
        self.load_file(self.load_tiles, "tiles.json")
        self.load_file(self.load_fuel_weight, "misc/fuel_weight.json")
        self.load_file(self.load_items, "items.json")
        self.load_file(self.load_liquids, "liquids.json")
        self.load_file(self.load_workbench_recipes, "recipes/workbench.json")
        self.load_file(self.load_engineering_workbench_recipes, "recipes/engineering_workbench.json")
        self.load_file(self.load_furnace_recipes, "recipes/furnace.json")
        self.load_file(self.load_anvil_recipes, "recipes/anvil.json")
        self.load_file(self.load_crusher_recipes, "recipes/crusher.json")
        self.load_file(self.load_centrifuge_recipes, "recipes/centrifuge.json")
        self.load_file(self.load_foundry_recipes, "recipes/foundry.json")
        self.load_file(self.load_woodworking_machine_recipes, "recipes/woodworking_machine.json")
        self.load_file(self.load_tile_to_item, "misc/tile_to_item.json")
        self.load_file(self.load_tile_to_bucket, "misc/tile_to_bucket.json")
        self.load_file(self.load_achievements, "achievements.json")
        self.load_file(self.load_ores, "ores.json")
        self.load_file(self.load_coke_oven, "recipes/coke_oven.json")
        self.load_file(self.load_chemical_reactor_recipes, "recipes/chemical_reactor.json")
        self.load_particles()

    def load_addons(self):

        logging.info("Loading Addons...")

        addon_dependencies = {}
        ordered_addons = os.listdir("addons")

        for addon in ordered_addons:
            try:
                addon_dependencies[addon] = os.listdir(f"addons/{addon}/overrides")
            except FileNotFoundError:
                addon_dependencies[addon] = []

        def sort_addons(dependencies):
            visited = set()
            sorted_addons = []
            all_addons = set(dependencies.keys())

            def visit(addon):
                if addon in visited:
                    return
                if addon not in all_addons:
                    logging.error(f"Missing dependency: {addon}")
                    raise ValueError(f"Missing dependency: {addon}")
                visited.add(addon)
                for dependency in dependencies.get(addon, []):
                    visit(dependency)
                sorted_addons.append(addon)

            for addon in dependencies:
                visit(addon)

            return sorted_addons

        ordered_addons = sort_addons(addon_dependencies)

        if "core" in ordered_addons:
            ordered_addons.remove("core")
            ordered_addons.insert(0, "core")

        string = "loading in order: "
        for addon in ordered_addons:
            string += f"{addon}, "
        logging.info(string[:-2])

        for addon in ordered_addons:
            self.load_addon(addon)

        tiles[255] = Tile("assets/null.png", "null", 1, True)
        tiles[254] = Tile("assets/tiles/old_stone_covering.png", "old stone covering", 1, True)


addon_loader = AddonLoader()
addon_loader.load_addons()
