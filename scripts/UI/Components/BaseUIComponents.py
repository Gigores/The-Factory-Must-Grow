from math import ceil
from abc import ABC, abstractmethod
from scripts.Managers.GameAssets import *
import re
import ast

BLANK = pg.transform.scale_by(pg.image.load("assets/ingame_UI/blank.png"), 6)
BLANK2 = pg.transform.scale_by(pg.image.load("assets/ingame_UI/blank2.png"), 6)
FRAME = pg.image.load("assets/ingame_UI/FRAME.png")
BUTTON = pg.image.load("assets/ingame_UI/button.png")
BUTTON_PRESSED = pg.image.load("assets/ingame_UI/button_pressed.png")
RED_BUTTON = pg.image.load("assets/ingame_UI/button_red.png")
RED_BUTTON_PRESSED = pg.image.load("assets/ingame_UI/button_red_pressed.png")

ELEMENT_SPACING = 5
FRAME_SIZE = (96, 96)
SMALL_FRAME_SIZE = (64, 64)

BLANK_WIDE = pg.transform.scale(
    pg.image.load("assets/ingame_UI/blank_wide.png"), ((FRAME_SIZE[0] + FRAME_SIZE[0] / 16) * INVENTORY_SIZE + 40, FRAME_SIZE[1] * 2.5))

FIREBOX = [
    pg.transform.scale_by(pg.image.load("assets/ingame_UI/firebox1.png"), 6),
    pg.transform.scale_by(pg.image.load("assets/ingame_UI/firebox2.png"), 6),
    pg.transform.scale_by(pg.image.load("assets/ingame_UI/firebox3.png"), 6),
    pg.transform.scale_by(pg.image.load("assets/ingame_UI/firebox4.png"), 6),
    pg.transform.scale_by(pg.image.load("assets/ingame_UI/firebox5.png"), 6),
]

TEXT_MOUSE_OFFSET = (20, 40)

CLICK_SOUND = pg.mixer.Sound("sound/click.wav")
SELECT_SOUND = pg.mixer.Sound("sound/select.wav")

SELECT_SOUND.set_volume(0.5)
CLICK_SOUND.set_volume(0.5)


def draw_item(display, item_name: str | None, item_amount: int, pos: tuple[int, int], image_size: tuple[int, int],
              font=FONT, placeholder_item=None, draw_bg: bool = True, draw_outline: bool = False):

    #display.blit(pg.transform.scale(FRAME, image_size), pos)
    bg = pg.Surface(image_size)
    bg.fill("#000000")
    bg.set_alpha(75)
    if draw_bg:
        display.blit(bg, pos)
    if draw_outline:
        pg.draw.rect(display, "#ffffff", (pos[0], pos[1], image_size[0], image_size[1]), int(image_size[0] / 16))
    if item_name:
        display.blit(pg.transform.scale(items[item_name].texture, image_size), pos)
    elif placeholder_item:
        image = pg.Surface(image_size)
        image.fill("#ff0000")
        image.blit(pg.transform.scale(items[placeholder_item].texture, image_size), (0, 0))
        image.set_colorkey("#ff0000")
        image.set_alpha(100)
        display.blit(image, pos)
    if item_amount > 1:
        display.blit(font.render(f"{item_amount}", True, "#ffffff"), (pos[0] + image_size[0] / 8 * 1.5, pos[1] + image_size[1] / 8 * 1.5))


def print_data(display, pos, text, font=SMALL_FONT):
    border_width = 5
    text_surf = font.render(text, True, "#ffffff")
    text_pos = (pos[0] + border_width, pos[1] + border_width)
    rect = pg.Rect(pos[0], pos[1], text_surf.get_width() + border_width * 2, text_surf.get_height() + border_width * 2)
    img = pg.Surface(rect.size)
    img.fill("#000000")
    img.set_alpha(150)
    display.blit(img, pos)
    display.blit(text_surf, text_pos)


