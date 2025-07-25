from scripts.UI.Components.BaseUIComponents import *
from scripts.Entities.Buildings.Furniture import BedsideTable
from scripts.Managers.GameAssets import *
from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.UI.Components.Bg import Bg
from scripts.UI.Entities.BaseUI import BaseUI


class BedsideTableUI(BaseUI, metaclass=UIRegistry):

    def __init__(self, parent):

        super().__init__(parent)
        self.obj = None

        self.main_ui_texture = pg.transform.scale(BLANK, BLANK.get_size())
        self.main_ui_pos = RESOLUTION / Vector(2, 2) - Vector(self.main_ui_texture.get_width(),
                                                              self.main_ui_texture.get_height()) / Vector(2, 2)

        self.player_inventory_pos = Vector(RESOLUTION.x / 2 - BLANK_WIDE.get_width() / 2,
                                           self.main_ui_pos.y + self.main_ui_texture.get_height() - 50)
        self.player_inventory_buttons = []
        for n in range(len(self.parent.inventory)):
            pos = self.__get_player_ui_button_pos(n)
            self.player_inventory_buttons.append(Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, pos))
        self.inventory = None

        self.inventory_pos = self.main_ui_pos + Vector(BLANK.get_width() / 2 - (FRAME_SIZE[0] * 5 + 20) / 2,
                                                       BLANK.get_height() / 2 - FRAME_SIZE[1] / 2)
        self.inventory_buttons = []
        for n in range(5):
            pos = self.__get_inventory_button_pos(n).as_tuple()
            self.inventory_buttons.append(Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, pos))

        self.bg = Bg()
        self.bg.blit(self.main_ui_texture, self.main_ui_pos.as_tuple())
        self.bg.blit(FONT.render("Bedside Table", True, "#757575"),
                     (self.main_ui_pos.x + 20, self.main_ui_pos.y + 20))
        self.bg.blit(BLANK_WIDE, self.player_inventory_pos.as_tuple())
        self.bg.blit(FONT.render("Inventory", True, "#757575"),
                     (self.player_inventory_pos.x + 20, self.player_inventory_pos.y + 20))

    def inventory_shift(self, inventory, button_id):

        item_name = inventory.n[button_id]
        item_amount = inventory.a[button_id]
        if self.parent.inventory.can_fit(item_name, item_amount):
            inventory.pop_from_slot(button_id, item_amount)
            self.parent.inventory.append(item_name, item_amount)

    def player_inventory_shift(self, inventory, button_id):

        item_name = inventory.n[button_id]
        item_amount = inventory.a[button_id]
        if self.obj.inventory.can_fit(item_name, item_amount):
            inventory.pop_from_slot(button_id, item_amount)
            self.obj.inventory.append(item_name, item_amount)

    def update(self, obj: BedsideTable):

        self.obj = obj
        self.inventory = obj.inventory

        self._handle_inventory(self.inventory, self.inventory_buttons, self.inventory_shift)
        """
        for n, btn in enumerate(self.inventory_buttons):
            btn.update()
            if btn.just_pressed and self.inventory.n[n]:
                item_name = self.inventory.n[n]
                item_amount = self.inventory.a[n] if self.parent.shift_pressed else 1
                if self.parent.inventory.can_fit(item_name, item_amount):
                    obj.inventory.pop_from_slot(n, item_amount)
                    self.parent.inventory.append(item_name, item_amount)
            if btn.touching and self.inventory.n[n]:
                pos = (get_mouse_pos()[0] + TEXT_MOUSE_OFFSET[0], get_mouse_pos()[1] + TEXT_MOUSE_OFFSET[1])
                print_data(screen, pos, items[self.inventory.n[n]].name)
        """
        self._handle_inventory(self.parent.inventory, self.player_inventory_buttons, self.player_inventory_shift)
        """
        for n, btn in enumerate(self.player_inventory_buttons):
            btn.update()
            if btn.just_pressed and self.parent.inventory.n[n]:
                item_name = self.parent.inventory.n[n]
                item_amount = self.parent.inventory.a[n] if self.parent.shift_pressed else 1
                if obj.inventory.can_fit(item_name, item_amount):
                    self.parent.inventory.pop_from_slot(n, item_amount)
                    obj.inventory.append(item_name, item_amount)
            if btn.touching and self.parent.inventory.n[n]:
                pos = (get_mouse_pos()[0] + TEXT_MOUSE_OFFSET[0], get_mouse_pos()[1] + TEXT_MOUSE_OFFSET[1])
                print_data(screen, pos, items[self.parent.inventory.n[n]].name)
        """

    def draw(self, display):

        self.bg.draw()

        for n, (item, amount) in enumerate(zip(self.parent.inventory.n, self.parent.inventory.a)):
            pos = self.__get_player_ui_button_pos(n)
            draw_item(screen, item, amount, pos, FRAME_SIZE)
        if self.inventory:
            for n, (item, amount) in enumerate(zip(self.inventory.n, self.inventory.a)):
                pos = self.__get_inventory_button_pos(n).as_tuple()
                draw_item(screen, item, amount, pos, FRAME_SIZE)

        self.draw_cursor_slot()

    def events(self, events):

        pass

    def __get_player_ui_button_pos(self, n: int):

        return self.player_inventory_pos.x + 20 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * n, self.player_inventory_pos.y + 60

    def __get_inventory_button_pos(self, n: int):

        return self.inventory_pos + from_iterable(FRAME_SIZE) * Vector(n, 0) + Vector(5 * n, 0)
