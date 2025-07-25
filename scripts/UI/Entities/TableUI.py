from scripts.UI.Components.BaseUIComponents import *
from scripts.Entities.Buildings.Furniture import Table
from scripts.Managers.GameAssets import *
from scripts.UI.Components.Bg import Bg
from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.UI.Entities.BaseUI import BaseUI


class TableUI(BaseUI, metaclass=UIRegistry):

    def __init__(self, parent):

        super().__init__(parent)

        self.main_ui_texture = pg.transform.scale(BLANK, BLANK.get_size())
        self.main_ui_pos = RESOLUTION / Vector(2, 2) - Vector(self.main_ui_texture.get_width(),
                                                              self.main_ui_texture.get_height()) / Vector(2, 2)

        self.player_inventory_pos = Vector(RESOLUTION.x / 2 - BLANK_WIDE.get_width() / 2,
                                           self.main_ui_pos.y + self.main_ui_texture.get_height() - 50)
        self.player_inventory_buttons = []
        for n in range(len(self.parent.inventory)):
            pos = self.__get_player_ui_button_pos(n)
            self.player_inventory_buttons.append(Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, pos))

        self.inventory_slot_size = from_iterable(FRAME_SIZE) * Vector(1.5, 1.5)
        self.inventory_size = self.inventory_slot_size * Vector(3, 1)
        self.inventory_pos = Vector(self.main_ui_pos.x + (BLANK.get_width() / 2 - self.inventory_size.x / 2) - 5 * 2,
                                    self.main_ui_pos.y + (BLANK.get_height() / 2 - self.inventory_size.y / 2))
        self.inventory_buttons = []
        for n in range(3):
            pos = self.__get_inventory_button_pos(n).as_tuple()
            self.inventory_buttons.append(Button(BUTTON, BUTTON_PRESSED, "", self.inventory_slot_size.as_tuple(), pos))
        self.inventory = None

        self.bg = Bg()
        self.bg.blit(self.main_ui_texture, self.main_ui_pos.as_tuple())
        self.bg.blit(FONT.render("Table", True, "#757575"),
                    (self.main_ui_pos.x + 20, self.main_ui_pos.y + 20))
        self.bg.blit(BLANK_WIDE, self.player_inventory_pos.as_tuple())
        self.bg.blit(FONT.render("Inventory", True, "#757575"),
                    (self.player_inventory_pos.x + 20, self.player_inventory_pos.y + 20))

    def main_ui_shift(self, inventory, button_id):

        if self.parent.inventory.can_fit(inventory.n[button_id], inventory.a[button_id]):
            self.parent.inventory.append(inventory.n[button_id], inventory.a[button_id])
            inventory.n[button_id] = None
            inventory.a[button_id] = 0

    def inventory_shift(self, inventory, button_id):

        if self.inventory.can_fit(inventory.n[button_id], inventory.a[button_id]):
            self.inventory.append(inventory.n[button_id], inventory.a[button_id])
            inventory.n[button_id] = None
            inventory.a[button_id] = 0

    def update(self, obj: Table):

        self.inventory = obj.inventory

        self._handle_inventory(self.inventory, self.inventory_buttons, self.main_ui_shift)
        self._handle_inventory(self.parent.inventory, self.player_inventory_buttons, self.inventory_shift)

    def draw(self, display):

        self.bg.draw()

        for n, (item, amount) in enumerate(zip(self.parent.inventory.n, self.parent.inventory.a)):
            pos = self.__get_player_ui_button_pos(n)
            draw_item(screen, item, amount, pos, FRAME_SIZE)
        if self.inventory:
            for n, (item, amount) in enumerate(zip(self.inventory.n, self.inventory.a)):
                pos = self.__get_inventory_button_pos(n)
                draw_item(screen, item, amount, pos.as_tuple(), self.inventory_slot_size.as_tuple())

        self.draw_cursor_slot()

    def events(self, events):

        pass

    def __get_player_ui_button_pos(self, n: int):

        return self.player_inventory_pos.x + 20 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * n, self.player_inventory_pos.y + 60

    def __get_inventory_button_pos(self, n: int):

        return self.inventory_pos + self.inventory_slot_size * Vector(n, 0) + Vector(10 * n, 0)
