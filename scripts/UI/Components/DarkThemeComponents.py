from scripts.UI.Components.BaseUIComponents import *
import string
from copy import deepcopy


ENTER_SOUND = pg.mixer.Sound("sound/enter.wav")


class TextButton:

    def __init__(self, pos: Vector, width: int, text: str, height: int = None, fixed_text_pos: bool = False,
                 selected: bool = False, font: pg.font.Font = HUGE_FONT, text_pos: str = "left",
                 text_color: str = "#ffffff"):

        self.pos = pos
        self.rect = pg.Rect(pos.x, pos.y, width, height if height else font.get_height())
        self.text = text
        self.fixed_text_pos = fixed_text_pos
        self.selected = selected
        self.font = font
        self.screen_pos = Vector(0, 0)
        self.text_screen_pos = (0, 0)
        self.text_color = text_color

        self.touching = False
        self.just_touched = False
        self.was_touching = False
        self.just_pressed = False
        self.pressed = False

        if text_pos == "left":
            self.text_pos = pos + Vector(20, font.get_height() * 0.1)
        elif text_pos == "right":
            srf = self.font.render(f"{('▶ ' if self.touching else '  ') if not self.fixed_text_pos else ''}{self.text}", True, self.text_color)
            self.text_pos = pos + Vector(self.rect.width, 0) - Vector(srf.get_width(), font.get_height() * -0.1)
        elif text_pos == "center":
            srf = self.font.render(f"{('▶ ' if self.touching else '  ') if not self.fixed_text_pos else ''}{self.text}",
                             True, self.text_color)
            self.text_pos = pos + Vector(self.rect.width / 2, 0) - Vector(srf.get_width() / 2, font.get_height() * -0.1)

    def update(self, offset: tuple = (0, 0), get_mouse_position: callable = get_mouse_pos):

        self.screen_pos = (
            self.pos.x + offset[0],
            self.pos.y + offset[1],
        )
        self.text_screen_pos = (
            self.text_pos.x + offset[0],
            self.text_pos.y + offset[1],
        )
        self.rect.x, self.rect.y = self.screen_pos

        if self.just_pressed:
            self.just_pressed = False

        self.touching = self.rect.collidepoint(get_mouse_position())
        mouse_pressed = pg.mouse.get_pressed()[0]

        if not mouse_pressed and self.pressed:
            self.just_pressed = True

        if self.touching and mouse_pressed and not self.pressed:
            self.pressed = True
        elif not (self.touching and mouse_pressed):
            self.pressed = False

        if self.touching and not self.was_touching:
            self.just_touched = True
        else:
            self.just_touched = False

        self.was_touching = self.touching

    def draw(self, dest=screen) :

        if self.fixed_text_pos :
            bg_color = "#202020" if self.touching else ("#404040" if self.selected else "#000000")
        else :
            bg_color = "#000000"

        pg.draw.rect(dest, bg_color, self.rect)

        text_to_render = f"{('> ' if self.touching else '  ') if not self.fixed_text_pos else ''}{self.text}"
        rendered_text = self.font.render(text_to_render, True, self.text_color)
        dest.blit(rendered_text, self.text_screen_pos)

        if self.just_touched:
            # SELECT_SOUND.stop()
            SELECT_SOUND.play()


