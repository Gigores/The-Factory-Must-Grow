from scripts.UI.Components.BaseUIComponents import *
from scripts.Entities.Buildings.Furnace import Furnace
from scripts.Managers.GameAssets import *
from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.UI.Entities.BaseUI import BaseUI


class FurnaceUI(BaseUI, metaclass=UIRegistry):

    def __init__(self, parent):

        super().__init__(parent)

        self.furnace_ui_pos = (
            RESOLUTION.x / 2 - BLANK.get_width() / 2,
            RESOLUTION.y / 2 - BLANK.get_height() / 2
        )
        self.furnace_ui_textures = [
            pg.transform.scale(pg.image.load("assets/ingame_ui/furnace.png"), BLANK.get_size()),
            pg.transform.scale(pg.image.load("assets/ingame_ui/furnace_2.png"), BLANK.get_size()),
            pg.transform.scale(pg.image.load("assets/ingame_ui/furnace_3.png"), BLANK.get_size()),
            pg.transform.scale(pg.image.load("assets/ingame_ui/furnace_4.png"), BLANK.get_size()),
            pg.transform.scale(pg.image.load("assets/ingame_ui/furnace_5.png"), BLANK.get_size()),
        ]

        self.inventory_pos = (
            RESOLUTION.x / 2 - BLANK_WIDE.get_width() / 2,
            self.furnace_ui_pos[1] + self.furnace_ui_textures[0].get_height() - 25
        )
        self.inventory_buttons = []
        for i in range(len(self.parent.inventory)):
            pos = (self.inventory_pos[0] + 20 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * i, self.inventory_pos[1] + 60)
            btn = Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, pos)
            self.inventory_buttons.append(btn)

        self.recipies_pos = (
            RESOLUTION.x / 2 - BLANK.get_width(),
            RESOLUTION.y / 2 - BLANK.get_height() / 2
        )
        self.recipies_buttons = []

        for n, recipie in enumerate(furnace_recipies):
            texture = pg.Surface(SMALL_FRAME_SIZE)
            texture.fill("#a2a2a2")
            draw_item(texture, recipie.result[0], 1, (0, 0), SMALL_FRAME_SIZE)

            pos = (self.recipies_pos[0] + 20 + (SMALL_FRAME_SIZE[0] + 10) * n, self.recipies_pos[1] + 60)

            btn = Button(texture, None, "", SMALL_FRAME_SIZE, pos)

            self.recipies_buttons.append(btn)

        craft_button_size = (130, BLANK_WIDE.get_height() / 3 * 2)
        craft_button_pos = (
            RESOLUTION.x / 2 + 2 - craft_button_size[0] / 2,
            self.furnace_ui_pos[1] - craft_button_size[1] - 5
        )
        self.craft_button = Button(
            RED_BUTTON, RED_BUTTON_PRESSED, "CRAFT", craft_button_size, craft_button_pos, "#dddddd", BIG_FONT
        )
        refuel_button_size = (130, BLANK_WIDE.get_height() / 3 * 2)
        refuel_button_pos = (
            RESOLUTION.x / 2 - 2 - refuel_button_size[0] * 1.5,
            self.furnace_ui_pos[1] - refuel_button_size[1] - 5
        )
        self.refuel_button = Button(
            BUTTON, BUTTON_PRESSED, "REFUEL", refuel_button_size, refuel_button_pos, "#606060", BIG_FONT
        )
        self.get_fuel_button = Button(
            BUTTON, BUTTON_PRESSED, "GET FUEL", refuel_button_size, refuel_button_pos, "#606060", BIG_FONT
        )
        get_button_pos = (
            self.craft_button.pos[0] + self.craft_button.texture.get_width() + 4,
            self.craft_button.pos[1]
        )
        get_button_size = self.craft_button.texture.get_size()
        self.get_button = Button(
            BUTTON, BUTTON_PRESSED, "GET", get_button_size, get_button_pos, "#606060", BIG_FONT
        )
        self.button_holder_pos = (
            self.refuel_button.pos[0] - 10,
            self.refuel_button.pos[1] - 10
        )
        button_holder_size = (
            self.refuel_button.texture.get_width() + self.craft_button.texture.get_width() + self.get_button.texture.get_width() + 30,
            self.refuel_button.texture.get_height() * 1.5,
        )
        self.button_holder_texture = pg.transform.scale(BLANK, button_holder_size)

        self.current_texture_id = 0
        self.a = False

        self.fuel_slot_pos = (self.furnace_ui_pos[0] + 404, self.furnace_ui_pos[1] + 188)
        self.fuel_slot_data = (None, 0)
        self.fuel_slot_button = Button(BUTTON, BUTTON_PRESSED, "", SMALL_FRAME_SIZE, self.fuel_slot_pos)

        self.ingredient_slot_pos = (self.furnace_ui_pos[0] + 76, self.furnace_ui_pos[1] + 188)
        self.ingredient_slot_data = (None, 0)
        self.ingredient_slot_button = Button(BUTTON, BUTTON_PRESSED, "", SMALL_FRAME_SIZE, self.ingredient_slot_pos)

        self.result_slot_pos = (self.furnace_ui_pos[0] + 244, self.furnace_ui_pos[1] + 78)
        self.result_slot_data = (None, 0)
        self.result_slot_button = Button(BUTTON, BUTTON_PRESSED, "", SMALL_FRAME_SIZE, self.result_slot_pos)

        self.arrow_pos = (self.furnace_ui_pos[0] + 106, self.furnace_ui_pos[1] + 98)
        self.arrow_textures = [
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/0.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/1.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/2.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/3.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/4.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/5.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/6.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/7.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/8.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/9.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/10.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/11.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/12.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/13.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/14.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/15.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/16.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/17.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/18.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/19.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/20.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/21.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/22.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/23.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/24.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/25.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/26.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/27.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/28.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/29.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/30.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/31.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/32.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/33.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/34.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/35.png"), 6),
            pg.transform.scale_by(pg.image.load("assets/ingame_UI/furnace_arrow/36.png"), 6),
        ]
        self.arrow_texture_id = 0

        self.current_recipe_id = 0

        self.bg = pg.Surface(RESOLUTION.as_tuple())
        self.bg.fill("#000000")
        # self.bg.blit(self.furnace_ui_textures[self.current_texture_id], self.furnace_ui_pos)
        #self.bg.blit(BLANK, self.recipies_pos)
        #self.bg.blit(FONT.render("Recipies", True, "#757575"), (self.recipies_pos[0] + 20, self.recipies_pos[1] + 20))
        self.bg.blit(BLANK_WIDE, self.inventory_pos)
        self.bg.blit(FONT.render("Inventory", True, "#757575"), (self.inventory_pos[0] + 30, self.inventory_pos[1] + 20))
        self.bg.set_colorkey("#000000")

        self.obj = None

    def draw(self, display):

        screen.blit(self.furnace_ui_textures[self.current_texture_id], self.furnace_ui_pos)

        screen.blit(self.bg, (0, 0))

        screen.blit(self.arrow_textures[self.arrow_texture_id], self.arrow_pos)

        for i, (n, a) in enumerate(zip(self.parent.inventory.n, self.parent.inventory.a)):

            pos = (self.inventory_pos[0] + 20 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * i, self.inventory_pos[1] + 60)
            draw_item(screen, n, a, pos, FRAME_SIZE)

        draw_item(screen, self.fuel_slot_data[0], self.fuel_slot_data[1], self.fuel_slot_pos, SMALL_FRAME_SIZE, draw_bg=False)
        draw_item(screen, self.ingredient_slot_data[0], self.ingredient_slot_data[1], self.ingredient_slot_pos, SMALL_FRAME_SIZE, draw_bg=False)
        draw_item(screen, self.result_slot_data[0], self.result_slot_data[1], self.result_slot_pos, SMALL_FRAME_SIZE, draw_bg=False)

        self.draw_cursor_slot()

    def events(self, events):

        pass

    def inventory_shift(self, inventory, button_id):

        item_name = inventory.n[button_id]
        item_amount = inventory.a[button_id]

        if item_name in FUEL_WEIGHT:
            if self.obj.fuel_slot.can_fit(item_name, item_amount):
                self.parent.inventory.pop_from_slot(button_id, item_amount)
                self.obj.fuel_slot.append(item_name, item_amount)
        elif furnace_recipies.find(item_name):
            if self.obj.ingredient_slot.can_fit(item_name, item_amount):
                self.parent.inventory.pop_from_slot(button_id, item_amount)
                self.obj.ingredient_slot.append(item_name, item_amount)

    def result_slot_shift(self, slot):

        if self.parent.inventory.can_fit(slot.item_name, slot.item_amount):
            self.parent.inventory.append(slot.item_name, slot.item_amount)
            slot.clear()

    def ingredient_slot_shift(self, slot):

        if self.parent.inventory.can_fit(slot.item_name, slot.item_amount):
            self.parent.inventory.append(slot.item_name, slot.item_amount)
            slot.clear()

    def fuel_slot_shift(self, slot):

        if self.parent.inventory.can_fit(slot.item_name, slot.item_amount):
            self.parent.inventory.append(slot.item_name, slot.item_amount)
            slot.clear()

    def update(self, obj: Furnace):

        self.obj = obj

        self._handle_inventory(self.parent.inventory, self.inventory_buttons, self.inventory_shift)
        self._handle_slot(obj.result_slot, self.result_slot_button, self.result_slot_shift, output_only=True)
        self._handle_slot(obj.ingredient_slot, self.ingredient_slot_button, self.ingredient_slot_shift)
        self._handle_slot(obj.fuel_slot, self.fuel_slot_button, self.fuel_slot_shift)

        if obj.fuel_left == 0: self.current_texture_id = 0
        else: self.current_texture_id = int(3 * obj.fuel_left / obj.fuel_start_amount) + 1

        if obj.progress == 0: self.arrow_texture_id = 0
        else:
            self.arrow_texture_id = len(self.arrow_textures) - int(len(self.arrow_textures) / obj.progress_start * obj.progress)
            if self.arrow_texture_id > len(self.arrow_textures) - 1: self.arrow_texture_id = len(self.arrow_textures) - 1

        self.fuel_slot_data = (obj.fuel_slot.item_name, obj.fuel_slot.item_amount)
        self.result_slot_data = (obj.result_slot.item_name, obj.result_slot.item_amount)
        self.ingredient_slot_data = (obj.ingredient_slot.item_name, obj.ingredient_slot.item_amount)
