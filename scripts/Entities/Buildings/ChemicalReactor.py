from scripts.Entities.ABC.Building import Building
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.Managers.IngameManagers.Inventory import Inventory, Slot
from scripts.Managers.IngameManagers.InventoryLiquids import InventiryTankArray
from scripts.constants import *
from scripts.Managers.GameAssets import chemical_reactor_recipes
from math import sin
from scripts.Entities.ABC.ElectricNode import ElectricNode


TEXTURE_SIZE = TILE_SIZE * Vector(3, 3)
TEXTURE_OFFSET = TEXTURE_SIZE * Vector(-0.5, -0.9)
TOUCH_HITBOX_SIZE = TEXTURE_SIZE * Vector(0.9, 0.5)
TOUCH_HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.05, 0.5)
HITBOX_SIZE = TEXTURE_SIZE * Vector(0.8, 0.8)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.1, 0.2)
TEXTURE = load_texture("assets/entities/chemical_reactor.png", TEXTURE_SIZE)
PIXEL_SIZE = TEXTURE_SIZE / Vector(50, 50)
WINDOW_RECT = pg.Rect(PIXEL_SIZE.x * 30, PIXEL_SIZE.y * (18 - 1), PIXEL_SIZE.x * (6 + 2), PIXEL_SIZE.y * (9 + 3))
DEFAULT_LIQUID_TOPLEFT = Vector(WINDOW_RECT.x, WINDOW_RECT.y + WINDOW_RECT.h / 2)
DEFAULT_LIQUID_TOPRIGHT = Vector(WINDOW_RECT.x + WINDOW_RECT.w, WINDOW_RECT.y + WINDOW_RECT.h / 2)
DEFAULT_LIQUID_TOPSEMILEFT = Vector(WINDOW_RECT.x + WINDOW_RECT.w * 0.25, WINDOW_RECT.y + WINDOW_RECT.h / 2)
DEFAULT_LIQUID_TOP = Vector(WINDOW_RECT.x + WINDOW_RECT.w * 0.5, WINDOW_RECT.y + WINDOW_RECT.h / 2)
DEFAULT_LIQUID_TOPSEMIRIGHT = Vector(WINDOW_RECT.x + WINDOW_RECT.w * 0.75, WINDOW_RECT.y + WINDOW_RECT.h / 2)
DEFAULT_LIQUID_BOTTOMLEFT = Vector(WINDOW_RECT.x, WINDOW_RECT.y + WINDOW_RECT.h)
DEFAULT_LIQUID_BOTTOMRIGHT = Vector(WINDOW_RECT.x + WINDOW_RECT.w, WINDOW_RECT.y + WINDOW_RECT.h)
LIQUID_JIGGLE_RANGE = WINDOW_RECT.h / 8
SOUND1 = pg.mixer.Sound("sound/pickaxe_1.mp3")
SOUND1.set_volume(0.5)
SOUND2 = pg.mixer.Sound("sound/ore_done.mp3")
SOUND2.set_volume(0.5)
WIRE_CONNECTION_OFFSET = PIXEL_SIZE * Vector(-10, -9)


