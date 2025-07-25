import pygame as pg

from scripts.Classes.ABC.Scene import Scene
from scripts.Classes.Registry.SceneRegistry import SceneRegistry


class MainMenuScene(Scene, metaclass=SceneRegistry):

    def __init__(self, parent):

        super().__init__(parent)

    def handle_events(self, events: list[pg.event.Event]):

        for event in events:

            if event.type == pg.QUIT:
                self.parent.running = False

        self.parent.main_menu.events(events)

    def update(self):

        self.parent.main_menu.update()

    def draw(self):

        self.parent.main_menu.draw()
