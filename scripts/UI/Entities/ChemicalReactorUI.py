from scripts.UI.Entities.BaseUI import BaseUI
from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.Managers.GameAssets import *
from scripts.UI.Components.BaseUIComponents import *
from scripts.UI.Components.Bg import Bg
from scripts.Entities.Buildings.ChemicalReactor import ChemicalReactor


def generate_colors(n):
    colors = []
    step = 255 // (n - 1)

    for r in range(0, 256, step):
        for g in range(0, 256, step):
            for b in range(0, 256, step):
                colors.append((r, g, b, 255))

    return colors


UI_TEXTURE = pg.transform.scale_by(pg.image.load("assets/ingame_UI/chemical_reactor.png"), 6)
PIXEL_SIZE = from_iterable(UI_TEXTURE.get_size()) / Vector(190, 102)


pallete = [
    (0, 0, 0, 0),
    (0, 0, 0, 255),
    (0, 32, 0, 255),
    (0, 64, 0, 255),
    (0, 96, 0, 255),
    (0, 128, 0, 255),
    (0, 160, 0, 255),
    (0, 192, 0, 255),
    (0, 224, 0, 255),
    (0, 255, 0, 255),
]

pallete = [(0, 0, 0, 0)] + [(0, n * 4, 0, 255) for n in range(0, 64)]
pallete = [(0, 0, 0, 0), (0, 0, 0, 255), (0, 0, 85, 255), (0, 0, 170, 255), (0, 0, 255, 255), (0, 85, 0, 255), (0, 85, 85, 255), (0, 85, 170, 255), (0, 85, 255, 255), (0, 170, 0, 255), (0, 170, 85, 255), (0, 170, 170, 255), (0, 170, 255, 255), (0, 255, 0, 255), (0, 255, 85, 255), (0, 255, 170, 255), (0, 255, 255, 255), (85, 0, 0, 255), (85, 0, 85, 255), (85, 0, 170, 255), (85, 0, 255, 255), (85, 85, 0, 255), (85, 85, 85, 255), (85, 85, 170, 255), (85, 85, 255, 255), (85, 170, 0, 255), (85, 170, 85, 255), (85, 170, 170, 255), (85, 170, 255, 255), (85, 255, 0, 255), (85, 255, 85, 255), (85, 255, 170, 255), (85, 255, 255, 255), (170, 0, 0, 255), (170, 0, 85, 255), (170, 0, 170, 255), (170, 0, 255, 255), (170, 85, 0, 255), (170, 85, 85, 255), (170, 85, 170, 255), (170, 85, 255, 255), (170, 170, 0, 255), (170, 170, 85, 255), (170, 170, 170, 255), (170, 170, 255, 255), (170, 255, 0, 255), (170, 255, 85, 255), (170, 255, 170, 255), (170, 255, 255, 255), (255, 0, 0, 255), (255, 0, 85, 255), (255, 0, 170, 255), (255, 0, 255, 255), (255, 85, 0, 255), (255, 85, 85, 255), (255, 85, 170, 255), (255, 85, 255, 255), (255, 170, 0, 255), (255, 170, 85, 255), (255, 170, 170, 255), (255, 170, 255, 255), (255, 255, 0, 255), (255, 255, 85, 255), (255, 255, 170, 255), (255, 255, 255, 255)]
pallete = [(0, 0, 0, 0)] + generate_colors(6)

"""

# aplle ][
pallete = [
    (0, 0, 0, 0),
    (81, 92, 22, 255),
    (132, 61, 82, 255),
    (234, 125, 39, 255),
    (81, 72, 136, 255),
    (232, 93, 239, 255),
    (245, 183, 201, 255),
    (0, 103, 82, 255),
    (0, 200, 44, 255),
    (145, 145, 145, 255),
    (201, 209, 153, 255),
    (0, 166, 240, 255),
    (152, 219, 201, 255),
    (200, 193, 247, 255),
    (255, 255, 255, 255)
]

# commodore 64
pallete = [
    (0, 0, 0, 0),
    (98, 98, 98, 255),
    (137, 137, 137, 255),
    (173, 173, 173, 255),
    (255, 255, 255, 255),
    (159, 78, 68, 255),
    (203, 126, 117, 255),
    (109, 84, 18, 255),
    (161, 104, 60, 255),
    (201, 212, 135, 255),
    (154, 226, 155, 255),
    (92, 171, 94, 255),
    (106, 191, 198, 255),
    (136, 126, 203, 255),
    (80, 69, 155, 255),
    (160, 87, 163, 255)
]
"""


