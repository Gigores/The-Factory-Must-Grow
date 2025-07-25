from copy import deepcopy
from scripts.UI.Components.BaseUIComponents import *
from scripts.UI.Components.Bg import Bg
from scripts.Managers.GameAssets import *
from scripts.Classes.Registry.UIRegistry import UIRegistry
from .Enterpreter import Enterpreter


class Terminal:

    def __init__(self, parent, size: Vector, pos: Vector):

        self.parent = parent
        self.size = size
        self.pos = pos
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

        self.entepreter = Enterpreter(self)
        self.surf = pg.Surface(self.size.as_tuple())
        self.font = pg.font.Font("assets/commodore.ttf", 30)
        self.lines = []
        self.current_text = ""
        self.cursor_pos = 0
        self.cursor2_pos = 0
        self.last_text = None
        self.prompts = []
        self.command_list = [
            ("set_player_speed", "num"),
            ("teleport", "num", "num"),
            ("set_health", "num"),
            ("set_hunger", "num"),
            ("damage", "num"),
            ("kill",),
            ("get_item", "item", "num"),
            ("save_as", "str"),
            ("spawn", "entity", "num", "num"),
            ("use_collisions", "bool"),
            ("set_tile", "tile", "num", "num"),
            ("help", "help"),
            ("list", "data"),
        ]
        self.current_program = {}
        self.command_history = []
        self.command_history_cursor = 0

        self.error_sound = pg.mixer.Sound("sound/terminal_error.wav")

        self.print(f'TheFactoryMustGrow {GAME_VERSION}\ntype "help" to get a\nlist of commands\n ')

    def draw(self):

        self.surf.fill("#000000")

        font = self.font

        max_lines = self.size.y // font.get_height() - 1

        for i, line in enumerate(reversed(self.lines[:self.cursor2_pos])):
            pos = Vector(10, (max_lines - (i + 2)) * font.get_height())
            self.surf.blit(font.render(line, True, "#00ff00"), pos.as_tuple())

        # biggest_command_size = max(len(i[0]) for i in self.command_list) + 1
        # if len(self.current_text) and len(self.prompts):
        #     width = font.render("a"*biggest_command_size, True, "#ffffff").get_width() + 5
            #     height = len(self.prompts) * font.get_height() + 10
            # pg.draw.rect(self.surf, "#000000", (5, (max_lines - (len(self.prompts) + 1)) * font.get_height() - 5, width, height))
            # pg.draw.rect(self.surf, "#00ff00", (5, (max_lines - (len(self.prompts) + 1)) * font.get_height() - 5, width, height), 3)
            # for i, prompt in enumerate(self.prompts):
                # pos = Vector(10, (max_lines - (i + 2)) * font.get_height())
                # surf1 = font.render(self.current_text.split()[0], True, "#00ff00", "#005500")
                # surf2 = font.render(prompt[len(self.current_text.split()[0]):].strip(), True, "#00ff00", "#000000")
                # self.surf.blit(surf1, pos.as_tuple())
                # self.surf.blit(surf2, (pos + Vector(surf1.get_width(), 0)).as_tuple())

        text_pos = Vector(10, self.size.y - font.get_height() * 1.5)
        self.surf.blit(font.render(self.current_text, True, "#00ff00"), text_pos.as_tuple())
        if self.parent.animation_counter % 120 > 60:
            self.surf.blit(font.render("_", True, "#00ff00"), (text_pos.x + self.font.render(self.current_text[0:self.cursor_pos], True, "#00ff00").get_width(), text_pos.y))
        # pg.draw.rect(self.surf, "#00ff00", (text_pos.x + self.font.render(self.current_text[0:self.cursor_pos], True, "#00ff00").get_width(), text_pos.y, 5, font.get_height()))

        screen.blit(self.surf, self.pos.as_tuple())

    def update(self):

        self.prompts = [item[0] for item in self.command_list if item[0].startswith(self.current_text.split()[0])] if self.current_text else []

    def events(self, events):

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE and self.cursor_pos != 0:
                    if len(self.current_text):
                        self.current_text = self.current_text[:self.cursor_pos - 1] + self.current_text[self.cursor_pos:]
                        self.cursor_pos -= 1
                elif event.key == pg.K_DELETE:
                    self.current_text = self.current_text[:self.cursor_pos] + self.current_text[self.cursor_pos + 1:]
                elif event.key == pg.K_LEFT:
                    self.cursor_pos -= 1
                    if self.cursor_pos < 0:
                        self.cursor_pos = len(self.current_text)
                elif event.key == pg.K_RIGHT:
                    self.cursor_pos += 1
                    if self.cursor_pos >= len(self.current_text) + 1:
                        self.cursor_pos = 0
                elif event.key == pg.K_RETURN:
                    self.print(f"> {self.current_text}")
                    self.command_history.append(self.current_text)
                    self.command_history_cursor = len(self.command_history) - 1
                    self.entepreter.execute_input(self.current_text)
                    self.cursor_pos = 0
                    self.current_text = ""
                elif event.key not in [pg.K_LSHIFT, pg.K_LCTRL, pg.K_RETURN, pg.K_UP, pg.K_DOWN, pg.K_BACKSPACE] and event.unicode:
                    self.current_text = self.current_text[:self.cursor_pos] + event.unicode + self.current_text[self.cursor_pos:]
                    self.cursor_pos += 1
                elif event.key == pg.K_UP and len(self.command_history):
                    if self.parent.ctrl_pressed:
                        self.cursor2_pos -= 1
                    else:
                        if self.command_history_cursor > -1:
                            self.current_text = self.command_history[self.command_history_cursor]
                            self.command_history_cursor -= 1
                            self.cursor_pos = len(self.current_text)
                elif event.key == pg.K_DOWN:
                    if self.parent.ctrl_pressed:
                        if self.cursor2_pos < len(self.lines):
                            self.cursor2_pos += 1
                    else:
                        pass
                        # if self.command_history_cursor < len(self.command_history):
                        #     self.command_history_cursor += 1
                        #     self.current_text = self.command_history[self.command_history_cursor]
                        #     self.cursor_pos = len(self.current_text)
                if event.key not in [pg.K_LSHIFT, pg.K_LCTRL, pg.K_RETURN, pg.K_UP, pg.K_DOWN]:
                    SELECT_SOUND.stop()
                    SELECT_SOUND.play()

    def print(self, text):

        lines = text.split("\n")
        lines = [piece for l in lines for piece in [l[i:i+43] for i in range(0, len(l), 35)]]
        self.lines += lines
        self.cursor2_pos += len(lines)

    def throw_error(self, e: Exception):

        self.error_sound.play()
        args = ""
        for arg in e.args: args += arg
        self.print(f"? {e.__class__.__name__}: {args}")


