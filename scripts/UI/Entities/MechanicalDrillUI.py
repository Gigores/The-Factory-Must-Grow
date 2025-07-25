from scripts.Entities.Buildings.MechanicalDrill import MechanicalDrill
from scripts.UI.Entities.BaseUI import BaseUI
from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.Managers.GameAssets import *
from scripts.UI.Components.BaseUIComponents import *
from scripts.UI.Components.Bg import Bg


def resize_surface_to_match_width(surf1, surf2):
    width1, height1 = surf1.get_size()
    width2, height2 = surf2.get_size()

    new_width = width1
    new_height = int(height2 * (new_width / width2))

    resized_surface = pg.transform.scale(surf2, (new_width, new_height))

    return resized_surface


UI_TEXTURES = [
    resize_surface_to_match_width(BLANK, pg.image.load("assets/ingame_UI/mechanical_drill.png")),
    resize_surface_to_match_width(BLANK, pg.image.load("assets/ingame_UI/mechanical_drill_2.png")),
    resize_surface_to_match_width(BLANK, pg.image.load("assets/ingame_UI/mechanical_drill_3.png")),
    resize_surface_to_match_width(BLANK, pg.image.load("assets/ingame_UI/mechanical_drill_4.png")),
    resize_surface_to_match_width(BLANK, pg.image.load("assets/ingame_UI/mechanical_drill_5.png")),
]


def percentage(part, whole):
    if whole == 0:
        return 100
    return round((part / whole) * 100)