class ChemicalReactor(ElectricNode, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE, 600, TEXTURE_OFFSET,
                         "chemical_reactor", "pickaxe", punch_sound=SOUND1, break_sound=SOUND2,
                         collider_hitbox_offset=TOUCH_HITBOX_OFFSET, collider_hitbox_size=TOUCH_HITBOX_SIZE,
                         ui_id="ChemicalDrillUI", wire_connection_offset=WIRE_CONNECTION_OFFSET,
                         network_weight=-200_000)

        self.current_color = "#55ff55"
        self.anim_val = 3

        self.input = Inventory(self.parent, 4)
        self.output = Inventory(self.parent, 4, log=True)

        self.input_liquids = InventiryTankArray(2, 50)
        self.output_liquids = InventiryTankArray(2, 50)

        self.input_bucket_1 = Slot()
        self.input_bucket_2 = Slot()
        self.input_bucket_3 = Slot()
        self.input_bucket_4 = Slot()
        self.output_bucket_1 = Slot()
        self.output_bucket_2 = Slot()
        self.output_bucket_3 = Slot()
        self.output_bucket_4 = Slot()

        #self.input_fluids.pump_in("water", 10)
        #self.input_fluids.pump_in("carbon_monoxide", 10)

        self.current_recipe = 0
        self.progress = 0
        self.total_progress = 0
        self.enough_energy = False

    def set_recipe(self, recipe_id):

        self.current_recipe = recipe_id
        self.progress = 0
        self.total_progress = 0

    def distribute(self, energy: int):

        self.enough_energy = energy >= -self.network_weight

    def select_texture(self) -> pg.Surface:

        surface = pg.Surface(self.texture.get_size())
        surface.fill((0, 255, 0))
        surface.set_colorkey((0, 255, 0))
        pg.draw.rect(surface, "#2e2e2e", WINDOW_RECT)

        if self.active:

            custom_liquid_topleft = DEFAULT_LIQUID_TOPLEFT + Vector(0, sin(self.parent.animation_counter / 10) * LIQUID_JIGGLE_RANGE)
            custom_liquid_topsemileft = DEFAULT_LIQUID_TOPSEMILEFT + Vector(0, sin(self.parent.animation_counter / 10 + 5) * LIQUID_JIGGLE_RANGE)
            custom_liquid_top = DEFAULT_LIQUID_TOP + Vector(0, sin(self.parent.animation_counter / 10 + 10) * LIQUID_JIGGLE_RANGE)
            custom_liquid_topsemiright = DEFAULT_LIQUID_TOPSEMIRIGHT + Vector(0, sin(self.parent.animation_counter / 10 + 15) * LIQUID_JIGGLE_RANGE)
            custom_liquid_topright = DEFAULT_LIQUID_TOPRIGHT + Vector(0, sin(self.parent.animation_counter / 10 + 20) * LIQUID_JIGGLE_RANGE)

            liquid_polygon = [
                custom_liquid_topleft.as_tuple(), custom_liquid_topsemileft.as_tuple(), custom_liquid_top.as_tuple(),
                custom_liquid_topsemiright.as_tuple(), custom_liquid_topright.as_tuple(),
                DEFAULT_LIQUID_BOTTOMRIGHT.as_tuple(), DEFAULT_LIQUID_BOTTOMLEFT.as_tuple()
            ]

            pg.draw.polygon(surface, self.current_color, liquid_polygon)

        surface.blit(self.texture, (0, 0))
        return surface

    def update(self, preview_mode: bool = False):

        super().update(preview_mode)

        self._handle_tank_interraction(self.input_liquids[0], self.input_bucket_1, self.output_bucket_1)
        self._handle_tank_interraction(self.input_liquids[1], self.input_bucket_2, self.output_bucket_2)
        self._handle_tank_interraction(self.output_liquids[0], self.input_bucket_3, self.output_bucket_3, True)
        self._handle_tank_interraction(self.output_liquids[1], self.input_bucket_4, self.output_bucket_4, True)

        self.active = self.total_progress != 0

        if self.can_cook() and self.total_progress == 0:
            self.input.pop_m(chemical_reactor_recipes[self.current_recipe].input_items)
            self.input_liquids.pump_out_m(chemical_reactor_recipes[self.current_recipe].input_liquids)
            self.total_progress = chemical_reactor_recipes[self.current_recipe].time
            self.current_color = chemical_reactor_recipes[self.current_recipe].color

        if self.parent.animation_counter % 3 == 0:
            if self.total_progress != 0:
                self.progress += 1
                if self.progress >= self.total_progress:
                    self.total_progress = 0
                    self.progress = 0
                    self.output.append_m(chemical_reactor_recipes[self.current_recipe].output_items)
                    self.output_liquids.pump_in_m(chemical_reactor_recipes[self.current_recipe].output_liquids)

    def enough_engredients(self) -> bool:

        return all([
            self.input_liquids.has_m(chemical_reactor_recipes[self.current_recipe].input_liquids),
            self.input.has_m(chemical_reactor_recipes[self.current_recipe].input_items),
            self.output_liquids.can_pump_in_m(chemical_reactor_recipes[self.current_recipe].output_liquids),
            self.output.can_fit_m(chemical_reactor_recipes[self.current_recipe].output_items)
        ])

    def can_cook(self) -> bool:

        return self.enough_energy and self.enough_engredients()

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "code": self.code,
            "pos": self.pos.as_tuple(),

            "input_items": self.input.dumb(),
            "input_liquids": self.input_liquids.dumb(),
            "output_items": self.output.dumb(),
            "output_liquids": self.output_liquids.dumb(),

            "input_bucket_1": self.input_bucket_1.dumb(),
            "input_bucket_2": self.input_bucket_2.dumb(),
            "input_bucket_3": self.input_bucket_3.dumb(),
            "input_bucket_4": self.input_bucket_4.dumb(),
            "output_bucket_1": self.output_bucket_1.dumb(),
            "output_bucket_2": self.output_bucket_2.dumb(),
            "output_bucket_3": self.output_bucket_3.dumb(),
            "output_bucket_4": self.output_bucket_4.dumb(),

            "current_color": self.current_color,
            "current_recipe": self.current_recipe,
            "progress": self.progress,
            "total_progress": self.total_progress,
            "enough_energy": self.enough_energy
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.code = data["code"]

        self.input.load(data["input_items"])
        self.input_liquids.load(data["input_liquids"])
        self.output.load(data["output_items"])
        self.output_liquids.load(data["output_liquids"])

        self.input_bucket_1.load(data["input_bucket_1"])
        self.input_bucket_2.load(data["input_bucket_2"])
        self.input_bucket_3.load(data["input_bucket_3"])
        self.input_bucket_4.load(data["input_bucket_4"])
        self.output_bucket_1.load(data["output_bucket_1"])
        self.output_bucket_2.load(data["output_bucket_2"])
        self.output_bucket_3.load(data["output_bucket_3"])
        self.output_bucket_4.load(data["output_bucket_4"])

        self.current_color = data["current_color"]
        self.current_recipe = data["current_recipe"]
        self.progress = data["progress"]
        self.total_progress = data["total_progress"]
        self.enough_energy = data["enough_energy"]