class Button:

    def __init__(self, texture, texture_pressed, text: str, size, pos, text_color="#000000", font=FONT,
                 mouse_button_id: int = 0, invert_rect: bool = False, activa_on_up: bool = False):

        self.texture = pg.transform.scale(texture, size)
        if texture_pressed: self.pressed_texture = pg.transform.scale(texture_pressed, size)
        self.text_surface = font.render(text, True, text_color)
        self.pos = pos
        self.rect = pg.Rect((pos[0], pos[1], size[0], size[1]))
        self.pressed = False
        self.just_pressed = False
        self.touching = False
        self.just_touched = False
        self.have_texture_pressed = bool(texture_pressed)
        self.mouse_button_id = mouse_button_id
        self.invert_rect = invert_rect
        self.active_on_up = activa_on_up
        self.screen_pos = (0, 0)

        self.delta_y = self.texture.get_height() / 5.714285714

    def draw(self, dest: pg.Surface = screen):

        text_pos = (
            self.screen_pos[0] + self.texture.get_width() / 2 - self.text_surface.get_width() / 2,
            self.screen_pos[1] + self.texture.get_height() / 2 - self.text_surface.get_height() / 2
            + self.delta_y * int(self.pressed and self.have_texture_pressed),
        )

        dest.blit(self.texture if not (self.pressed and self.have_texture_pressed) else self.pressed_texture, self.screen_pos)
        dest.blit(self.text_surface, text_pos)

    def update(self, offset: tuple = (0, 0), get_mouse_position: callable = get_mouse_pos):

        self.screen_pos = (
            self.pos[0] + offset[0],
            self.pos[1] + offset[1],
        )
        self.rect.x, self.rect.y = self.screen_pos

        if self.just_pressed:
            self.just_pressed = False

        self.touching = (not self.rect.collidepoint(get_mouse_position())) if self.invert_rect else (self.rect.collidepoint(get_mouse_position()))
        mouse_pressed = pg.mouse.get_pressed()[self.mouse_button_id]

        if self.active_on_up:

            if not mouse_pressed and self.pressed:
                self.just_pressed = True

            if self.touching and mouse_pressed and not self.pressed:
                self.pressed = True
            elif not (self.touching and mouse_pressed):
                self.pressed = False

        else:

            if self.touching and mouse_pressed and not self.pressed:
                self.pressed = True
                self.just_pressed = True
            elif not (self.touching and mouse_pressed):
                self.pressed = False


