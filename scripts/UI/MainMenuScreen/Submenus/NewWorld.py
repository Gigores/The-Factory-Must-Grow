import pygame as pg
from scripts.UI.MainMenuScreen.Submenu import Submenu
from scripts.constants import *
from scripts.UI.Components.DarkThemeComponents import TextButton, CLICK_SOUND, TextInput, ImageRadiobutton, ENTER_SOUND
from random import randint
from scripts.Classes.Registry.SubmenuRegistry import SubmenuRegistry


class NewWorld(Submenu, metaclass=SubmenuRegistry):

    def __init__(self, parent, rect_width):

        super().__init__(parent, "new_world")

        self.name_input = TextInput(Vector(0, HUGE_FONT.get_height() * 4), self, HUGE_FONT, 10, "world name")
        self.seed_input = TextInput(Vector(0, HUGE_FONT.get_height() * 5 + 20), self, HUGE_FONT, 8, "seed", str([str(i) for i in range(0, 10)]))
        self.random_seed_btn = TextButton(Vector(self.seed_input.rect.width, self.seed_input.pos.y), rect_width-self.seed_input.rect.width, "R", fixed_text_pos=True)
        islands = (
            (load_texture("assets/icons/classic.png", Vector(130, 130)), "Classic"),
            (load_texture("assets/icons/archipelago.png", Vector(130, 130)), "Archipelago"),
        )
        self.world_type = ImageRadiobutton(Vector(0, self.seed_input.pos.y + self.seed_input.rect.height * 1.5), Vector(150, 150), islands)
        self.done_btn = TextButton(Vector(0, RESOLUTION.y - HUGE_FONT.get_height() * 3), rect_width, "Done")
        self.return_btn_3 = TextButton(Vector(0, RESOLUTION.y - HUGE_FONT.get_height() * 2), rect_width, "Back")

    def events(self, events: list):

        self.name_input.events(events)
        self.seed_input.events(events)

    def update(self):

        self.done_btn.update()
        self.return_btn_3.update()
        self.random_seed_btn.update()

        self.name_input.update()
        self.seed_input.update()
        self.world_type.update()

        if self.done_btn.just_pressed and len(self.name_input.text) > 0 and len(
                self.seed_input.text) > 0 and self.world_type.selected is not None :
            ENTER_SOUND.play()
            seed = int(self.seed_input.text) if not pg.key.get_pressed()[pg.K_LSHIFT] else 0
            self.parent.parent.new_game(self.name_input.text, seed, self.world_type.selected)

        if self.return_btn_3.just_pressed :
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.parent.set_submenu("hub")

        if self.random_seed_btn.just_pressed :
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.seed_input.text = ""
            for i in range(self.seed_input.text_limit) : self.seed_input.text += str(randint(0, 9))

    def draw(self):

        screen.blit(HUGE_FONT.render("New Game", True, "#ffffff"), (0, 60))

        self.name_input.draw()
        self.seed_input.draw()
        self.done_btn.draw()
        self.return_btn_3.draw()
        self.random_seed_btn.draw()
        self.world_type.draw()
