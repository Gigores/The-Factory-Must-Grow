from scripts.UI.Components.BaseUIComponents import *
from scripts.Entities.Buildings.Anvil import Anvil
from scripts.Managers.GameAssets import *
from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.UI.Components.Bg import Bg
from scripts.UI.Entities.BaseUI import BaseUI


class AnvilUI(BaseUI, metaclass=UIRegistry):

    def __init__(self, parent):

        self.main_ui_texture = pg.transform.scale(BLANK, BLANK.get_size())
        self.main_ui_pos = RESOLUTION / Vector(2, 2) - Vector(self.main_ui_texture.get_width(),
                                                              self.main_ui_texture.get_height()) / Vector(2, 2)

        recipe_book_btn_pos = (self.main_ui_pos.x - self.RECIPE_BOOK_SIZE.x * 1.2, self.main_ui_pos.y + BLANK.get_height() / 2 - self.RECIPE_BOOK_SIZE.y / 2)
        super().__init__(parent, recipe_book_pos=recipe_book_btn_pos)
        self.obj = None

        self.sound = pg.mixer.Sound("sound/anvil.mp3")
        self.sound.set_volume(0.5)

        self.player_inventory_pos = Vector(RESOLUTION.x / 2 - BLANK_WIDE.get_width() / 2,
                                           self.main_ui_pos.y + self.main_ui_texture.get_height() - 50)
        self.player_inventory_buttons = []
        for n in range(len(self.parent.inventory)):
            pos = self.__get_player_ui_button_pos(n)
            self.player_inventory_buttons.append(Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, pos))

        forge_btn_size = (FRAME_SIZE[0] * 1.5, FRAME_SIZE[1])
        forge_btn_pos = (self.main_ui_pos.x + self.main_ui_texture.get_width() / 2 - forge_btn_size[0] / 2,
                         self.main_ui_pos.y + self.main_ui_texture.get_height() / 2 - forge_btn_size[1] / 2 - 30)
        self.forge_btn = Button(BUTTON, BUTTON_PRESSED, "Forge", forge_btn_size, forge_btn_pos)

        self.ingredient_slot_data = (None, 0)
        self.result_slot_data = (None, 0)
        self.ingredient_slot_pos = (forge_btn_pos[0] - FRAME_SIZE[0] * 1.5, forge_btn_pos[1])
        self.result_slot_pos = (forge_btn_pos[0] + forge_btn_size[0] + FRAME_SIZE[0] * 0.5, forge_btn_pos[1])
        self.ingredient_slot_button = Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, self.ingredient_slot_pos)
        self.result_slot_button = Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, self.result_slot_pos)

        self.bg = Bg()
        self.bg.blit(self.main_ui_texture, self.main_ui_pos.as_tuple())
        self.bg.blit(FONT.render("Anvil", True, "#757575"),
                    (self.main_ui_pos.x + 20, self.main_ui_pos.y + 20))
        self.bg.blit(BLANK_WIDE, self.player_inventory_pos.as_tuple())
        self.bg.blit(FONT.render("Inventory", True, "#757575"),
                    (self.player_inventory_pos.x + 20, self.player_inventory_pos.y + 20))

        self.recipies_texture = pg.transform.scale(BLANK, self.main_ui_texture.get_size())
        self.recipies_pos = self.main_ui_pos.as_tuple()

        self.recipies_texture.blit(FONT.render("Anvil Recipes", True, "#757575"), (20, 20))

        self.current_book_recipie = None

        self.recipe_window_pos = Vector(self.recipies_pos[0] + 20, self.recipies_pos[1] + self.recipies_texture.get_height() * 0.9)
        border = FRAME_SIZE[0] / 3
        self.recipe_window_size = Vector(FRAME_SIZE[0] * 3 + border * 2 + border * 0.5, FRAME_SIZE[1] + border * 3)
        self.recipe_window_texture = pg.transform.scale(BLANK, self.recipe_window_size.as_tuple())

        self.arrow_center_pos = self.recipe_window_pos + Vector(border * 2, border) + Vector(FRAME_SIZE[0] * 1.5, FRAME_SIZE[1] * 0.5)
        self.arrow_polugon = ([self.arrow_center_pos.x - FRAME_SIZE[0]/2, self.arrow_center_pos.y - FRAME_SIZE[0]/4], [self.arrow_center_pos.x - FRAME_SIZE[0]/2, self.arrow_center_pos.y + FRAME_SIZE[0]/4], [self.arrow_center_pos.x + FRAME_SIZE[0]/2 - border, self.arrow_center_pos.y])

        self.recipe_buttons = []

        pos = from_iterable(self.recipies_pos) + Vector(15, 60)
        for i, recipe in enumerate(anvil_recipies):

            button_texture = pg.Surface(SMALL_FRAME_SIZE)
            button_texture.fill("#a2a2a2")
            draw_item(button_texture, recipe.result[0], 1, (0, 0), SMALL_FRAME_SIZE)

            btn = Button(button_texture, None, "", SMALL_FRAME_SIZE, pos.as_tuple())

            self.recipe_buttons.append(btn)

            if i % 7 >= 6:
                pos.x = self.recipies_pos[0] + 15
                pos.y += SMALL_FRAME_SIZE[1] + 10
            else :
                pos += Vector(SMALL_FRAME_SIZE[0] + 10, 0)

        self.exmpl_ingredient_pos = self.recipe_window_pos + Vector(border, border) + Vector(border * 0.5, 0)
        self.exmpl_ingredient_button = Button(TEXTUTURE_NULL, TEXTUTURE_NULL, "NULL", FRAME_SIZE, self.exmpl_ingredient_pos.as_tuple())
        self.exmpl_result_pos = self.recipe_window_pos + Vector(border, border) + Vector(FRAME_SIZE[0] * 2, 0) + Vector(border * 0.5, 0)
        self.exmpl_result_button = Button(TEXTUTURE_NULL, TEXTUTURE_NULL, "NULL", FRAME_SIZE, self.exmpl_result_pos.as_tuple())

    def events(self, events):

        pass

    def slot_shift(self, slot):

        if self.parent.inventory.can_fit(slot.item_name, slot.item_amount):
            self.parent.inventory.append(slot.item_name, slot.item_amount)
            slot.clear()

    def inventory_shift(self, inventory, button_id):

        item_name = inventory.n[button_id]
        item_amount = inventory.a[button_id]
        if not inventory.n[button_id] is None:
            if self.obj.ingredient_slot.item_name == item_name or self.obj.ingredient_slot.item_name is None:
                if self.obj.ingredient_slot.item_amount + item_amount <= items[item_name].stack_size:
                    inventory.pop_from_slot(button_id, item_amount)
                    self.obj.ingredient_slot.append(item_name, item_amount)

    def update(self, obj: Anvil):

        self.obj = obj

        self.update_recipe_book_btn()

        if self.recipies_opened:

            for i, button in enumerate(self.recipe_buttons):
                button.update()

                if button.touching:
                    self._draw_item_information(anvil_recipies[i].result[0])
                if button.just_pressed:
                    self.current_book_recipie = anvil_recipies[i]

            if self.current_book_recipie:

                self.exmpl_ingredient_button.update()
                self.exmpl_result_button.update()

                if self.exmpl_ingredient_button.touching:
                    self._draw_item_information(self.current_book_recipie.ingredient[0])
                if self.exmpl_result_button.touching:
                    self._draw_item_information(self.current_book_recipie.result[0])

        else:

            self.forge_btn.update()

            if self.forge_btn.just_pressed:
                recipe = anvil_recipies.find(obj.ingredient_slot.item_name)
                if recipe:
                    self.sound.stop()
                    self.sound.play()
                    if obj.result_slot.can_fit(recipe.result[0], recipe.result[1]) and obj.ingredient_slot.item_amount >= recipe.ingredient[1]:
                        obj.ingredient_slot.pop(recipe.ingredient[1])
                        obj.result_slot.append(recipe.result[0], recipe.result[1])
            self._handle_slot(obj.ingredient_slot, self.ingredient_slot_button, self.slot_shift)
            self._handle_slot(obj.result_slot, self.result_slot_button, self.slot_shift, output_only=True)
            self._handle_inventory(self.parent.inventory, self.player_inventory_buttons, self.inventory_shift)
            self.ingredient_slot_data = (obj.ingredient_slot.item_name, obj.ingredient_slot.item_amount)
            self.result_slot_data = (obj.result_slot.item_name, obj.result_slot.item_amount)

    def draw(self, display):

        self.draw_recipe_book_btn()

        if self.recipies_opened:

            display.blit(self.recipies_texture, self.recipies_pos)

            for button in self.recipe_buttons:
                button.draw()

            if self.current_book_recipie:
                display.blit(self.recipe_window_texture, self.recipe_window_pos.as_tuple())
                pg.draw.polygon(display, "#757575", self.arrow_polugon)
                draw_item(display, self.current_book_recipie.ingredient[0], self.current_book_recipie.ingredient[1], self.exmpl_ingredient_pos.as_tuple(), FRAME_SIZE, SMALL_FONT)
                draw_item(display, self.current_book_recipie.result[0], self.current_book_recipie.result[1], self.exmpl_result_pos.as_tuple(), FRAME_SIZE, SMALL_FONT)

        else:

            self.bg.draw()
            for n, (item, amount) in enumerate(zip(self.parent.inventory.n, self.parent.inventory.a)):
                pos = self.__get_player_ui_button_pos(n)
                draw_item(screen, item, amount, pos, FRAME_SIZE)
            self.forge_btn.draw()
            draw_item(screen, self.ingredient_slot_data[0], self.ingredient_slot_data[1], self.ingredient_slot_pos, FRAME_SIZE)
            draw_item(screen, self.result_slot_data[0], self.result_slot_data[1], self.result_slot_pos, FRAME_SIZE)

        self.draw_cursor_slot()

    def __get_player_ui_button_pos(self, n: int):

        return self.player_inventory_pos.x + 20 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * n, self.player_inventory_pos.y + 60

    def when_opened(self):

        self.current_book_recipie = None
        self.recipies_opened = False