class Text:

    class Lexer:

        def __init__(self, text: str):

            self.text = text
            self.char_id = 0
            self.char = "-"

            if not text:
                raise ValueError("Text length can't be empty")

        def tokenize(self):

            self.reset()
            tokens = []
            text = ""

            while self.char_id < len(self.text) - 1 :
                if self.char == "<" :
                    if text :
                        tokens.append(("text", text))
                        text = ""
                    tokens.append(self.process_tag())
                elif self.char == "\n" :
                    if text :
                        tokens.append(("text", text))
                        text = ""
                    tokens.append(("nl", None))
                else :
                    text += self.char

                self.advance()

            if text:
                text += self.char
                tokens.append(("text", text))

            return tokens

        def process_tag(self) -> tuple[str, dict[str, any]] :
            token = ""
            attributes = {}

            while self.char_id < len(self.text) - 1 :
                self.advance()
                if self.char == ">" :
                    break
                token += self.char

            parts = token.split()
            key = parts[0]

            def parse_value(value: str) -> any :
                is_string = False
                if value.startswith('"') and value.endswith('"') :
                    value = value[1 :-1]
                    is_string = True
                elif value.startswith("'") and value.endswith("'") :
                    value = value[1 :-1]
                    is_string = True

                if value == "True" :
                    return True
                elif value == "False" :
                    return False
                try :
                    if "." in value :
                        return float(value)
                    if not is_string:
                        return int(value)
                except ValueError :
                    pass

                try :
                    parsed = ast.literal_eval(value)
                    if type(parsed) in (list, tuple, dict):
                        return parsed
                    else:
                        return value
                except (ValueError, SyntaxError) :
                    return value

            for attr in parts[1 :] :
                if "=" in attr :
                    attr_key, attr_value = attr.split("=", 1)
                    attributes[attr_key] = parse_value(attr_value)
                else :
                    attributes[attr] = None

            return key, attributes

        def reset(self):

            self.char_id = 0
            self.char = self.text[0]

        def advance(self):

            self.char_id += 1
            self.char = self.text[self.char_id]

        @staticmethod
        def get_raw_text(tokens) -> str:

            text = ""

            for token in tokens:
                token_type, token_content = token
                if token_type == "text":
                    text += token_content

            return text

    def __init__(self, pos: Vector, text: str, default_text_color: str = "#ffffff", font: pg.font.Font = FONT, max_size: Vector = None):

        self.pos = pos
        self.text = text
        self.font = font
        self.max_size = max_size
        self.default_text_color = default_text_color
        self.tokens = self.Lexer(self.text).tokenize()
        self.surface = self.update_text_surface()

    @staticmethod
    def get_token_attribute(token_type, token_content: dict, attribute_name, expected_type, default_value=None):

        attribute = token_content.get(attribute_name, default_value)
        if attribute is None:
            raise ValueError(f"Missing required '{attribute_name}' attribute in '{token_type}' tag.")
        if type(attribute) is not expected_type:
            raise TypeError(f"Expected '{expected_type.__name__}' type for attribute '{attribute_name}' in '{token_type}' tag, but got {type(attribute).__name__}: {attribute}")
        if token_type == "molecule": print(attribute)
        return attribute

    def update_text_surface(self) -> pg.Surface:

        if self.max_size is None:
            width = max([self.font.get_height() if token[0] == "item" else (self.get_token_attribute("molecule", token[1], "width", int, 400) if token[0] == "molecule" else self.font.render(token[1], False, self.default_text_color).get_width()) for token in self.split_and_merge_tokens()])
            height = sum([self.font.get_height() if token[0] == "nl" else (self.get_token_attribute("molecule", token[1], "height", int, 400) if token[0] == "molecule" else 0) for token in self.tokens]) + self.font.get_linesize()
        else:
            width, height = self.max_size.as_tuple()

        surface = pg.Surface((width, abs(height)))
        surface.fill((0, 0, 0, 0))
        surface.set_colorkey((0, 0, 0, 0))

        text_pos = Vector(0, 0)
        text_col = self.default_text_color
        for token in self.tokens:
            token_type, token_content = token
            if token_type == "text":
                rendered_token_content = self.font.render(token_content.replace('\n', ''), False, text_col)
                surface.blit(rendered_token_content, text_pos.as_tuple())
                text_pos += Vector(rendered_token_content.get_width(), 0)
            elif token_type == "nl":
                text_pos.x = self.pos.x
                text_pos.y += self.font.get_height()
            elif token_type == "col":
                if "hex" in token_content:
                    new_color = self.get_token_attribute("col", token_content, "hex", str)
                    text_col = f"#{new_color}"
                else:
                    text_col = self.default_text_color
            elif token_type == "item":
                item_name = self.get_token_attribute("item", token_content, "name", str)
                texture = pg.transform.scale(items[item_name].texture, (self.font.get_height(), self.font.get_height()))
                surface.blit(texture, text_pos.as_tuple())
                text_pos += Vector(texture.get_width(), 0)
            elif token_type == "molecule":
                text_pos.x = self.pos.x
                text_pos.y += self.font.get_height()
                molecule_surf = MOLECULE_RENDERER.render_molecule_diagram(**token_content)
                surface.blit(molecule_surf, text_pos.as_tuple())
                text_pos += Vector(0, surface.get_height())
            else:
                raise NameError(f"There is no tag with name '{token_type}'")
        return surface

    def split_and_merge_tokens(self):

        grouped_tokens = []
        current_group = []

        for token_type, token_content in self.tokens:
            if token_type == "nl":
                if current_group:
                    grouped_tokens.append(("text", " ".join(content for _, content in current_group)))
                    current_group = []
            elif token_type == "text":
                current_group.append((token_type, token_content))
            elif token_type == "item":
                current_group.append((token_type, ""))
            elif token_type == "molecule":
                if current_group:
                    grouped_tokens.append(("text", " ".join(content for _, content in current_group)))
                    current_group = []
                grouped_tokens.append((token_type, token_content))

        if current_group:
            grouped_tokens.append(("text", " ".join(content for _, content in current_group)))

        return grouped_tokens

    def draw(self, dest: pg.Surface = screen, pos: Vector = None):

        dest.blit(self.surface, self.pos.as_tuple() if not pos else pos.as_tuple())
        # pg.draw.rect(screen, "#ff0000", (self.pos.x, self.pos.y, self.surface.get_width(), self.surface.get_height()), 2)


