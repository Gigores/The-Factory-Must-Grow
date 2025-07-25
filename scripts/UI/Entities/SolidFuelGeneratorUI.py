from scripts.UI.Components.BaseUIComponents import *
from scripts.Entities.Buildings.SolidFuelGenerator import SolidFuelGenerator
from scripts.Managers.GameAssets import *
from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.UI.Entities.BaseUI import BaseUI


class SolidFuelGeneratorUI(BaseUI, metaclass=UIRegistry):

    def __init__(self, parent):

        super().__init__(parent)
        self.obj = None

        self.furnace_ui_pos = (
            RESOLUTION.x / 2 - BLANK.get_width() / 2,
            RESOLUTION.y / 2 - BLANK.get_height() / 2
        )
        self.furnace_ui_textures = [
            pg.transform.scale(pg.image.load("assets/ingame_ui/solid_fuel_generator.png"), BLANK.get_size()),
            pg.transform.scale(pg.image.load("assets/ingame_ui/solid_fuel_generator_2.png"), BLANK.get_size()),
            pg.transform.scale(pg.image.load("assets/ingame_ui/solid_fuel_generator_3.png"), BLANK.get_size()),
            pg.transform.scale(pg.image.load("assets/ingame_ui/solid_fuel_generator_4.png"), BLANK.get_size()),
            pg.transform.scale(pg.image.load("assets/ingame_ui/solid_fuel_generator_5.png"), BLANK.get_size()),
        ]
        self.current_texture_id = 0

        self.inventory_pos = (
            RESOLUTION.x / 2 - BLANK_WIDE.get_width() / 2,
            self.furnace_ui_pos[1] + self.furnace_ui_textures[0].get_height() - 25
        )
        self.inventory_buttons = []
        for i in range(len(self.parent.inventory)):
            pos = (self.inventory_pos[0] + 20 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * i, self.inventory_pos[1] + 60)
            btn = Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, pos)
            self.inventory_buttons.append(btn)

        self.fuel_slot_pos = from_iterable(self.furnace_ui_pos) + from_iterable(BLANK.get_size()) / Vector(3.6, 6.1818181818181818181818181818182)
        self.fuel_slot_data = (None, 0)
        self.fuel_slot_button = Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, self.fuel_slot_pos.as_tuple())

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

        for i, (n, a) in enumerate(zip(self.parent.inventory.n, self.parent.inventory.a)):

            pos = (self.inventory_pos[0] + 20 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * i, self.inventory_pos[1] + 60)
            draw_item(screen, n, a, pos, FRAME_SIZE)

        draw_item(screen, self.fuel_slot_data[0], self.fuel_slot_data[1], self.fuel_slot_pos.as_tuple(), FRAME_SIZE, draw_bg=False)

        self.draw_cursor_slot()

    def events(self, events):

        pass

    def inventory_shift(self, inventory, button_id):

        pass

    def fuel_slot_shift(self, slot):

        if self.parent.inventory.can_fit(slot.item_name, slot.item_amount):
            self.parent.inventory.append(slot.item_name, slot.item_amount)
            slot.clear()

    def update(self, obj: SolidFuelGenerator):

        self.obj = obj

        self._handle_inventory(self.parent.inventory, self.inventory_buttons, self.inventory_shift)
        self._handle_slot(obj.fuel_slot, self.fuel_slot_button, self.fuel_slot_shift)

        if obj.fuel_left == 0: self.current_texture_id = 0
        else: self.current_texture_id = int(3 * obj.fuel_left / obj.fuel_total) + 1

        self.fuel_slot_data = (obj.fuel_slot.item_name, obj.fuel_slot.item_amount)
