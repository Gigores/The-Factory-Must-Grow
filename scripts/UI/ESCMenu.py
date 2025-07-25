from scripts.UI.Components.BaseUIComponents import *
from scripts.constants import *
from scripts.Classes.Registry.UIRegistry import UIRegistry


class ESCMenu(metaclass=UIRegistry):

    def __init__(self, parent):

        self.parent = parent

        button_size = Vector(RESOLUTION.x / 3, RESOLUTION.y / 16)
        central_button_pos = Vector(RESOLUTION.x / 2 - button_size.x / 2, RESOLUTION.y / 2 - button_size.y / 2)
        spacing = 32
        self.buttons = dict()

        pos = central_button_pos + Vector(0, -(button_size.y + spacing))
        self.buttons["back_to_game"] = Button(BUTTON, BUTTON_PRESSED, "Back to game", button_size.as_tuple(), pos.as_tuple())

        pos = central_button_pos
        self.buttons["save_and_quit"] = Button(BUTTON, BUTTON_PRESSED, "Save", button_size.as_tuple(), pos.as_tuple())

        pos = central_button_pos + Vector(0, button_size.y + spacing)
        self.buttons["save_and_quit_to_title"] = Button(BUTTON, BUTTON_PRESSED, "Quit to main menu", button_size.as_tuple(), pos.as_tuple(), activa_on_up=True)

    def events(self, events):

        pass

    def update(self, obj):

        for button in self.buttons.values():
            button.update()

        if self.buttons["back_to_game"].just_pressed:
            self.parent.active_ui_id = None
            self.parent.active_object_ui = None

        if self.buttons["save_and_quit"].just_pressed:
            self.parent.saves_manager.save()

        if self.buttons["save_and_quit_to_title"].just_pressed:
            self.parent.save_and_quit_to_title()

    def draw(self, display):

        for button in self.buttons.values():
            button.draw()