class AchievementDisplay:

    def __init__(self, parent, pos, image, text, ach_id):

        self.parent = parent
        self.pos = pos
        self.texture = image
        self.text = text
        self.ach_id = ach_id
        self.text_obj = Text(Vector(0, 0), text)
        self.screen_pos = Vector(0, 0)
        self.rect = self.texture.get_rect()
        self.texture_offset = from_iterable(self.texture.get_size()) * Vector(-0.5, -0.5)
        self.touching = False

    def update(self, offset: tuple, get_mouse_position: callable = get_mouse_pos):

        self.screen_pos = self.pos + from_iterable(offset)
        self.rect.x, self.rect.y = (self.screen_pos + self.texture_offset).as_tuple()
        self.touching = self.rect.collidepoint(get_mouse_position())

    def draw(self, dest: pg.Surface = screen):

        dest.blit(self.texture, (self.screen_pos + self.texture_offset).as_tuple())
        if not (self.ach_id in self.parent.unlocked_achievements):
            surf = pg.Surface(self.texture.get_size())
            surf.fill("#000000")
            surf.set_alpha(150)
            dest.blit(surf, (self.screen_pos + self.texture_offset).as_tuple())
        # pg.draw.rect(dest, "#ff0000", self.rect, 2)

    def draw_text(self, dest: pg.Surface = screen):

        if self.touching:
            pos = self.screen_pos + self.texture_offset + Vector(self.texture.get_width(), 0)
            # print(pos)
            texture_size = from_iterable(self.text_obj.surface.get_size()) + Vector(20, 20)
            bg = pg.Surface(texture_size.as_tuple())
            bg.fill("#000000")
            bg.set_alpha(100)
            text = self.text_obj.surface.copy()
            text.set_colorkey("#000000")
            dest.blit(bg, pos.as_tuple())
            dest.blit(text, (pos + Vector(10, 10)).as_tuple())


class Arrow:

    WIDTH = 10

    def __init__(self, parent, from_, to_, fixed: bool = False):

        self.parent = parent
        self.from_ = from_
        self.to_ = to_
        self.offset = Vector(0, 0)
        self.rect1_base = pg.Rect(
            self.from_.x - self.WIDTH if self.from_.x < self.to_.x else self.to_.x + self.WIDTH,
            self.from_.y - self.WIDTH if fixed else self.to_.y - self.WIDTH,
            self.to_.x - self.from_.x,
            self.WIDTH * 2
        )
        self.rect2_base = pg.Rect(
            self.from_.x - self.WIDTH + (self.to_.x - self.from_.x) if fixed else self.to_.x - self.WIDTH + (self.from_.x - self.to_.x),
            self.from_.y - self.WIDTH if self.from_.y < self.to_.y else self.to_.y + self.WIDTH,
            self.WIDTH * 2,
            self.to_.y - self.from_.y,
        )
        self.rect1 = self.rect1_base.copy()
        self.rect2 = self.rect2_base.copy()

        self.surf1, self.surf2 = self.create_surfaces()

    def create_surfaces(self) -> tuple[pg.Surface, pg.Surface]:

        surf1 = pg.Surface((abs(self.rect1_base.width), abs(self.rect1_base.height)))
        surf2 = pg.Surface((abs(self.rect2_base.width), abs(self.rect2_base.height)))

        surf1.fill("#000000")
        surf2.fill("#000000")

        surf1.set_alpha(100)
        surf2.set_alpha(100)

        return surf1, surf2

    def update(self, offset, get_mouse_position):

        self.rect1.x = self.rect1_base.x + offset[0]
        self.rect1.y = self.rect1_base.y + offset[1]
        self.rect2.x = self.rect2_base.x + offset[0]
        self.rect2.y = self.rect2_base.y + offset[1]

    def draw(self, dest):

        dest.blit(self.surf1, (self.rect1.x, self.rect1.y))
        dest.blit(self.surf2, (self.rect2.x, self.rect2.y))