class TextInput:

    def __init__(self, pos: Vector, parent, font: pg.font.Font, text_limit: int, placeholder_text: str = "",
                 avilable_chars=None,):

        self.pos = pos
        self.parent = parent
        self.text_limit = text_limit
        self.font = font
        self.rect = self.font.render("#"*(text_limit+1), True, "#ffffff").get_rect()
        self.rect.x, self.rect.y = pos.as_tuple()
        self.rect.h *= 1.3
        self.placeholder = placeholder_text
        self.avilable_chars = avilable_chars
        self.cursor_pos = 0

        self.text = ""
        self.button = Button(BUTTON, None, "", self.rect.size,
                             self.pos.as_tuple())
        self.button2 = Button(BUTTON, None, "", self.rect.size,
                              self.pos.as_tuple(), invert_rect=True)
        self.active = False

    def update(self, offset: Vector = Vector(0, 0), get_mouse_position=get_mouse_pos):

        self.button.update(offset.as_tuple(), get_mouse_position)
        if self.button.just_pressed:
            self.active = not self.active
            if self.active:
                self.cursor_pos = len(self.text)

        self.button2.update(offset.as_tuple(), get_mouse_position)
        if self.button2.just_pressed:
            self.active = False

    def events(self, events):

        if self.active:
            for event in events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.active = False
                    #elif event.key == pg.K_c and pg.key.get_pressed()[pg.K_LCTRL]:
                    #    pyperclip.copy(self.text)
                    #    print("copy")
                    #elif event.key == pg.K_v and pg.key.get_pressed()[pg.K_LCTRL]:
                    #    self.text = pyperclip.paste()
                    #    self.cursor_pos = len(self.text)
                    #elif event.key == pg.K_x and pg.key.get_pressed()[pg.K_LCTRL]:
                    #    pyperclip.copy(self.text)
                    #    self.text = ""
                    #    self.cursor_pos = 0
                    elif event.key == pg.K_BACKSPACE and self.cursor_pos != 0:
                        if len(self.text):
                            self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                            self.cursor_pos -= 1
                    elif event.key == pg.K_DELETE:
                        self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
                    elif event.key == pg.K_LEFT:
                        self.cursor_pos -= 1
                        if self.cursor_pos < 0:
                            self.cursor_pos = len(self.text)
                    elif event.key == pg.K_RIGHT:
                        self.cursor_pos += 1
                        if self.cursor_pos >= len(self.text) + 1:
                            self.cursor_pos = 0
                    elif ((self.avilable_chars is None or event.unicode in self.avilable_chars) and len(self.text) <
                          self.text_limit and event.key not in [pg.K_LSHIFT, pg.K_LCTRL, pg.K_BACKSPACE]):
                        self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                        self.cursor_pos += 1
                    if event.key not in [pg.K_LSHIFT, pg.K_LCTRL]:
                        SELECT_SOUND.stop()
                        SELECT_SOUND.play()

    def draw(self, dest=screen):

        text_surf = self.font.render(self.text, True, "#ffffff")
        if self.text or self.active:
            dest.blit(text_surf, self.pos.as_tuple())
        else:
            dest.blit(self.font.render(self.placeholder, True, "#404040"), self.pos.as_tuple())
        line_rect = (self.pos.x, self.pos.y + self.rect.height, self.rect.width, 10)
        pg.draw.rect(dest, "#ffffff", line_rect)
        if self.active:
            text_before_texture = self.font.render(self.text[:self.cursor_pos], True, "#ffffff")
            pg.draw.rect(dest, "#ffffff", (self.pos.x + text_before_texture.get_width(),
                                           self.pos.y, 10, text_surf.get_height()))

    def reset(self):

        self.text = ""
        self.active = False


class ImageRadiobutton:

    def __init__(self, pos: Vector, button_size: Vector, options: tuple[tuple[pg.Surface, str], ...]):

        self.pos = pos
        self.options_data = options
        self.options = [TextButton(Vector(self.pos.x + button_size.x * i, self.pos.y), button_size.x,
                                   "", height=button_size.y, fixed_text_pos=True) for i,
                                    (texture, name) in enumerate(self.options_data)]
        self.selected = None

    def draw(self):

        for i, btn in enumerate(self.options):
            btn.draw()
            texture = self.options_data[i][0]
            texture_pos = btn.pos + Vector(btn.rect.width / 2 - texture.get_width() / 2,
                                           btn.rect.height / 2 - texture.get_height() / 2)
            screen.blit(texture, texture_pos.as_tuple())
            if self.selected == i:
                pg.draw.rect(screen, "#ffffff", btn.rect, 5)

        for i, btn in enumerate(self.options):
            if btn.touching:
                print_data(screen,
                           (from_iterable(get_mouse_pos()) + from_iterable(TEXT_MOUSE_OFFSET)).as_tuple(),
                           self.options_data[i][1], BIG_FONT)

    def update(self):

        for i, btn in enumerate(self.options):
            btn.update()
            if btn.just_pressed: self.selected = i

    def reset(self):

        self.selected = None


