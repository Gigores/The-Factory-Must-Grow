from scripts.UI.Components.BaseUIComponents import *
from scripts.Managers.GameAssets import *
from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.UI.Entities.BaseUI import BaseUI


class WorkbenchUI(BaseUI, metaclass=UIRegistry):

    def __init__(self, parent):

        self.workbench_ui_texture = pg.transform.scale_by(pg.image.load("assets/ingame_UI/workbench_inv.png"), 7)
        self.workbench_pos = (
            RESOLUTION.x / 2 - self.workbench_ui_texture.get_width() / 2,
            RESOLUTION.y / 2 - self.workbench_ui_texture.get_width() / 2
        )
        recipe_book_btn_pos = (self.workbench_pos[0] - self.RECIPE_BOOK_SIZE.x * 1.2, self.workbench_pos[1] + BLANK.get_height() / 2 - self.RECIPE_BOOK_SIZE.y / 2)
        super().__init__(parent, recipe_book_btn_pos)
        self.obj = None

        self.recipies_size = from_iterable(self.workbench_ui_texture.get_size())*Vector(1, 1.5)
        self.recipies_texture = pg.transform.scale(BLANK, self.recipies_size.as_tuple())
        self.recipies_pos = (
            RESOLUTION.x / 2 - self.recipies_size.x / 2,
            RESOLUTION.y / 2 - self.recipies_size.y / 2
        )

        self.recipies_buttons = {}
        self.category_buttons = []

        self.recipes = {submenu: [] for submenu in workbench_recipies.keys()}

        self.current_category = list(self.recipes.keys())[0]
        self.current_book_recipie = None

        for menu in self.recipes.keys():
            for submenu in workbench_recipies[menu]:
                for recipe in workbench_recipies[menu][submenu]:
                    self.recipes[menu].append(recipe)

        for category_name, category in workbench_recipies.items():
            if not (category_name in self.recipies_buttons.keys()):
                self.recipies_buttons[category_name] = list()
            pos = from_iterable(self.recipies_pos) + Vector(20, 90)
            for n, subcategory in enumerate(category.values()):
                for j, recipe in enumerate(subcategory):
                    texture = pg.Surface(SMALL_FRAME_SIZE)
                    texture.fill("#a2a2a2")
                    draw_item(texture, recipe.result[0], 1, (0, 0), SMALL_FRAME_SIZE)

                    btn = Button(texture, None, "", SMALL_FRAME_SIZE, pos.as_tuple())

                    self.recipies_buttons[category_name].append(btn)

                    if j % 8 >= 7:
                        pos.x = self.recipies_pos[0] + 20
                        pos.y += SMALL_FRAME_SIZE[1] + 10
                    else:
                        pos += Vector(SMALL_FRAME_SIZE[0] + 10, 0)

                pos.x = self.recipies_pos[0] + 20
                pos.y += SMALL_FRAME_SIZE[1] + 10

        category_buttons_pos = (self.recipies_pos[0] + 20,
                                self.recipies_pos[1] + 20)
        try:
            category_buttons_size = ((self.recipies_texture.get_width() - 20) / len(self.recipies_buttons.keys()) - 20, 50)
        except ZeroDivisionError:
            category_buttons_size = self.recipies_texture.get_width() - 20

        for n, category_name in enumerate(self.recipies_buttons.keys()):
            pos = (category_buttons_pos[0] + (category_buttons_size[0] + 20) * n,
                   category_buttons_pos[1])
            btn = Button(BUTTON, BUTTON_PRESSED, category_name, category_buttons_size, pos, font=SMALL_FONT)
            self.category_buttons.append(btn)

        self.engredient1_pos = (self.workbench_pos[0] + 247, self.workbench_pos[1] + 150)
        self.engredient2_pos = (self.workbench_pos[0] + 248, self.workbench_pos[1] + 263)
        self.result_pos = (self.workbench_pos[0] + 488, self.workbench_pos[1] + 150)

        self.inventory_pos = (
            RESOLUTION.x / 2 - BLANK_WIDE.get_width() / 2 - 170,
            self.recipies_pos[1] + self.workbench_ui_texture.get_height() * 0.9
        )
        self.inventory_buttons = []
        for i, (n, a) in enumerate(zip(self.parent.inventory.n, self.parent.inventory.a)):

            pos = (self.inventory_pos[0] + 20 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * i, self.inventory_pos[1] + 60)
            btn = Button(BUTTON, None, "", FRAME_SIZE, pos)

            self.inventory_buttons.append(btn)

        craft_button_size = (340, BLANK_WIDE.get_height())
        craft_button_pos = (self.inventory_pos[0] + BLANK_WIDE.get_width() + ELEMENT_SPACING, self.inventory_pos[1])

        self.craft_button = Button(
            RED_BUTTON, RED_BUTTON_PRESSED, "CRAFT", craft_button_size, craft_button_pos, "#dddddd", HUGEISH_FONT
        )

        self.current_recipie = None

        self.bg = pg.Surface(RESOLUTION.as_tuple())

        self.eng1_btn = Button(BUTTON, BUTTON_PRESSED, "", SMALL_FRAME_SIZE, self.engredient1_pos)
        self.eng2_btn = Button(BUTTON, BUTTON_PRESSED, "", SMALL_FRAME_SIZE, self.engredient2_pos)
        self.res_btn = Button(BUTTON, BUTTON_PRESSED, "", SMALL_FRAME_SIZE, self.result_pos)

        # self.bg.blit(self.recipies_texture, self.recipies_pos)
        self.bg.blit(self.workbench_ui_texture, self.workbench_pos)
        # self.bg.blit(FONT.render("Recipies", True, "#757575"), (self.recipies_pos[0] + 20, self.recipies_pos[1] + 70))
        self.bg.blit(BLANK_WIDE, self.inventory_pos)
        self.bg.blit(FONT.render("Inventory", True, "#757575"), (self.inventory_pos[0] + 30, self.inventory_pos[1] + 20))
        self.bg.set_colorkey("#000000")

        # pprint.pprint(self.recipies_buttons)
        # pprint.pprint(self.category_buttons)

        self.recipe_window_pos = Vector(self.recipies_pos[0] + 20, self.recipies_pos[1] + self.recipies_texture.get_height() * 0.9)
        border = FRAME_SIZE[0] / 3
        self.recipe_window_size = Vector(FRAME_SIZE[0] * 4 + border * 2 + border * 0.5, FRAME_SIZE[1] + border * 3)
        self.recipe_window_texture = pg.transform.scale(BLANK, self.recipe_window_size.as_tuple())

        self.exmpl_ingredient_1_pos = self.recipe_window_pos + Vector(border, border)
        self.exmpl_ingredient_1_button = Button(TEXTUTURE_NULL, TEXTUTURE_NULL, "NULL", FRAME_SIZE, self.exmpl_ingredient_1_pos.as_tuple())
        self.exmpl_ingredient_2_pos = self.recipe_window_pos + Vector(border, border) + Vector(FRAME_SIZE[0], 0) + Vector(border * 0.5, 0)
        self.exmpl_ingredient_2_button = Button(TEXTUTURE_NULL, TEXTUTURE_NULL, "NULL", FRAME_SIZE, self.exmpl_ingredient_2_pos.as_tuple())
        self.exmpl_result_pos = self.recipe_window_pos + Vector(border, border) + Vector(FRAME_SIZE[0] * 3, 0) + Vector(border * 0.5, 0)
        self.exmpl_result_button = Button(TEXTUTURE_NULL, TEXTUTURE_NULL, "NULL", FRAME_SIZE, self.exmpl_result_pos.as_tuple())

        self.arrow_center_pos = self.recipe_window_pos + Vector(border * 2, border) + Vector(FRAME_SIZE[0] * 2.5, FRAME_SIZE[1] * 0.5)
        self.arrow_polygon = ([self.arrow_center_pos.x - FRAME_SIZE[0] / 2, self.arrow_center_pos.y - FRAME_SIZE[0] / 4], [self.arrow_center_pos.x - FRAME_SIZE[0] / 2, self.arrow_center_pos.y + FRAME_SIZE[0] / 4], [self.arrow_center_pos.x + FRAME_SIZE[0] / 2 - border, self.arrow_center_pos.y])

    def draw(self, display):

        self.draw_recipe_book_btn()

        if self.recipies_opened:

            display.blit(self.recipies_texture, self.recipies_pos)

            if self.current_book_recipie:
                display.blit(self.recipe_window_texture, self.recipe_window_pos.as_tuple())
                pg.draw.polygon(display, "#757575", self.arrow_polygon)
                draw_item(display, self.current_book_recipie.ingredient1[0], self.current_book_recipie.ingredient1[1], self.exmpl_ingredient_1_pos.as_tuple(), FRAME_SIZE, SMALL_FONT)
                draw_item(display, self.current_book_recipie.ingredient2[0], self.current_book_recipie.ingredient2[1], self.exmpl_ingredient_2_pos.as_tuple(), FRAME_SIZE, SMALL_FONT)
                draw_item(display, self.current_book_recipie.result[0], self.current_book_recipie.result[1], self.exmpl_result_pos.as_tuple(), FRAME_SIZE, SMALL_FONT)

            for btn in self.category_buttons:
                btn.draw()

            for n, button in enumerate(self.recipies_buttons[self.current_category]):
                button.draw()

            #screen.blit(FONT.render("Recipies", True, "#757575"), (self.recipies_pos[0] + 20, self.recipies_pos[1] + 20))
            #screen.blit(BLANK_WIDE, self.inventory_pos)
            #screen.blit(FONT.render("Inventory", True, "#757575"), (self.inventory_pos[0] + 30, self.inventory_pos[1] + 20))

        else:

            self.craft_button.draw()

            screen.blit(self.bg, (0, 0))

            if self.obj:
                draw_item(screen, self.obj.ing1_slot.item_name, self.obj.ing1_slot.item_amount,
                          self.engredient1_pos, SMALL_FRAME_SIZE, SMALL_FONT, draw_bg=False)
                draw_item(screen, self.obj.ing2_slot.item_name, self.obj.ing2_slot.item_amount,
                          self.engredient2_pos, SMALL_FRAME_SIZE, SMALL_FONT, draw_bg=False)

                item_placeholder =self.current_recipie.result[0] if self.current_recipie else None
                item_amount = self.obj.res_slot.item_amount if self.obj.res_slot.item_name else 1
                draw_item(screen, self.obj.res_slot.item_name, item_amount,
                          self.result_pos, SMALL_FRAME_SIZE, SMALL_FONT, draw_bg=False,
                          placeholder_item=item_placeholder)

            for i, (n, a) in enumerate(zip(self.parent.inventory.n, self.parent.inventory.a)):

                pos = (self.inventory_pos[0] + 20 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * i, self.inventory_pos[1] + 60)
                draw_item(screen, n, a, pos, FRAME_SIZE)

        self.draw_cursor_slot()

    def events(self, events):

        pass

    def __flatten_recipies(self) -> list:

        return [element for sublist in workbench_recipies[self.current_category].values() for element in sublist]

    def inventory_shift(self, inventory, button_id):

        if self.obj.ing1_slot.can_fit(inventory.n[button_id], inventory.a[button_id]):
            self.obj.ing1_slot.append(inventory.n[button_id], inventory.a[button_id])
            inventory.pop_from_slot(button_id, inventory.a[button_id])
        elif self.obj.ing2_slot.can_fit(inventory.n[button_id], inventory.a[button_id]):
            self.obj.ing2_slot.append(inventory.n[button_id], inventory.a[button_id])
            inventory.pop_from_slot(button_id, inventory.a[button_id])

    def slot_shift(self, slot):

        if self.parent.inventory.can_fit(slot.item_name, slot.item_amount):
            self.parent.inventory.append(slot.item_name, slot.item_amount)
            slot.clear()

    def display_result_slot_info(self, button, item_name):

        if button.touching and (self.current_recipie or item_name):
            pos = (get_mouse_pos()[0] + TEXT_MOUSE_OFFSET[0], get_mouse_pos()[1] + TEXT_MOUSE_OFFSET[1])
            if item_name:
                print_data(screen, pos, items[item_name].name)
            else:
                print_data(screen, pos, items[self.current_recipie.result[0]].name)

    def update(self, obj):

        self.obj = obj

        self.update_recipe_book_btn()

        if self.recipies_opened:

            for i, btn in enumerate(self.recipies_buttons[self.current_category]):
                btn.update()
                if btn.touching:
                    self._draw_item_information(self.recipes[self.current_category][i].result[0])
                if btn.just_pressed:
                    self.current_book_recipie = self.recipes[self.current_category][i]

            for btn, category in zip(self.category_buttons, workbench_recipies.keys()):
                btn.update()
                if btn.just_pressed:
                    self.current_category = category
                    for btnj in self.recipies_buttons[category]:
                        btnj.update()

            self.exmpl_ingredient_1_button.update()
            self.exmpl_ingredient_2_button.update()
            self.exmpl_result_button.update()

            if self.exmpl_ingredient_1_button.touching:
                self._draw_item_information(self.current_book_recipie.ingredient1[0])
            if self.exmpl_ingredient_2_button.touching:
                self._draw_item_information(self.current_book_recipie.ingredient2[0])
            if self.exmpl_result_button.touching:
                self._draw_item_information(self.current_book_recipie.result[0])

        else:

            self.craft_button.update()

            self._handle_inventory(self.parent.inventory, self.inventory_buttons, self.inventory_shift)
            self._handle_slot(obj.ing1_slot, self.eng1_btn, self.slot_shift)
            self._handle_slot(obj.ing2_slot, self.eng2_btn, self.slot_shift)
            self._handle_slot(obj.res_slot, self.res_btn, self.slot_shift, output_only=True)

            self.current_recipie = workbench_recipies.find(obj.ing1_slot.item_name, obj.ing1_slot.item_amount,
                                                           obj.ing2_slot.item_name, obj.ing2_slot.item_amount)
            if self.current_recipie is None:
                self.current_recipie = workbench_recipies.find(obj.ing2_slot.item_name, obj.ing2_slot.item_amount,
                                                               obj.ing1_slot.item_name, obj.ing1_slot.item_amount)

            if self.craft_button.just_pressed and self.current_recipie:

                self.craft()

    def craft(self):

        ingredient1 = self.current_recipie.ingredient1
        ingredient2 = self.current_recipie.ingredient2
        result = self.current_recipie.result

        has_engr1 = self.obj.ing1_slot.contain(ingredient1[0], ingredient1[1])
        has_engr2 = self.obj.ing2_slot.contain(ingredient2[0], ingredient2[1])
        enough_space = self.obj.res_slot.can_fit(result[0], result[1])

        if has_engr1 and has_engr2 and enough_space :
            self.obj.ing1_slot.pop(ingredient1[1])
            self.obj.ing2_slot.pop(ingredient2[1])
            self.obj.res_slot.append(result[0], result[1])
            return

        has_engr1 = self.obj.ing2_slot.contain(ingredient1[0], ingredient1[1])
        has_engr2 = self.obj.ing1_slot.contain(ingredient2[0], ingredient2[1])
        enough_space = self.obj.res_slot.can_fit(result[0], result[1])

        if has_engr1 and has_engr2 and enough_space :
            self.obj.ing2_slot.pop(ingredient1[1])
            self.obj.ing1_slot.pop(ingredient2[1])
            self.obj.res_slot.append(result[0], result[1])

    def when_opened(self):

        self.current_book_recipie = None
        self.recipies_opened = False
