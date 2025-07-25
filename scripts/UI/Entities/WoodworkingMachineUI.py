from scripts.UI.Components.BaseUIComponents import *
from scripts.Entities.Buildings.WoodworkingMachine import WoodworkingMachine
from scripts.Managers.GameAssets import *
from scripts.UI.Components.Bg import Bg
from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.UI.Entities.BaseUI import BaseUI


class WoodworkingMachineUI(BaseUI, metaclass=UIRegistry):

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

        crush_btn_size = (FRAME_SIZE[0] * 1.5, FRAME_SIZE[1])
        crush_btn_pos = (self.main_ui_pos.x + self.main_ui_texture.get_width() / 2 - crush_btn_size[0] / 2,
                         self.main_ui_pos.y + self.main_ui_texture.get_height() / 2 - crush_btn_size[1] / 2 - 30)
        self.crush_btn = Button(BUTTON, BUTTON_PRESSED, "Crush", crush_btn_size, crush_btn_pos)

        self.ing_slot_data = (None, 0)
        self.res_slot_data = (None, 0)
        self.ing_slot_pos = (crush_btn_pos[0] - FRAME_SIZE[0] * 1.5, crush_btn_pos[1])
        self.res_slot_pos = (crush_btn_pos[0] + crush_btn_size[0] + FRAME_SIZE[0] * 0.5, crush_btn_pos[1])
        self.ing_slot_button = Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, self.ing_slot_pos)
        self.res_slot_button = Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, self.res_slot_pos)

        self.bar_rect = pg.Rect(crush_btn_pos[0], crush_btn_pos[1], crush_btn_size[0], crush_btn_size[1])
        self.slider_rect = pg.Rect(self.bar_rect.x, self.bar_rect.y, 0, self.bar_rect.height)

        arrow_point = (
            (self.bar_rect.width, 0),
            (self.bar_rect.width, self.bar_rect.height),
            (self.bar_rect.width - self.bar_rect.width * 0.4, self.bar_rect.height),
            (self.bar_rect.width, self.bar_rect.height / 2),
            (self.bar_rect.width - self.bar_rect.width * 0.4, 0),
        )
        arrow_rect_top = pg.Rect(0, 0, self.bar_rect.width * 0.6, self.bar_rect.height / 4)
        arrow_rect_bottom = pg.Rect(0, self.bar_rect.height * 0.75, self.bar_rect.width * 0.6, self.bar_rect.height / 4)

        self.arrow_mask = pg.Surface(self.bar_rect.size)
        self.arrow_mask.fill("#ab1111")
        pg.draw.polygon(self.arrow_mask, "#a2a2a2", arrow_point)
        pg.draw.rect(self.arrow_mask, "#a2a2a2", arrow_rect_top)
        pg.draw.rect(self.arrow_mask, "#a2a2a2", arrow_rect_bottom)
        self.arrow_mask.set_colorkey("#ab1111")

        self.bg = Bg()
        self.bg.blit(self.main_ui_texture, self.main_ui_pos.as_tuple())
        self.bg.blit(FONT.render("Woodworking Machine", True, "#757575"),
                     (self.main_ui_pos.x + 20, self.main_ui_pos.y + 20))
        self.bg.blit(BLANK_WIDE, self.player_inventory_pos.as_tuple())
        self.bg.blit(FONT.render("Inventory", True, "#757575"),
                     (self.player_inventory_pos.x + 20, self.player_inventory_pos.y + 20))

    def ing_slot_shift(self, slot):

        if self.parent.inventory.can_fit(slot.item_name, slot.item_amount):
            self.parent.inventory.append(slot.item_name, slot.item_amount)
            slot.pop(slot.item_amount)

    def res_slot_shift(self, slot):

        if self.parent.inventory.can_fit(slot.item_name, slot.item_amount):
            self.parent.inventory.append(slot.item_name, slot.item_amount)
            slot.pop(slot.item_amount)

    def inventory_shift(self, inventory, button_id):

        item_name = inventory.n[button_id]
        item_amount = inventory.a[button_id]
        if not inventory.n[button_id] is None:
            if self.obj.ing_slot.item_name == item_name or self.obj.ing_slot.item_name is None:
                if self.parent.shift_pressed:
                    # if items[item_name].stack_size - obj.ingredient_slot.item_amount > item_amount:
                    if self.obj.ing_slot.item_amount + item_amount <= items[item_name].stack_size:
                        self.parent.inventory.pop_from_slot(button_id, item_amount)
                        self.obj.ing_slot.append(item_name, item_amount)
                else:
                    if self.obj.ing_slot.item_amount < items[item_name].stack_size:
                        self.parent.inventory.pop_from_slot(button_id, 1)
                        self.obj.ing_slot.append(item_name, 1)

    def update(self, obj: WoodworkingMachine):

        self.obj = obj

        try:
            self.slider_rect.width = obj.progress * self.bar_rect.width / obj.max_progress
        except ZeroDivisionError:
            self.slider_rect.width = 0

        self._handle_slot(obj.ing_slot, self.ing_slot_button, self.ing_slot_shift)
        self._handle_slot(obj.res_slot, self.res_slot_button, self.res_slot_shift, output_only=True)
        self._handle_inventory(self.parent.inventory, self.player_inventory_buttons, self.inventory_shift)

        self.ing_slot_data = (obj.ing_slot.item_name, obj.ing_slot.item_amount)
        self.res_slot_data = (obj.res_slot.item_name, obj.res_slot.item_amount)

    def draw(self, display):

        self.bg.draw()

        for n, (item, amount) in enumerate(zip(self.parent.inventory.n, self.parent.inventory.a)):
            pos = self.__get_player_ui_button_pos(n)
            draw_item(screen, item, amount, pos, FRAME_SIZE)
        #self.crush_btn.draw()
        draw_item(screen, self.ing_slot_data[0], self.ing_slot_data[1], self.ing_slot_pos,
                  FRAME_SIZE)
        draw_item(screen, self.res_slot_data[0], self.res_slot_data[1], self.res_slot_pos, FRAME_SIZE)

        pg.draw.rect(screen, "#222222", self.bar_rect)
        pg.draw.rect(screen, "#ddcc00", self.slider_rect)
        screen.blit(self.arrow_mask, (self.bar_rect.x, self.bar_rect.y))

        self.draw_cursor_slot()

    def events(self, events):

        pass

    def __get_player_ui_button_pos(self, n: int):

        return self.player_inventory_pos.x + 20 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * n, self.player_inventory_pos.y + 60