class Scrollable:

    def __init__(self, pos: Vector, size: Vector, constant_offset: Vector = Vector(0, 0)):

        self.pos = pos
        self.size = size
        self.rect = pg.Rect(pos.x, pos.y, size.x, size.y)
        self._elements = dict()
        self.mouse_in = False
        self.offset = deepcopy(constant_offset)
        self.constant_offset = constant_offset
        self.surf = pg.Surface(self.size.as_tuple())

    def clear(self):

        self._elements = dict()

    def append_element(self, name, element):

        self._elements[name] = element

    def get_element(self, name):

        return self._elements[name]

    def get_elements(self):

        return self._elements.items()

    def get_mouse_position(self):

        if self.mouse_in:
            return (from_iterable(get_mouse_pos()) - self.pos).as_tuple()
        else:
            return (from_iterable(get_mouse_pos()) * Vector(100_000, 100_000)).as_tuple()

    def events(self, events):

        for element_name, element in self.get_elements():
            if hasattr(element, "events") and callable(getattr(element, "events")):
                print(element)
                element.events(events)

        for event in events:

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_WHEELUP:
                    self.offset.y += 50
                elif event.button == pg.BUTTON_WHEELDOWN:
                    self.offset.y -= 50
                if self.offset.y > self.constant_offset.y: self.offset.y = self.constant_offset.y

    def update(self):

        self.mouse_in = self.rect.collidepoint(get_mouse_pos())

        for obj in self._elements.values():
            obj.update(self.offset.as_tuple(), self.get_mouse_position)

    def draw(self):

        self.surf.fill("#000000")

        for obj in self._elements.values():
            obj.draw(self.surf)

        screen.blit(self.surf, self.pos.as_tuple())

        pg.draw.rect(screen, "#333333", (self.pos.x, self.pos.y - 5, self.size.x, 5))
        pg.draw.rect(screen, "#333333", (self.pos.x, self.pos.y + self.size.y, self.size.x, 5))

        # pg.draw.rect(screen, "#ff0000", self.rect, 5)


class ImageButton:

    BORDER_WIDTH = 50

    def __init__(self, pos: Vector, size: Vector, image: pg.Surface, selected: bool = False):

        self.pos = pos
        self.size = size
        self.image = image
        self.selected = selected

        self.screen_pos = (0, 0)
        self.rect = pg.Rect(pos.x, pos.y, size.x, size.y)
        self.touching = False
        self.just_touched = False
        self.was_touching = False
        self.just_pressed = False
        self.pressed = False

    def update(self, offset: tuple = (0, 0), get_mouse_position: callable = get_mouse_pos):

        self.screen_pos = (
            self.pos.x + offset[0],
            self.pos.y + offset[1],
        )
        self.rect.x, self.rect.y = self.screen_pos

        if self.just_pressed:
            self.just_pressed = False

        self.touching = self.rect.collidepoint(get_mouse_position())
        mouse_pressed = pg.mouse.get_pressed()[0]

        if not mouse_pressed and self.pressed:
            self.just_pressed = True

        if self.touching and mouse_pressed and not self.pressed:
            self.pressed = True
        elif not (self.touching and mouse_pressed):
            self.pressed = False

        if self.touching and not self.was_touching:
            self.just_touched = True
        else:
            self.just_touched = False

        self.was_touching = self.touching

    def draw(self, dest=screen):

        bg_color = "#202020" if self.touching else ("#404040" if self.selected else "#000000")
        pg.draw.rect(dest, bg_color, self.rect)
        dest.blit(self.image, (from_iterable(self.screen_pos) +
                               Vector(self.BORDER_WIDTH, self.BORDER_WIDTH)).as_tuple())

        if self.just_touched:
            SELECT_SOUND.stop()
            SELECT_SOUND.play()


class SaveButton(TextButton):

    def __init__(self, pos, name: str, width, screenshot: pg.Surface, selected):

        super().__init__(pos, width, name, fixed_text_pos=True, selected=selected, font=HUGEISH_FONT, height=200)
        screenshot_size = (int(((self.rect.height - 20) * screenshot.get_width()) / screenshot.get_height()), self.rect.height - 20)
        self.screenshot = pg.transform.scale(screenshot, screenshot_size)
        self.screenshot_pos = (0, 0)

    def update(self, offset: tuple = (0, 0), get_mouse_position: callable = get_mouse_pos):

        super().update(offset, get_mouse_position)

        self.screenshot_pos = (
            self.pos.x + 10 + offset[0],
            self.pos.y + 10 + offset[1],
        )

    def draw(self, dest=screen):

        if self.fixed_text_pos :
            bg_color = "#202020" if self.touching else ("#404040" if self.selected else "#000000")
        else :
            bg_color = "#000000"

        pg.draw.rect(dest, bg_color, self.rect)

        dest.blit(self.screenshot, self.screenshot_pos)

        text_to_render = f"{('> ' if self.touching else '    ') if not self.fixed_text_pos else ''}{self.text}"
        rendered_text = self.font.render(text_to_render, True, "#ffffff")
        dest.blit(rendered_text, (from_iterable(self.text_screen_pos) + Vector(self.screenshot.get_width() + 10, 5)).as_tuple())

        if self.just_touched :
            SELECT_SOUND.stop()
            SELECT_SOUND.play()
