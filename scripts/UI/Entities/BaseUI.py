from scripts.constants import *
from scripts.UI.Components.BaseUIComponents import *
from scripts.Managers.GameAssets import *
from scripts.Managers.IngameManagers.InventoryLiquids import InventoryTank
from scripts.Managers.IngameManagers.Inventory import *
from scripts.Managers.GameAssets import ITEM_TO_LIQUID, LIQUID_TO_ITEM
from copy import copy
from math import sin


class BaseUI:

    RECIPE_BOOK_SIZE = TILE_SIZE * Vector(2, 2)
    RECIPE_BOOK_TEXTURE = pg.transform.scale(pg.image.load("assets/ingame_UI/recipe_book.png"), RECIPE_BOOK_SIZE.as_tuple())

    def __init__(self, parent, recipe_book_pos=(0, 0)):

        self.parent = parent

        self.mouse_slot = [None, 0]

        self.recipe_book_btn = Button(self.RECIPE_BOOK_TEXTURE, self.RECIPE_BOOK_TEXTURE, "",
                                      self.RECIPE_BOOK_SIZE.as_tuple(), recipe_book_pos)
        self.recipies_opened = False

        self.tooltip = Text(Vector(1, 1), "<col hex='FF0000'>shanik go fuck yourself", font=FONT)

    def draw_recipe_book_btn(self):

        self.recipe_book_btn.draw()

    def update_recipe_book_btn(self):

        self.recipe_book_btn.update()
        if self.recipe_book_btn.just_pressed:
            self.recipies_opened = not self.recipies_opened
        if self.recipe_book_btn.touching:
            self._draw_text_information("Recipies")

    def handle_events_recipe_book(self, events):

        pass

    def _draw_item_info(self, button, text):

        if button.touching and text:
            self._draw_item_information(text)

    def _draw_tank_info(self, rect, tank):

        if rect.collidepoint(get_mouse_pos()) and tank.current_liquid:
            self._draw_liquid_information(tank)

    def _draw_liquid(self, rect: pg.Rect, tank: InventoryTank):

        if tank.current_liquid:

            color = liquids[tank.current_liquid]["color"]
            gas = liquids[tank.current_liquid]["gas"]
            fill_percentage = tank.get_fill_percentage()

            y_level = (rect.h / 100) * fill_percentage

            rect_pos = Vector(rect.x, rect.y)

            jiggle_range = 3
            if gas:
                fill_point_left = rect_pos + Vector(0, y_level + sin(self.parent.animation_counter / 10) * jiggle_range)
                fill_point_semileft = rect_pos + Vector(rect.w * 0.25, y_level + sin(self.parent.animation_counter / 10 + 5) * jiggle_range)
                fill_point = rect_pos + Vector(rect.w * 0.5, y_level + sin(self.parent.animation_counter / 10 + 10) * jiggle_range)
                fill_point_semiright = rect_pos + Vector(rect.w * 0.75, y_level + sin(self.parent.animation_counter / 10 + 15) * jiggle_range)
                fill_point_right = rect_pos + Vector(rect.w, y_level + sin(self.parent.animation_counter / 10 + 20) * jiggle_range)
            else:
                fill_point_left = rect_pos + Vector(0, rect.h) - Vector(0, y_level + sin(self.parent.animation_counter / 10) * jiggle_range)
                fill_point_semileft = rect_pos + Vector(rect.w * 0.25, rect.h) - Vector(0, y_level + sin(self.parent.animation_counter / 10 + 5) * jiggle_range)
                fill_point = rect_pos + Vector(rect.w * 0.5, rect.h) - Vector(0, y_level + sin(self.parent.animation_counter / 10 + 10) * jiggle_range)
                fill_point_semiright = rect_pos + Vector(rect.w * 0.75, rect.h) - Vector(0, y_level + sin(self.parent.animation_counter / 10 + 15) * jiggle_range)
                fill_point_right = rect_pos + Vector(rect.w, rect.h) - Vector(0, y_level + sin(self.parent.animation_counter / 10 + 20) * jiggle_range)

            bottom_left = rect_pos + Vector(0, rect.h * int(not gas))
            bottom_right = rect_pos + Vector(rect.w, rect.h * int(not gas))

            pg.draw.polygon(screen, color, [fill_point_left.as_tuple(), fill_point_semileft.as_tuple(), fill_point.as_tuple(), fill_point_semiright.as_tuple(), fill_point_right.as_tuple(), bottom_right.as_tuple(), bottom_left.as_tuple()])

    def _handle_inventory(self, inventory, buttons, when_shift, custom_draw_info_method=None, output_only=False):

        if custom_draw_info_method is None:
            draw_info_method = self._draw_item_info
        else:
            draw_info_method = custom_draw_info_method

        for button_id, button in enumerate(buttons):
            button.update()
            if button.just_pressed:
                if self.parent.shift_pressed and inventory.a[button_id] > 0:
                    when_shift(inventory, button_id)
                else:
                    self._handle_slot_interaction(
                        inventory.n[button_id],
                        inventory.a[button_id],
                        lambda: inventory.pop_from_slot(button_id, 1),
                        lambda name: self._set_name_inventory(inventory, button_id, name),
                        lambda amount: self._set_amount_inventory(inventory, button_id, amount),
                        output_only=output_only
                    )

            draw_info_method(button, inventory.n[button_id])

    def _handle_slot(self, slot, button, when_shift, *, output_only=False, custom_draw_info_method=None):

        if custom_draw_info_method is None:
            draw_info_method = self._draw_item_info
        else:
            draw_info_method = custom_draw_info_method

        button.update()

        if button.just_pressed:
            if self.parent.shift_pressed and slot.item_amount > 0:
                when_shift(slot)
            else:
                self._handle_slot_interaction(
                    slot.item_name,
                    slot.item_amount,
                    lambda: slot.pop(1),
                    lambda name: self._set_name_slot(slot, name),
                    lambda amount: self._set_amount_slot(slot, amount),
                    output_only
                )

        draw_info_method(button, slot.item_name)

    def _handle_slot_interaction(self, item_name, item_amount, pop_item, set_name, set_amount, output_only=False):

        if self.parent.ctrl_pressed:
            if (item_name == self.mouse_slot[0] or self.mouse_slot[0] is None) and item_amount > 0:
                if self.mouse_slot[0]:
                    if items[self.mouse_slot[0]].stack_size > self.mouse_slot[1]:
                        self.mouse_slot[0] = item_name
                        pop_item()
                        self.mouse_slot[1] += 1
                else:
                    self.mouse_slot[0] = item_name
                    pop_item()
                    self.mouse_slot[1] += 1
        else:
            if self.mouse_slot[0] == item_name and item_amount > 0:
                if self.parent.ctrl_pressed:
                    if item_amount < items[item_name].stack_size and not output_only:
                        set_amount(item_amount + 1)
                        self.mouse_slot[1] -= 1
                else:
                    item_amount = set_amount(item_amount + self.mouse_slot[1])
                    self.mouse_slot[1] = 0
                    if item_amount > items[item_name].stack_size:
                        self.mouse_slot[1] = item_amount - items[item_name].stack_size
                        set_amount(items[item_name].stack_size)
                if self.mouse_slot[1] == 0:
                    self.mouse_slot[0] = None
            else:
                if not output_only or item_amount > 0:
                    new_item_name = item_name
                    new_item_amount = item_amount

                    set_name(self.mouse_slot[0])
                    set_amount(self.mouse_slot[1])

                    self.mouse_slot[0] = new_item_name
                    self.mouse_slot[1] = new_item_amount

    def draw_cursor_slot(self):

        draw_item(screen, self.mouse_slot[0], self.mouse_slot[1], (from_iterable(get_mouse_pos()) - from_iterable(FRAME_SIZE) * Vector(0.5, 0.5)).as_tuple(), FRAME_SIZE, draw_bg=False)

    def when_opened(self):

        pass

    def _draw_item_information(self, item_name):
        pos = (get_mouse_pos()[0] + TEXT_MOUSE_OFFSET[0], get_mouse_pos()[1] + TEXT_MOUSE_OFFSET[1])
        self.tooltip.tokens = self.tooltip.Lexer(items[item_name].tooltip).tokenize()
        self.tooltip.surface = self.tooltip.update_text_surface()
        print_item_data(screen, pos, items[item_name].name, self.tooltip)

    def _draw_liquid_information(self, tank: InventoryTank):
        pos = (get_mouse_pos()[0] + TEXT_MOUSE_OFFSET[0], get_mouse_pos()[1] + TEXT_MOUSE_OFFSET[1])
        self.tooltip.tokens = self.tooltip.Lexer(liquids[tank.current_liquid]["tooltip"]).tokenize()
        self.tooltip.surface = self.tooltip.update_text_surface()
        print_liquid_data(screen, pos, liquids[tank.current_liquid]["name"], tank.fill_level, tank.max_volume, self.tooltip)

    @staticmethod
    def _draw_text_information(text):
        pos = (get_mouse_pos()[0] + TEXT_MOUSE_OFFSET[0], get_mouse_pos()[1] + TEXT_MOUSE_OFFSET[1])
        print_data(screen, pos, text)

    @staticmethod
    def _set_name_slot(slot, name):
        slot.item_name = name
        return name

    @staticmethod
    def _set_amount_slot(slot, amount):
        slot.item_amount = amount
        return amount

    @staticmethod
    def _set_name_inventory(inventory, slot_id, name):
        inventory.n[slot_id] = name
        return name

    @staticmethod
    def _set_amount_inventory(inventory, slot_id, amount):
        inventory.a[slot_id] = amount
        return amount
