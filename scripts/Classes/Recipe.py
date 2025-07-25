import logging
from dataclasses import dataclass

from scripts.constants import items


@dataclass
class WorkbenchRecipe:

    ingredient1: (str, int)
    ingredient2: (str, int)
    result: (str, int)


@dataclass
class EngineeringWorkbenchRecipe:

    ingredients: list[list[str, int], ...]
    result: (str, int)


@dataclass
class FurnaceRecipe:

    ingredient: (str, int)
    result: (str, int)
    weight: int


@dataclass
class AnvilRecipe:

    ingredient: (str, int)
    result: (str, int)


@dataclass
class CrusherRecipe:

    ingredient: (str, int)
    result: (str, int)
    time: int
    particle_type: str


@dataclass
class MagneticCentrifugeRecipe:

    ingredient: (str, int)
    result1: (str, int)
    result2: (str, int)
    time: int


@dataclass
class WoodworkingMachineRecipe:

    ingredient: (str, int)
    result: (str, int)
    time: int


@dataclass
class CokeOvenRecipe:

    ingredient: (str, int)
    result: (str, int)
    time: int


@dataclass
class FoundryRecipe:

    ingredient_tag: str
    mold: str
    result: str
    weight: int


@dataclass
class ChemicalReactorRecipe:

    input_liquids: list[list[str, int], ...]
    input_items: list[list[str, int], ...]
    time: int
    output_liquids: list[list[str, int], ...]
    output_items: list[list[str, int], ...]
    formula: str
    color: str
    icon_item: str
    name: str


class WorkbenchRecipeManager(dict):

    def __init__(self):

        super().__init__()

    def append(self, recipe: WorkbenchRecipe, category: str, subcategory: int):

        if not (category in self.keys()):
            self[category] = dict()

        if not (subcategory in self[category].keys()):
            self[category][subcategory] = list()

        self[category][subcategory].append(recipe)

    def find(self, ingredient1: str, amount1: int, ingredient2: str, amount2: int) -> WorkbenchRecipe | None:

        for category in self.values():
            for subcategory in category.values():
                for recipe in subcategory:

                    is_equal = (recipe.ingredient1[0] == ingredient1 and amount1 >= recipe.ingredient1[1]
                                and recipe.ingredient2[0] == ingredient2 and amount2 >= recipe.ingredient2[1])
                    if is_equal: return recipe
                    else: continue

        return None


class EngineeringWorkbenchRecipeManager(dict):

    def __init__(self):

        super().__init__()

    def append(self, recipe: EngineeringWorkbenchRecipe, category: str, subcategory: int):

        if not (category in self.keys()):
            self[category] = dict()

        if not (subcategory in self[category].keys()):
            self[category][subcategory] = list()

        self[category][subcategory].append(recipe)

    @staticmethod
    def _validate_items(names: list[str], quantities: list[int], check_list: list[list]) -> bool :
        expected_items = {name : (qty if qty is not None else 0) for name, qty in zip(names, quantities) if
                          name is not None}

        for item_name, item_qty in check_list :
            if item_name is None or item_name not in expected_items or item_qty != expected_items[item_name] :
                return False

        check_list_names = {item[0] for item in check_list if item[0] is not None}
        if set(expected_items.keys()) != check_list_names :
            return False

        return True

    def find(self, ingredient_names: list[str], ingredient_amounts: list[int]) -> EngineeringWorkbenchRecipe | None:

        for category in self.values():
            for subcategory in category.values():
                for recipe in subcategory:

                    if self._validate_items(ingredient_names, ingredient_amounts, recipe.ingredients):
                        return recipe

        return None


class FurnaceRecipeManager(list):

    def __init__(self):

        super().__init__()

    def find(self, ingredient: str) -> FurnaceRecipe | None:

        for recipe in self:

            is_equal = recipe.ingredient[0] == ingredient
            if is_equal:
                return recipe
            else: continue

        return None


class AnvilRecipeManager(list):

    def __init__(self):

        super().__init__()

    def find(self, ingredient: str) -> AnvilRecipe | None:

        for recipe in self:

            is_equal = recipe.ingredient[0] == ingredient
            if is_equal: return recipe
            else: continue

        return None


class CrusherRecipeManager(list):

    def __init__(self):

        super().__init__()

    def find(self, ingredient: str) -> CrusherRecipe | None:

        for recipe in self:

            is_equal = recipe.ingredient[0] == ingredient
            if is_equal: return recipe
            else: continue

        return None


class MagneticCentrifugeManager(list):

    def __init__(self):

        super().__init__()

    def find(self, ingredient: str) -> MagneticCentrifugeRecipe | None:

        for recipe in self:

            is_equal = recipe.ingredient[0] == ingredient
            if is_equal: return recipe
            else: continue

        return None


class WoodworkingMachineRecipeManager(list):

    def __init__(self):

        super().__init__()

    def find(self, ingredient: str) -> CrusherRecipe | None:

        for recipe in self:

            is_equal = recipe.ingredient[0] == ingredient
            if is_equal: return recipe
            else: continue

        return None


class CokeOvenRecipeManager(list):

    def __init__(self):

        super().__init__()

    def find(self, ingredient: str) -> CrusherRecipe | None:

        for recipe in self:

            is_equal = recipe.ingredient[0] == ingredient
            if is_equal: return recipe
            else: continue

        return None


class FoundryRecipeManager(list):

    def __init__(self):

        super().__init__()

    def find(self, ingredient: str, mold: str) -> FoundryRecipe | None:

        for recipe in self:

            is_equal = (recipe.ingredient_tag in items[ingredient].tags) and recipe.mold == mold
            if is_equal: return recipe
            else: continue

        return None


class ChemicalReactorRecipeManager(list):

    pass
