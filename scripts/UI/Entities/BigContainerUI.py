from scripts.UI.Components.BaseUIComponents import *
from scripts.Entities.Buildings.BigContainer import BigContainer
from scripts.Managers.GameAssets import *
from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.UI.Components.Bg import Bg
from scripts.UI.Entities.BaseUI import BaseUI


class BigContainerUI(BaseUI, metaclass=UIRegistry):

    def __init__(self, parent):

        super().__init__(parent)

        self.inventory = None

        self.main_ui_size = from_iterable(BLANK.get_size()) * Vector(2, 1.5)
        self.main_ui_texture = pg.transform.scale(BLANK, self.main_ui_size.as_tuple())
        self.main_ui_pos = RESOLUTION / Vector(2, 2) - Vector(self.main_ui_texture.get_width(), self.main_ui_texture.get_height()) / Vector(2, 2)
        self.main_ui_buttons = []

        self.player_inventory_pos = Vector(RESOLUTION.x / 2 - BLANK_WIDE.get_width() / 2, self.main_ui_pos.y + self.main_ui_texture.get_height() - 50)
        self.player_inventory_buttons = []
        for n in range(len(self.parent.inventory)):
            pos = self.__get_player_ui_button_pos(n)
            self.player_inventory_buttons.append(Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, pos))

        self.bg = Bg()
        self.bg.blit(self.main_ui_texture, self.main_ui_pos.as_tuple())
        self.bg.blit(FONT.render("Big Container", True, "#757575"), (self.main_ui_pos.x + 20, self.main_ui_pos.y + 20))
        self.bg.blit(BLANK_WIDE, self.player_inventory_pos.as_tuple())
        self.bg.blit(FONT.render("Inventory", True, "#757575"), (self.player_inventory_pos.x + 20, self.player_inventory_pos.y + 20))

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

    def events(self, events):

        pass

    def update(self, obj: BigContainer):

        self.inventory = obj.inventory

        if not len(self.main_ui_buttons):
            for n in range(len(self.inventory)):
                pos = self.__get_main_ui_button_pos(n)
                self.main_ui_buttons.append(Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, pos,))

        self._handle_inventory(self.inventory, self.main_ui_buttons, self.main_ui_shift)
        self._handle_inventory(self.parent.inventory, self.player_inventory_buttons, self.inventory_shift)

    def draw(self, display):

        self.bg.draw()

        if self.inventory:
            for n, (item, amount) in enumerate(zip(self.inventory.n, self.inventory.a)):
                pos = self.__get_main_ui_button_pos(n)
                draw_item(screen, item, amount, pos, FRAME_SIZE)

        for n, (item, amount) in enumerate(zip(self.parent.inventory.n, self.parent.inventory.a)):
            pos = self.__get_player_ui_button_pos(n)
            draw_item(screen, item, amount, pos, FRAME_SIZE)

        self.draw_cursor_slot()

    def __get_main_ui_button_pos(self, n: int):

        return self.main_ui_pos.x + 36 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * (n % 10), self.main_ui_pos.y + 90 + (
                    FRAME_SIZE[1] + FRAME_SIZE[0] / 16) * (n // 10)

    def __get_player_ui_button_pos(self, n: int):

        return self.player_inventory_pos.x + 20 + (
                    FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * n, self.player_inventory_pos.y + 60
