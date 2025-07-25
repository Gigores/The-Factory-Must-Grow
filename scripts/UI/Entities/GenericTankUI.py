from scripts.UI.Components.Bg import Bg
from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.UI.Entities.BaseUI import BaseUI
from scripts.constants import *
from scripts.UI.Components.BaseUIComponents import *


class GenericTankUI(BaseUI, metaclass=UIRegistry):

    def __init__(self, parent):

        super().__init__(parent)
        self.obj = None

        self.main_ui_pos = RESOLUTION / Vector(2, 2) - Vector(BLANK.get_width(), BLANK.get_height()) / Vector(2, 2)
        self.main_ui_texture = load_texture("assets/ingame_UI/single_tank.png", from_iterable(BLANK.get_size()))

        self.pixel_size = from_iterable(BLANK.get_size()) / Vector(90, 68)

        self.input_slot_pos = self.main_ui_pos + self.pixel_size * Vector(48, 15)
        self.input_slot_button = Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, self.input_slot_pos.as_tuple())
        self.output_slot_pos = self.main_ui_pos + self.pixel_size * Vector(48, 33)
        self.output_slot_button = Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, self.output_slot_pos.as_tuple())

        self.liquid_window_rect = pg.Rect(self.main_ui_pos.x + self.pixel_size.x * 29, self.main_ui_pos.y + self.pixel_size.y * 23, self.pixel_size.x * 8, self.pixel_size.y * 29)

        self.player_inventory_pos = Vector(RESOLUTION.x / 2 - BLANK_WIDE.get_width() / 2, self.main_ui_pos.y + BLANK.get_height() - 50)
        self.player_inventory_buttons = []
        for n in range(len(self.parent.inventory)):
            pos = self.__get_player_ui_button_pos(n)
            self.player_inventory_buttons.append(Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, pos))

        self.bg = Bg()
        self.bg.blit(self.main_ui_texture, self.main_ui_pos.as_tuple())
        self.bg.blit(BLANK_WIDE, self.player_inventory_pos.as_tuple())
        self.bg.blit(FONT.render("Inventory", True, "#757575"), (self.player_inventory_pos.x + 20, self.player_inventory_pos.y + 20))

    def slot_shift(self, slot):

        if self.parent.inventory.can_fit(slot.item_name, slot.item_amount):
            self.parent.inventory.append(slot.item_name, slot.item_amount)
            slot.clear()

    def inventory_shift(self, inventory, button_id):

        if self.obj.input_slot.can_fit(self.parent.inventory.n[button_id], self.parent.inventory.a[button_id]):
            self.obj.input_slot.append(self.parent.inventory.n[button_id], self.parent.inventory.a[button_id])
            self.parent.inventory.n[button_id] = None
            self.parent.inventory.a[button_id] = 0

    def draw(self, display):

        pg.draw.rect(screen, "#000000", self.liquid_window_rect)

        if self.obj:
            self._draw_liquid(self.liquid_window_rect, self.obj.tank)

        self.bg.draw()

        if self.obj:
            draw_item(screen, self.obj.input_slot.item_name, self.obj.input_slot.item_amount, self.input_slot_pos.as_tuple(), FRAME_SIZE)
            draw_item(screen, self.obj.output_slot.item_name, self.obj.output_slot.item_amount, self.output_slot_pos.as_tuple(), FRAME_SIZE)

        for n, (item, amount) in enumerate(zip(self.parent.inventory.n, self.parent.inventory.a)):
            pos = self.__get_player_ui_button_pos(n)
            draw_item(screen, item, amount, pos, FRAME_SIZE)

        self.draw_cursor_slot()

    def events(self, events):

        pass

    def update(self, obj):

        self.obj = obj

        self._handle_inventory(self.parent.inventory, self.player_inventory_buttons, self.inventory_shift)

        self._handle_slot(self.obj.input_slot, self.input_slot_button, self.slot_shift)
        self._handle_slot(self.obj.output_slot, self.output_slot_button, self.slot_shift)

        self._draw_tank_info(self.liquid_window_rect, self.obj.tank)

    def __get_player_ui_button_pos(self, n: int):

        return self.player_inventory_pos.x + 20 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * n, self.player_inventory_pos.y + 60