class ChemicalDrillUI(BaseUI, metaclass=UIRegistry):

    def __init__(self, parent):

        from scripts.Managers.GameAssets import items, liquids

        super().__init__(parent)
        self.obj = None

        self.main_ui_pos = RESOLUTION / Vector(2, 2) - Vector(UI_TEXTURE.get_width(), UI_TEXTURE.get_height()) / Vector(2, 2)

        self.player_inventory_pos = Vector(RESOLUTION.x / 2 - BLANK_WIDE.get_width() / 2,
                                           self.main_ui_pos.y + UI_TEXTURE.get_height() - 50)
        self.player_inventory_buttons = []
        for n in range(len(self.parent.inventory)):
            pos = self.__get_player_ui_button_pos(n)
            self.player_inventory_buttons.append(Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, pos))

        self.input_inventory_buttons = None
        self.output_inventory_buttons = None

        self.bg = Bg()
        self.bg.blit(UI_TEXTURE, self.main_ui_pos.as_tuple())
        self.bg.blit(BLANK_WIDE, self.player_inventory_pos.as_tuple())
        self.bg.blit(FONT.render("Inventory", True, "#757575"),
                    (self.player_inventory_pos.x + 20, self.player_inventory_pos.y + 20))

        self.input_bucket_1_slot_pos = self.main_ui_pos + PIXEL_SIZE * Vector(8, 31)
        self.input_bucket_1_slot_button = Button(BUTTON, BUTTON_PRESSED, "", SMALL_FRAME_SIZE, self.input_bucket_1_slot_pos.as_tuple())

        self.input_bucket_2_slot_pos = self.main_ui_pos + PIXEL_SIZE * Vector(33, 31)
        self.input_bucket_2_slot_button = Button(BUTTON, BUTTON_PRESSED, "", SMALL_FRAME_SIZE, self.input_bucket_2_slot_pos.as_tuple())

        self.input_bucket_3_slot_pos = self.main_ui_pos + PIXEL_SIZE * Vector(147, 31)
        self.input_bucket_3_slot_button = Button(BUTTON, BUTTON_PRESSED, "", SMALL_FRAME_SIZE, self.input_bucket_3_slot_pos.as_tuple())

        self.input_bucket_4_slot_pos = self.main_ui_pos + PIXEL_SIZE * Vector(172, 31)
        self.input_bucket_4_slot_button = Button(BUTTON, BUTTON_PRESSED, "", SMALL_FRAME_SIZE, self.input_bucket_4_slot_pos.as_tuple())

        self.output_bucket_1_slot_pos = self.main_ui_pos + PIXEL_SIZE * Vector(8, 69)
        self.output_bucket_1_slot_button = Button(BUTTON, BUTTON_PRESSED, "", SMALL_FRAME_SIZE, self.output_bucket_1_slot_pos.as_tuple())

        self.output_bucket_2_slot_pos = self.main_ui_pos + PIXEL_SIZE * Vector(33, 69)
        self.output_bucket_2_slot_button = Button(BUTTON, BUTTON_PRESSED, "", SMALL_FRAME_SIZE, self.output_bucket_2_slot_pos.as_tuple())

        self.output_bucket_3_slot_pos = self.main_ui_pos + PIXEL_SIZE * Vector(147, 69)
        self.output_bucket_3_slot_button = Button(BUTTON, BUTTON_PRESSED, "", SMALL_FRAME_SIZE, self.output_bucket_3_slot_pos.as_tuple())

        self.output_bucket_4_slot_pos = self.main_ui_pos + PIXEL_SIZE * Vector(172, 69)
        self.output_bucket_4_slot_button = Button(BUTTON, BUTTON_PRESSED, "", SMALL_FRAME_SIZE, self.output_bucket_4_slot_pos.as_tuple())

        self.display_pos = self.main_ui_pos + PIXEL_SIZE * Vector(57, 7)
        self.display_actual_pos = self.main_ui_pos + PIXEL_SIZE * Vector(54, 4)
        self.display_size = PIXEL_SIZE * Vector(82, 50)

        self.input_tank_1_rect = pg.Rect(self.main_ui_pos.x + PIXEL_SIZE.x * 10, self.main_ui_pos.y + PIXEL_SIZE.y * 43, PIXEL_SIZE.x * 6, PIXEL_SIZE.y * 24)
        self.input_tank_2_rect = pg.Rect(self.main_ui_pos.x + PIXEL_SIZE.x * 35, self.main_ui_pos.y + PIXEL_SIZE.y * 43, PIXEL_SIZE.x * 6, PIXEL_SIZE.y * 24)
        self.output_tank_1_rect = pg.Rect(self.main_ui_pos.x + PIXEL_SIZE.x * 149, self.main_ui_pos.y + PIXEL_SIZE.y * 43, PIXEL_SIZE.x * 6, PIXEL_SIZE.y * 24)
        self.output_tank_2_rect = pg.Rect(self.main_ui_pos.x + PIXEL_SIZE.x * 174, self.main_ui_pos.y + PIXEL_SIZE.y * 43, PIXEL_SIZE.x * 6, PIXEL_SIZE.y * 24)

        self.WHITE_NOISE = [load_texture(f"assets/ingame_UI/white_noise/white_noise-{i}.png", self.display_size) for i in range(6)]
        for texture in self.WHITE_NOISE:
            texture.set_alpha(32)

        self.display_spacing = Vector(20, 20)

        self.current_recipe_data_pos = self.display_actual_pos + self.display_spacing
        self.current_recipe_data_header = SMALL_FONT.render("Current Recipe:", True, "#00ff00")
        self.engredients_status_data_pos = self.display_actual_pos + self.display_spacing * Vector(1, 2) + Vector(0, SMALL_FONT.get_height())
        self.engredients_status_data_header = SMALL_FONT.render("Engredients Status:", True, "#00ff00")
        self.electricity_status_data_pos = self.display_actual_pos + self.display_spacing * Vector(1, 2) + Vector(0, SMALL_FONT.get_height() * 3)
        self.electricity_status_data_header = SMALL_FONT.render("Electricity Status:", True, "#00ff00")
        self.progress_data_pos = self.display_actual_pos + self.display_size * Vector(0, 1) + self.display_spacing * Vector(1, -2)
        self.progress_data_header = SMALL_FONT.render("Progress:", True, "#00ff00")
        self.progress_bar_rect = pg.Rect(self.progress_data_pos.x + self.progress_data_header.get_width() + self.display_spacing.x, self.progress_data_pos.y, self.display_size.x - (self.progress_data_pos.x - self.display_actual_pos.x) - self.display_spacing.x * 2 - self.progress_data_header.get_width(), SMALL_FONT.get_height())

        change_recipe_button_size = Vector(250, 30)
        change_recipe_button_pos = self.display_actual_pos + self.display_spacing + (self.engredients_status_data_pos - self.display_actual_pos - self.display_spacing) + Vector(0, FONT.get_height()*3)

        change_recipe_button_texture = pg.Surface(change_recipe_button_size.as_tuple())
        change_recipe_button_texture.fill("#000000")
        pg.draw.rect(change_recipe_button_texture, "#005500", (0, 0, change_recipe_button_size.x, change_recipe_button_size.y), 2)
        change_recipe_button_texture.set_colorkey("#000000")

        self.change_recipe_button = Button(change_recipe_button_texture, change_recipe_button_texture, "change recipe", change_recipe_button_size.as_tuple(), change_recipe_button_pos.as_tuple(), "#00ff00", font=SMALL_FONT)

        self.chosing_recipe = False

        self.recipe_button_size = Vector(48, 48)

        self.line_start = self.display_actual_pos + self.display_spacing * Vector(0, 1) + self.recipe_button_size * Vector(1.1, 0) * Vector(3, 0) + self.display_spacing * Vector(1, 0)
        self.line_end = self.display_actual_pos + self.display_spacing * Vector(0, -1) + self.recipe_button_size * Vector(1.1, 0) * Vector(3, 0) + self.display_spacing * Vector(1, 0) + self.display_size * Vector(0, 1)

        self.currently_watched_recipe = None
        self.recipe_buttons = []
        self.cashed_buttons_textures: list[pg.Surface] = []
        for n, recipe in enumerate(chemical_reactor_recipes):
            pos = self.display_actual_pos + self.display_spacing * Vector(0.5, 1) + (self.recipe_button_size * Vector(1.1, 1.1)) * Vector(n % 3, n // 3)
            texture = change_texture_palette(items[recipe.icon_item].texture, pallete)
            self.cashed_buttons_textures.append(texture.copy())
            button = Button(texture, texture, "", self.recipe_button_size.as_tuple(), pos.as_tuple())
            self.recipe_buttons.append(button)

        recipe_name_pos = self.display_spacing
        recipe_formula_pos = recipe_name_pos + Vector(0, SMALL_FONT.get_height())
        ingredients_start_pos = recipe_name_pos + Vector(0, SMALL_FONT.get_height() * 2.5)

        self.info_pos = self.line_start - Vector(0, self.display_spacing.y)
        self.recipe_data_cash = []
        for recipe in chemical_reactor_recipes:

            surf = pg.Surface((self.display_size - Vector(self.line_start.x - self.display_pos.x + self.display_spacing.x, 0)).as_tuple())
            surf.fill("#000000")
            surf.blit(SMALL_FONT.render(recipe.name, True, "#00ff00"), recipe_name_pos.as_tuple())
            surf.blit(TINY_FONT.render(recipe.formula, True, "#00ff00"), recipe_formula_pos.as_tuple())

            pos = deepcopy(ingredients_start_pos)

            input_data = [(items[name].name, amount) for name, amount in recipe.input_items] + [(liquids[name]["name"], amount) for name, amount in recipe.input_liquids]
            for name, amount in input_data:
                surf.blit(SMALL_FONT.render(f"{name} x{amount}", True, "#00ff00"), pos.as_tuple())
                pos += Vector(0, SMALL_FONT.get_height())

            surf.blit(SMALL_FONT.render("↓", True, "#00ff00"), pos.as_tuple())
            pos += Vector(0, SMALL_FONT.get_height())

            output_data = [(items[name].name, amount) for name, amount in recipe.output_items] + [(liquids[name]["name"], amount) for name, amount in recipe.output_liquids]
            for name, amount in output_data:
                surf.blit(SMALL_FONT.render(f"{name} x{amount}", True, "#00ff00"), pos.as_tuple())
                pos += Vector(0, SMALL_FONT.get_height())

            surf.set_colorkey("#000000")
            self.recipe_data_cash.append(surf.copy())

        ok_button_size = self.recipe_button_size * Vector(1.1, 1.1) * Vector(2, 1) + self.recipe_button_size * Vector(1, 0)
        ok_button_pos = self.display_actual_pos + self.display_size * Vector(0, 1) + self.display_spacing * Vector(0.5, -1) - ok_button_size * Vector(0, 1)
        ok_button_texture = pg.Surface(ok_button_size.as_tuple())
        ok_button_texture.fill("#000000")
        ok_button_texture.set_colorkey("#000000")
        pg.draw.rect(ok_button_texture, "#005500", (0, 0, ok_button_size.x, ok_button_size.y), 2)

        self.ok_button = Button(ok_button_texture, ok_button_texture, "accept", ok_button_size.as_tuple(), ok_button_pos.as_tuple(), text_color="#00ff00")

        self.input_inventory_buttons = []
        for n in range(4):
            pos = self.__get_input_ui_button_pos(n)
            self.input_inventory_buttons.append(Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, pos))
        self.output_inventory_buttons = []
        for n in range(4):
            pos = self.__get_output_ui_button_pos(n)
            self.output_inventory_buttons.append(Button(BUTTON, BUTTON_PRESSED, "", FRAME_SIZE, pos))

    def change_buttons_textures(self):

        for n, button in enumerate(self.recipe_buttons):
            new_texture = pg.Surface(self.cashed_buttons_textures[n].get_size(), pg.SRCALPHA, 32)
            if n == self.currently_watched_recipe:
                pg.draw.rect(new_texture, "#005500", (0, 0, new_texture.get_width(), new_texture.get_height()), 1)
            new_texture.blit(self.cashed_buttons_textures[n], (0, 0))
            button.texture = pg.transform.scale(new_texture, self.recipe_button_size.as_tuple())

    def inventory_shift(self, inventory, button_id):

        if self.obj.input.can_fit(self.parent.inventory.n[button_id], self.parent.inventory.a[button_id]):
            self.obj.input.append(self.parent.inventory.n[button_id], self.parent.inventory.a[button_id])
            self.parent.inventory.n[button_id] = None
            self.parent.inventory.a[button_id] = 0

    def from_inventory_shift(self, inventory, button_id):

        if self.parent.inventory.can_fit(inventory.n[button_id], inventory.a[button_id]):
            self.parent.inventory.append(inventory.n[button_id], inventory.a[button_id])
            inventory.n[button_id] = None
            inventory.a[button_id] = 0

    def slot_shift(self, slot):

        if self.parent.inventory.can_fit(slot.item_name, slot.item_amount):
            self.parent.inventory.append(slot.item_name, slot.item_amount)
            slot.clear()

    def when_opened(self):

        self.chosing_recipe = False
        if self.obj:
            self.currently_watched_recipe = self.obj.current_recipe
        self.update_recipe_book_btn()

    @staticmethod
    def _calculate_bar_rect(initial_rect, current_value, max_value):

        return pg.Rect(initial_rect.x, initial_rect.y, (current_value / (max_value if max_value != 0 else 1)) * initial_rect.w, initial_rect.h)

    def draw(self, display):

        # self.draw_recipe_book_btn()

        if self.recipies_opened:

            pass

        else:

            pg.draw.rect(screen, "#000000", self.input_tank_1_rect)
            pg.draw.rect(screen, "#000000", self.input_tank_2_rect)
            pg.draw.rect(screen, "#000000", self.output_tank_1_rect)
            pg.draw.rect(screen, "#000000", self.output_tank_2_rect)

            if self.obj:

                self._draw_liquid(self.input_tank_1_rect, self.obj.input_liquids[0])
                self._draw_liquid(self.input_tank_2_rect, self.obj.input_liquids[1])
                self._draw_liquid(self.output_tank_1_rect, self.obj.output_liquids[0])
                self._draw_liquid(self.output_tank_2_rect, self.obj.output_liquids[1])

            self.bg.draw()

            if self.chosing_recipe:
                pass
            else:
                self.change_recipe_button.draw()

            for n, (item, amount) in enumerate(zip(self.parent.inventory.n, self.parent.inventory.a)):
                pos = self.__get_player_ui_button_pos(n)
                draw_item(screen, item, amount, pos, FRAME_SIZE)

            if self.obj:

                if self.chosing_recipe:
                    pg.draw.line(screen, "#00ff00", self.line_start.as_tuple(), self.line_end.as_tuple(), 2)
                    screen.blit(self.recipe_data_cash[self.currently_watched_recipe], self.info_pos.as_tuple())
                    for button in self.recipe_buttons:
                        button.draw()
                    self.ok_button.draw()
                else:
                    screen.blit(self.current_recipe_data_header, self.current_recipe_data_pos.as_tuple())
                    screen.blit(SMALL_FONT.render(chemical_reactor_recipes[self.obj.current_recipe].formula, True, "#00ff00"), (self.current_recipe_data_pos + Vector(20, SMALL_FONT.get_height())).as_tuple())
                    screen.blit(self.engredients_status_data_header, self.engredients_status_data_pos.as_tuple())
                    screen.blit(SMALL_FONT.render("Enough engredients" if self.obj.enough_engredients() else "Not enough engredients", True, "#00ff00"), (self.engredients_status_data_pos + Vector(20, SMALL_FONT.get_height())).as_tuple())
                    screen.blit(self.electricity_status_data_header, self.electricity_status_data_pos.as_tuple())
                    screen.blit(SMALL_FONT.render("Enough electricity" if self.obj.enough_energy else "Not enough electricity", True, "#00ff00"), (self.electricity_status_data_pos + Vector(20, SMALL_FONT.get_height())).as_tuple())
                    screen.blit(self.progress_data_header, (self.display_actual_pos + self.display_size * Vector(0, 1) + self.display_spacing * Vector(1, -2)).as_tuple())
                    pg.draw.rect(screen, "#00ff00", self.progress_bar_rect, 2)
                    pg.draw.rect(screen, "#00ff00", self._calculate_bar_rect(self.progress_bar_rect, self.obj.progress, self.obj.total_progress))
                for n, (item, amount) in enumerate(zip(self.obj.input.n, self.obj.input.a)):
                    pos = self.__get_input_ui_button_pos(n)
                    draw_item(screen, item, amount, pos, FRAME_SIZE, draw_bg=False)
                for n, (item, amount) in enumerate(zip(self.obj.output.n, self.obj.output.a)):
                    # print(item, amount)
                    pos = self.__get_output_ui_button_pos(n)
                    draw_item(screen, item, amount, pos, FRAME_SIZE, draw_bg=False)

                draw_item(screen, self.obj.input_bucket_1.item_name, self.obj.input_bucket_1.item_amount, self.input_bucket_1_slot_pos.as_tuple(), SMALL_FRAME_SIZE, draw_bg=False)
                draw_item(screen, self.obj.input_bucket_2.item_name, self.obj.input_bucket_2.item_amount, self.input_bucket_2_slot_pos.as_tuple(), SMALL_FRAME_SIZE, draw_bg=False)
                draw_item(screen, self.obj.input_bucket_3.item_name, self.obj.input_bucket_3.item_amount, self.input_bucket_3_slot_pos.as_tuple(), SMALL_FRAME_SIZE, draw_bg=False)
                draw_item(screen, self.obj.input_bucket_4.item_name, self.obj.input_bucket_4.item_amount, self.input_bucket_4_slot_pos.as_tuple(), SMALL_FRAME_SIZE, draw_bg=False)
                draw_item(screen, self.obj.output_bucket_1.item_name, self.obj.output_bucket_1.item_amount, self.output_bucket_1_slot_pos.as_tuple(), SMALL_FRAME_SIZE, draw_bg=False)
                draw_item(screen, self.obj.output_bucket_2.item_name, self.obj.output_bucket_2.item_amount, self.output_bucket_2_slot_pos.as_tuple(), SMALL_FRAME_SIZE, draw_bg=False)
                draw_item(screen, self.obj.output_bucket_3.item_name, self.obj.output_bucket_3.item_amount, self.output_bucket_3_slot_pos.as_tuple(), SMALL_FRAME_SIZE, draw_bg=False)
                draw_item(screen, self.obj.output_bucket_4.item_name, self.obj.output_bucket_4.item_amount, self.output_bucket_4_slot_pos.as_tuple(), SMALL_FRAME_SIZE, draw_bg=False)

        screen.blit(self.WHITE_NOISE[self.parent.animation_counter // 5 % len(self.WHITE_NOISE)], self.display_actual_pos.as_tuple())
        self.draw_cursor_slot()

    def update(self, obj: ChemicalReactor):

        self.obj = obj

        if self.recipies_opened:

            pass

        else:

            if self.chosing_recipe:
                for n, button in enumerate(self.recipe_buttons):
                    button.update()
                    if button.just_pressed:
                        self.currently_watched_recipe = n
                        self.change_buttons_textures()
                self.ok_button.update()
                if self.ok_button.just_pressed:
                    self.obj.set_recipe(self.currently_watched_recipe)
                    self.chosing_recipe = False
            else:
                self.change_recipe_button.update()
                if self.change_recipe_button.just_pressed:
                    self.currently_watched_recipe = self.obj.current_recipe
                    self.change_buttons_textures()
                    self.chosing_recipe = True

            self._handle_inventory(self.parent.inventory, self.player_inventory_buttons, self.inventory_shift)

            self._handle_inventory(self.obj.input, self.input_inventory_buttons, self.from_inventory_shift)
            self._handle_inventory(self.obj.output, self.output_inventory_buttons, self.from_inventory_shift, output_only=True)

            self._handle_slot(self.obj.input_bucket_1, self.input_bucket_1_slot_button, self.slot_shift)
            self._handle_slot(self.obj.input_bucket_2, self.input_bucket_2_slot_button, self.slot_shift)
            self._handle_slot(self.obj.input_bucket_3, self.input_bucket_3_slot_button, self.slot_shift)
            self._handle_slot(self.obj.input_bucket_4, self.input_bucket_4_slot_button, self.slot_shift)
            self._handle_slot(self.obj.output_bucket_1, self.output_bucket_1_slot_button, self.slot_shift, output_only=True)
            self._handle_slot(self.obj.output_bucket_2, self.output_bucket_2_slot_button, self.slot_shift, output_only=True)
            self._handle_slot(self.obj.output_bucket_3, self.output_bucket_3_slot_button, self.slot_shift, output_only=True)
            self._handle_slot(self.obj.output_bucket_4, self.output_bucket_4_slot_button, self.slot_shift, output_only=True)

            self._draw_tank_info(self.input_tank_1_rect, self.obj.input_liquids[0])
            self._draw_tank_info(self.input_tank_2_rect, self.obj.input_liquids[1])
            self._draw_tank_info(self.output_tank_1_rect, self.obj.output_liquids[0])
            self._draw_tank_info(self.output_tank_2_rect, self.obj.output_liquids[1])

    def events(self, events):

        pass

    def __get_input_ui_button_pos(self, n: int):

        return (self.main_ui_pos + (PIXEL_SIZE * Vector(54, 57) + PIXEL_SIZE * (Vector(16, 16) * Vector(n % 2, n // 2)))).as_tuple()

    def __get_output_ui_button_pos(self, n: int):

        return (self.main_ui_pos + (PIXEL_SIZE * Vector(105, 57) + PIXEL_SIZE * (Vector(16, 16) * Vector(n % 2, n // 2)))).as_tuple()

    def __get_player_ui_button_pos(self, n: int):

        return self.player_inventory_pos.x + 20 + (FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * n, self.player_inventory_pos.y + 60