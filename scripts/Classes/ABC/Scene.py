import pygame as pg


class Scene:

    def __init__(self, parent):

        self.parent = parent

    def handle_events(self, events: list[pg.event.Event]):

        pass

    def update(self):

        pass

    def draw(self):

        pass
