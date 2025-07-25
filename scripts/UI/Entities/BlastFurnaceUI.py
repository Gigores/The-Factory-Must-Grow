from scripts.UI.Components.BaseUIComponents import *
from scripts.Entities.Buildings.BlastFurnace import BlastFurnace
from scripts.Managers.GameAssets import *
from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.UI.Components.Bg import Bg
from scripts.UI.Entities.BaseUI import BaseUI


class BlastFurnaceUI(BaseUI, metaclass=UIRegistry):

    def __init__(self, parent):

        super().__init__(parent)
        self.obj = None

        self.main_ui_size = from_iterable(BLANK.get_size())*Vector(1, 1.5)
        self.main_ui_texture = pg.transform.scale(BLANK, self.main_ui_size.as_tuple())
        self.main_ui_pos = RESOLUTION / Vector(2, 2) - Vector(self.main_ui_size.x, self.main_ui_size.y) / Vector(2, 2)

        self.player_inventory_pos = Vector(RESOLUTION.x / 2 - BLANK_WIDE.get_width() / 2,
                                           self.main_ui_pos.y + self.main_ui_texture.get_height() - 50)
        self.player_inventory_buttons = []
        for n in range(len(self.parent.inventory)):
            pos = self.__get_player_ui_button_pos(n)
            self.player_inventory_buttons.append(Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, pos))

        self.eng1_pos = self.main_ui_pos + (from_iterable(FRAME_SIZE) * Vector(0.45, 1))
        self.eng1_data = (None, 0)
        self.eng1_btn = Button(BUTTON, None, "", FRAME_SIZE, self.eng1_pos.as_tuple())

        self.eng2_pos = self.main_ui_pos + (from_iterable(FRAME_SIZE) * Vector(1.55, 1))
        self.eng2_data = (None, 0)
        self.eng2_btn = Button(BUTTON, None, "", FRAME_SIZE, self.eng2_pos.as_tuple())

        self.fuel_pos = self.main_ui_pos + (from_iterable(FRAME_SIZE) * Vector(1, 4))
        self.fuel_data = (None, 0)
        self.fuel_btn = Button(BUTTON, None, "", FRAME_SIZE, self.fuel_pos.as_tuple())

        self.res_pos = self.main_ui_pos + (from_iterable(FRAME_SIZE) * Vector(4, 4))
        self.res_data = (None, 0)
        self.res_btn = Button(BUTTON, None, "", FRAME_SIZE, self.res_pos.as_tuple())

        self.firebox_size = from_iterable(FIREBOX[0].get_size())
        self.firebox_pos = Vector(self.fuel_pos.x + FRAME_SIZE[0] / 2 - self.firebox_size.x / 2, self.eng1_pos.y + (self.fuel_pos.y - self.eng1_pos.y) / 2)
        self.firebox_id = 0

        self.arrow_width = 30
        self.arrow_rect1 = pg.Rect(self.eng2_pos.x + FRAME_SIZE[0] * 1.5,
                                   self.eng2_pos.y + FRAME_SIZE[1] / 2 - self.arrow_width / 2,
                                   (self.res_pos.x + FRAME_SIZE[0] / 2 + self.arrow_width / 2) - (self.eng2_pos.x + FRAME_SIZE[0] * 1.5),
                                   self.arrow_width)
        self.filling_rect1 = pg.Rect(self.arrow_rect1.x, self.arrow_rect1.y, 0, self.arrow_rect1.height)
        self.arrow_rect2 = pg.Rect(self.arrow_rect1.x + self.arrow_rect1.width - self.arrow_width * 1.5,
                                   self.arrow_rect1.y + self.arrow_rect1.height,
                                   self.arrow_width * 2,
                                   self.arrow_rect1.width)
        self.filling_rect2 = pg.Rect(self.arrow_rect2.x, self.arrow_rect2.y, self.arrow_rect2.width, 0)
        self.arrow_mask = pg.Surface(self.arrow_rect2.size)
        self.arrow_mask.fill("#000000")
        pg.draw.rect(self.arrow_mask, "#A2A2A2", (0, 0, self.arrow_width * 0.5, self.arrow_rect2.height * 0.75))
        pg.draw.rect(self.arrow_mask, "#A2A2A2", (self.arrow_width * 1.5, 0, self.arrow_width * 0.5, self.arrow_rect2.height * 0.75))
        pg.draw.polygon(self.arrow_mask, "#A2A2A2", ((0, self.arrow_rect2.height * 0.75), (0, self.arrow_rect2.height), (self.arrow_rect2.width / 2, self.arrow_rect2.height)))
        pg.draw.polygon(self.arrow_mask, "#A2A2A2", ((self.arrow_rect2.width, self.arrow_rect2.height * 0.75), (self.arrow_rect2.width, self.arrow_rect2.height), (self.arrow_rect2.width / 2, self.arrow_rect2.height)))
        self.arrow_mask.set_colorkey("#000000")

        self.bg = Bg()
        self.bg.blit(self.main_ui_texture, self.main_ui_pos.as_tuple())
        self.bg.blit(FONT.render("Blast Furnace", True, "#757575"), (self.main_ui_pos.x + 30, self.main_ui_pos.y + 20))
        self.bg.blit(BLANK_WIDE, self.player_inventory_pos.as_tuple())
        self.bg.blit(FONT.render("Inventory", True, "#757575"), (self.player_inventory_pos.x + 30, self.player_inventory_pos.y + 20))

    def slot_shift(self, slot):

        item_amount = slot.item_amount
        if self.parent.inventory.can_fit(slot.item_name, item_amount):
            self.parent.inventory.append(slot.item_name, item_amount)
            slot.clear()

    def inventory_shift(self, inventory, button_id):

        item_name = inventory.n[button_id]
        item_amount = inventory.a[button_id]
        if self.obj.can_insert(item_name, item_amount):
            self.obj.insert(item_name, item_amount)
            self.parent.inventory.pop_from_slot(button_id, item_amount)

    def update(self, obj: BlastFurnace):

        self.obj = obj

        self._handle_inventory(self.parent.inventory, self.player_inventory_buttons, self.inventory_shift)

        if obj.fuel_left == 0: self.firebox_id = 0
        else: self.firebox_id = int(3 * obj.fuel_left / obj.fuel_start_amount) + 1

        self.eng1_data = obj.eng1_slot.item_name, obj.eng1_slot.item_amount
        self.eng2_data = obj.eng2_slot.item_name, obj.eng2_slot.item_amount
        self.fuel_data = obj.fuel_slot.item_name, obj.fuel_slot.item_amount
        self.res_data = obj.res_slot.item_name, obj.res_slot.item_amount

        self._handle_slot(obj.eng1_slot, self.eng1_btn, self.slot_shift)
        self._handle_slot(obj.eng2_slot, self.eng2_btn, self.slot_shift)
        self._handle_slot(obj.fuel_slot, self.fuel_btn, self.slot_shift)
        self._handle_slot(obj.res_slot, self.res_btn, self.slot_shift, output_only=True)

        if obj.progress_left > 1200:
            try: self.filling_rect1.width = (self.arrow_rect1.width - (obj.progress_left * self.arrow_rect1.width / 2400)) * 2
            except ZeroDivisionError: self.filling_rect1.width = self.arrow_rect1.width
        elif obj.progress_left == 0:
            self.filling_rect1.width = 0
        else:
            self.filling_rect1.width = self.arrow_rect1.width


        if obj.progress_left == 0:
            self.filling_rect2.height = 0
        elif obj.progress_left < 1200:
            try: self.filling_rect2.height = (self.arrow_rect2.height - (obj.progress_left * self.arrow_rect2.height / 2400)) * 2 - self.arrow_rect2.height
            except ZeroDivisionError: self.filling_rect2.height = self.arrow_rect2.height
        else:
            self.filling_rect2.height = 0

    def draw(self, display):

        self.bg.draw()

        for n, (item, amount) in enumerate(zip(self.parent.inventory.n, self.parent.inventory.a)):
            pos = self.__get_player_ui_button_pos(n)
            draw_item(screen, item, amount, pos, FRAME_SIZE)

        draw_item(screen, self.eng1_data[0], self.eng1_data[1], self.eng1_pos.as_tuple(), FRAME_SIZE, placeholder_item="coal")
        draw_item(screen, self.eng2_data[0], self.eng2_data[1], self.eng2_pos.as_tuple(), FRAME_SIZE, placeholder_item="crushed_refined_raw_iron")
        draw_item(screen, self.fuel_data[0], self.fuel_data[1], self.fuel_pos.as_tuple(), FRAME_SIZE, placeholder_item="coking_coal")
        draw_item(screen, self.res_data[0], self.res_data[1], self.res_pos.as_tuple(), FRAME_SIZE)

        pg.draw.rect(self.bg, "#222222", self.arrow_rect1)
        pg.draw.rect(self.bg, "#222222", self.arrow_rect2)
        pg.draw.rect(self.bg, "#ddcc00", self.filling_rect1)
        pg.draw.rect(self.bg, "#ddcc00", self.filling_rect2)
        self.bg.blit(self.arrow_mask, (self.arrow_rect2.x, self.arrow_rect2.y))

        screen.blit(FIREBOX[self.firebox_id], self.firebox_pos.as_tuple())

        self.draw_cursor_slot()

    def events(self, events):

        pass

    def __get_player_ui_button_pos(self, n: int):

        return self.player_inventory_pos.x + 20 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * n, self.player_inventory_pos.y + 60