class TerminalWindow(metaclass=UIRegistry):

    def __init__(self, parent):

        self.parent = parent

        self.main_ui_size = from_iterable(BLANK.get_size()) * Vector(2, 2)
        self.main_ui_texture = pg.transform.scale(BLANK, self.main_ui_size.as_tuple())
        self.main_ui_pos = RESOLUTION / Vector(2, 2) - Vector(self.main_ui_size.x, self.main_ui_size.y) / Vector(2, 2)

        terminal_pos = self.main_ui_pos+from_iterable(self.main_ui_texture.get_size()) * Vector(0.122222222, 0.1617647059)
        terminal_size = from_iterable(self.main_ui_texture.get_size()) * Vector(0.755555556, 0.5294117647)
        self.terminal = Terminal(self.parent, terminal_size, terminal_pos)

        self.WHITE_NOISE = [load_texture(f"assets/ingame_UI/white_noise/white_noise-{i}.png", terminal_size) for i in range(6)]
        for texture in self.WHITE_NOISE:
            texture.set_alpha(32)

        # self.mask1 = pg.Surface((self.main_ui_size-Vector(60, 60)).as_tuple())
        # self.mask1.blit(self.main_ui_texture, (-30, -30))
        # pg.draw.rect(self.mask1, "#000000", (0, 0, self.mask1.get_width(), self.mask1.get_height()), border_radius=30)
        # self.mask1.set_colorkey("#000000")

        terminal_texture = load_texture("assets/ingame_UI/terminal.png", from_iterable(self.main_ui_texture.get_size()))

        self.bg = Bg()
        self.bg.blit(terminal_texture, self.main_ui_pos.as_tuple())

    def draw(self, display):

        self.bg.draw()
        self.terminal.draw()
        screen.blit(self.WHITE_NOISE[self.parent.animation_counter // 5 % len(self.WHITE_NOISE)], self.terminal.pos.as_tuple())
        # screen.blit(self.mask1, self.terminal.pos.as_tuple())

    def update(self, obj):

        self.terminal.update()

    def events(self, events):

        self.terminal.events(events)
