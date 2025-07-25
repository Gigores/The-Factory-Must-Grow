import pygame as pg
from dataclasses import dataclass, field
from PgHelp import *
from scripts.constants import *
from typing import Literal


@dataclass
class Item:

    name: str
    stack_size: int
    texture_path: str

    tooltip: str
    tags: list[str] = field(default_factory=list)
    animated_texture: bool = False

    texture: pg.Surface | list[pg.Surface] = field(init=False, default=pg.Surface((1, 1)))

    def __post_init__(self):
        self.texture = pg.image.load(self.texture_path)


@dataclass
class Tool:

    name: str
    texture_path: str
    type_: str
    damage: int
    stack_size: int
    dont_need_clicking: bool

    tooltip: str
    tags: list[str] = field(default_factory=list)
    animated_texture: bool = False

    texture: pg.Surface = field(init=False, default=pg.Surface((1, 1)))

    def __post_init__(self):

        self.texture = pg.image.load(self.texture_path)


@dataclass
class BuildingItem:

    name: str
    stack_size: int
    texture_path: str
    entity: str
    available_tiles: list

    tooltip: str
    tags: list[str] = field(default_factory=list)
    animated_texture: bool = False

    texture: pg.Surface = field(init=False, default=pg.Surface((1, 1)))

    def __post_init__(self):

        self.texture = pg.image.load(self.texture_path)


@dataclass
class PlaceableTile:

    name: str
    stack_size: int
    texture_path: str
    tile_id: int
    item_deleting: bool
    unchangeable_tiles: list
    avilable_tiles: list
    display_tile: bool

    tooltip: str
    tags: list[str] = field(default_factory=list)
    animated_texture: bool = False

    texture: pg.Surface = field(init=False, default=pg.Surface((1, 1)))

    def __post_init__(self):

        self.texture = pg.image.load(self.texture_path)


@dataclass
class Food:

    name: str
    stack_size: int
    texture_path: str
    saturation_level: int
    affects: Literal["health", "hunger"]

    tooltip: str
    tags: list[str] = field(default_factory=list)
    animated_texture: bool = False

    texture: pg.Surface = field(init=False, default=pg.Surface((1, 1)))

    def __post_init__(self):

        self.texture = pg.image.load(self.texture_path)