class Scrollbar:

    def __init__(self, parent, pos: Vector, size: Vector, up_down: bool = True, left_right: bool = False,
                 bg_image: pg.Surface = None):

        self.parent = parent
        self.pos = pos
        self.size = size
        self.up_down = up_down
        self.left_right = left_right
        self.bg_image = bg_image
        self.objects = {}
        self.mouse_in = False
        self._surf = pg.Surface(size.as_tuple())
        self._offset = Vector(0, 0) + self.size / Vector(2, 2)
        self._rect = pg.Rect((self.pos.x, self.pos.y, self.size.x, self.size.y))

    def add_obj(self, name, obj):

        self.objects[name] = obj

    def get_object(self, name):

        return self.objects[name]

    def events(self, events):

        for event in events:

            if event.type == pg.MOUSEMOTION:
                if pg.mouse.get_pressed()[0] and self.mouse_in:
                    self._offset += from_iterable(event.rel)
            # elif event.type == pg.MOUSEBUTTONDOWN and self.mouse_in:
            #     if event.button == 4:
            #         self.__offset += Vector(20 * int(self.parent.parent.shift_pressed), 20 * int(not self.parent.parent.shift_pressed))
            #     if event.button == 5:
            #         self.__offset -= Vector(20 * int(self.parent.parent.shift_pressed), 20 * int(not self.parent.parent.shift_pressed))

    def get_mouse_position(self):

        return (from_iterable(get_mouse_pos()) - self.pos).as_tuple()

    def update(self):

        self.mouse_in = self._rect.collidepoint(get_mouse_pos())

        for obj in self.objects.values():

            obj.update(self._offset.as_tuple(), self.get_mouse_position)

    def draw(self):

        self._surf.fill("#000000")

        if self.bg_image:
            for y in range(ceil(self.size.y / self.bg_image.get_height()) + 1):
                for x in range(ceil(self.size.x / self.bg_image.get_width()) + 1):
                    pos = from_iterable(self.bg_image.get_size()) * Vector(x, y) + \
                          Vector(self._offset.x % self.bg_image.get_width(),
                                 self._offset.y % self.bg_image.get_height()) - \
                          from_iterable(self.bg_image.get_size())
                    self._surf.blit(self.bg_image, pos.as_tuple())

        for obj in self.objects.values():

            obj.draw(self._surf)

        # pg.draw.rect(self._surf, "#ff0000", (0, 0, self._surf.get_width(), self._surf.get_height()), 5)
        screen.blit(self._surf, self.pos.as_tuple())


class UI(ABC):

    def __init__(self, parent):

        self.parent = parent

    @abstractmethod
    def draw(self, display):

        pass

    @abstractmethod
    def update(self, obj):

        pass

    @abstractmethod
    def events(self, events):

        pass


def print_item_data(dest, pos: tuple, name, tooltip_obj: Text):
    border_width = 5
    text_surf = BIG_FONT.render(name, True, "#ffffff")
    text_pos = Vector(pos[0] + border_width, pos[1] + border_width)
    tooltip_surf = tooltip_obj.surface
    tooltip_pos = Vector(pos[0] + border_width, pos[1] + border_width * 2 + text_surf.get_height())
    rect = pg.Rect(pos[0], pos[1], (text_surf.get_width() if text_surf.get_width() > tooltip_surf.get_width() else tooltip_surf.get_width()) + border_width * 2, text_surf.get_height() + tooltip_surf.get_height() + border_width * 2)
    img = pg.Surface(rect.size)
    img.fill("#000000")
    img.set_alpha(150)
    vector_add = Vector(0, -img.get_height() if pos[1] + img.get_height() > RESOLUTION.y else 0)
    dest.blit(img, (from_iterable(pos) + vector_add).as_tuple())
    dest.blit(text_surf, (text_pos + vector_add).as_tuple())
    dest.blit(tooltip_surf, (tooltip_pos + vector_add).as_tuple())


def print_liquid_data(dest, pos: tuple, name, amount, max_amount, tooltip_obj: Text):
    border_width = 5
    text_surf = FONT.render(name, True, "#ffffff")
    text_pos = (pos[0] + border_width, pos[1] + border_width)
    tooltip_surf = tooltip_obj.surface
    tooltip_pos = (pos[0] + border_width, pos[1] + border_width * 2 + text_surf.get_height())
    amount_surf = FONT.render(f"{amount}L / {max_amount}L", True, "#ffffff")
    amount_pos = (pos[0] + border_width, pos[1] + border_width * 3 + text_surf.get_height() + tooltip_surf.get_height())
    rect = pg.Rect(pos[0], pos[1], (max([text_surf.get_width(), tooltip_surf.get_width(), amount_surf.get_width()])) + border_width * 2, text_surf.get_height() + tooltip_surf.get_height() + amount_surf.get_height() + border_width * 4)
    img = pg.Surface(rect.size)
    img.fill("#000000")
    img.set_alpha(150)
    dest.blit(img, pos)
    dest.blit(text_surf, text_pos)
    dest.blit(tooltip_surf, tooltip_pos)
    dest.blit(amount_surf, amount_pos)
