from PgHelp import *
from dataclasses import dataclass, field
from scripts.constants import *


@dataclass
class AchievementVisualData:

    pos: Vector
    size: Vector = ACHIEVENT_SIZE


@dataclass
class Achievement:

    name: str
    description: str
    icon: str
    req: tuple[str, str | list[str] | None]
    visual_data: AchievementVisualData
    parent: int | None
    fixed_arrow: bool = False