class MechanicalDrillUI(BaseUI, metaclass=UIRegistry):

    def __init__(self, parent):

        super().__init__(parent)
        self.obj = None

        self.main_ui_pos = RESOLUTION / Vector(2, 2) - Vector(UI_TEXTURES[0].get_width(), UI_TEXTURES[0].get_height()) / Vector(2, 2)

        self.player_inventory_pos = Vector(RESOLUTION.x / 2 - BLANK_WIDE.get_width() / 2,
                                           self.main_ui_pos.y + UI_TEXTURES[0].get_height() - 50)
        self.slot_size = (from_iterable(UI_TEXTURES[0].get_size()) / Vector(9, 10.1)).as_tuple()
        self.player_inventory_buttons = []
        for n in range(len(self.parent.inventory)):
            pos = self.__get_player_ui_button_pos(n)
            self.player_inventory_buttons.append(Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, pos))

        self.drill_inventory_pos = Vector(RESOLUTION.x / 2 - BLANK_WIDE.get_width() / 2,
                                           self.main_ui_pos.y + UI_TEXTURES[0].get_height() - 50)
        self.drill_inventory_buttons = []
        for n in range(9):
            pos = self.__get_drill_ui_button_pos(n)
            self.drill_inventory_buttons.append(Button(BUTTON, BUTTON_PRESSED, "", self.slot_size, pos))

        self.font = pg.font.Font("assets/commodore.ttf", 30)

        self.text_box_padding = 5
        self.text_box_margin = 15
        self.text_box_size = Vector(BLANK.get_width() - self.text_box_margin * 2, self.font.get_height() * 2 + self.text_box_padding * 2)
        self.text_box_pos = self.main_ui_pos + from_iterable(UI_TEXTURES[0].get_size()) / Vector(8.1818, 9.18) + Vector(self.text_box_margin, self.text_box_margin)

        self.current_texture_id = 0

        self.fuel_slot_pos = self.main_ui_pos + from_iterable(UI_TEXTURES[0].get_size()) / Vector(1.4285714285714285714285714285714, 2.02)
        self.fuel_slot_button = Button(BUTTON, BUTTON_PRESSED, "", self.slot_size, self.fuel_slot_pos.as_tuple())

        self.bg = Bg()
        # self.bg.blit(self.main_ui_texture, self.main_ui_pos.as_tuple())
        self.bg.blit(BLANK_WIDE, self.player_inventory_pos.as_tuple())
        self.bg.blit(FONT.render("Inventory", True, "#757575"),
                    (self.player_inventory_pos.x + 20, self.player_inventory_pos.y + 20))

    def slot_shift(self, slot):

        if self.parent.inventory.can_fit(slot.item_name, slot.item_amount):
            self.parent.inventory.append(slot.item_name, slot.item_amount)
            slot.clear()

    def inventory_shift(self, inventory, button_id):

        pass

    def drill_inventory_shift(self, inventory, button_id):

        if self.parent.inventory.can_fit(inventory.n[button_id], inventory.a[button_id]) :
            self.parent.inventory.append(inventory.n[button_id], inventory.a[button_id])
            inventory.n[button_id] = None
            inventory.a[button_id] = 0

    def fuel_shift(self, slot):

        if self.parent.inventory.can_fit(slot.item_name, slot.item_amount):
            self.parent.inventory.append(slot.item_name, slot.item_amount)
            slot.clear()

    def events(self, events):

        pass

    def update(self, obj: MechanicalDrill):

        self.obj = obj

        if obj.fuel_left == 0: self.current_texture_id = 0
        else: self.current_texture_id = int(3 * obj.fuel_left / obj.fuel_start_amount) + 1

        self._handle_inventory(self.parent.inventory, self.player_inventory_buttons, self.inventory_shift)
        self._handle_inventory(self.obj.inventory, self.drill_inventory_buttons, self.drill_inventory_shift)
        self._handle_slot(self.obj.fuel_slot, self.fuel_slot_button, self.fuel_shift)

    def draw(self, display):

        screen.blit(UI_TEXTURES[self.current_texture_id], self.main_ui_pos.as_tuple())
        self.bg.draw()
        if self.obj:
            if self.obj.current_ore is None:
                text = "Ore not found"
            else:
                text = f"Found {items[self.obj.current_ore].name}"
            text_surf = self.font.render(f" {text}", True, "green")
            screen.blit(text_surf, (self.text_box_pos + Vector(self.text_box_padding, self.text_box_padding + self.font.get_height())).as_tuple())
            text_surf = self.font.render("Ore status:", True, "green")
            screen.blit(text_surf, (self.text_box_pos + Vector(self.text_box_padding, self.text_box_padding)).as_tuple())
            text_surf = self.font.render(f"Progress: {100-percentage(self.obj.progress, self.obj.beggining_progress)}%", True, "green")
            screen.blit(text_surf, (self.text_box_pos + Vector(self.text_box_padding, self.text_box_padding + self.font.get_height() * 2)).as_tuple())
            for n, (item, amount) in enumerate(zip(self.obj.inventory.n, self.obj.inventory.a)):
                pos = self.__get_drill_ui_button_pos(n)
                draw_item(screen, item, amount, pos, self.slot_size, draw_bg=False)
            draw_item(screen, self.obj.fuel_slot.item_name, self.obj.fuel_slot.item_amount, self.fuel_slot_pos.as_tuple(), self.slot_size, draw_bg=False)
        for n, (item, amount) in enumerate(zip(self.parent.inventory.n, self.parent.inventory.a)):
            pos = self.__get_player_ui_button_pos(n)
            draw_item(screen, item, amount, pos, FRAME_SIZE)
        self.draw_cursor_slot()

    def __get_player_ui_button_pos(self, n: int):

        return self.player_inventory_pos.x + 20 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * n, self.player_inventory_pos.y + 60

    def __get_drill_ui_button_pos(self, n: int):

        return self.main_ui_pos.x + UI_TEXTURES[0].get_width() / 18 + (n % 3) * (UI_TEXTURES[0].get_width() / 8.181818181), self.main_ui_pos.y + UI_TEXTURES[0].get_height() / 1.87037037 + (n // 3) * (UI_TEXTURES[0].get_height() / 9.181818181818181818181818181818)