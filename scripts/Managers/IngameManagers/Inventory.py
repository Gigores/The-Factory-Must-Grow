import numpy as np
from math import sin
from scripts.Managers.GameAssets import *

LEFT_TEXTURE = load_texture("assets/inventory_left.png", INVENTORY_SCREEN_SIZE)
CENTER_TEXTURE = load_texture("assets/inventory_center.png", INVENTORY_SCREEN_SIZE)
RIGHT_TEXTURE = load_texture("assets/inventory_right.png", INVENTORY_SCREEN_SIZE)


class Slot:

    def __init__(self):

        self.item_name = None
        self.item_amount = 0

    def append(self, item_name: str, item_amount: int):

        if self.item_name == item_name or self.item_name is None:

            self.item_name = item_name
            self.item_amount += item_amount
            if self.item_amount > items[item_name].stack_size: raise RuntimeError(
                f"Item '{item_name}' amount cant be more than {items[item_name].stack_size}")

        else:
            raise RuntimeError(f"cant put '{item_name}' in slot")

    def pop(self, item_amount: int):

        self.item_amount -= item_amount
        if self.item_amount < 1: self.item_name = None
        if self.item_amount < 0: raise RuntimeError(f"Item amount cant be less than zero")

    def clear(self):

        self.item_amount = 0
        self.item_name = None

    def can_fit(self, item_name: str, item_amount: int = 1) -> bool:

        if item_name == self.item_name or self.item_name is None:
            if self.item_amount + item_amount <= items[item_name].stack_size:
                return True

        return False

    def contain(self, item_name: str, item_amount: int):

        return all((self.item_name == item_name, self.item_amount >= item_amount))

    def dumb(self) -> dict:

        return {
            "amount": int(self.item_amount),
            "name": self.item_name
        }

    def load(self, data: dict):

        self.item_amount = data["amount"]
        self.item_name = data["name"]

    def __repr__(self):

        return f"{self.item_name}: {self.item_amount}"


class Inventory:

    def __init__(self, parent, size: int = INVENTORY_SIZE, *, main: bool = False, log: bool = False):

        self.parent = parent
        self.is_main = main
        self.n = [None for _ in range(size)]
        self.a = np.array([0 for _ in range(size)], dtype=np.uint8)
        self.__animation_counter = 0
        self.last_active = 0
        self.size = size
        self.logging = log

        if self.logging:
            print("initialized:", self.n, self.a)

    def shuffle(self):

        n = len(self.n)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            self.n[i], self.n[j] = self.n[j], self.n[i]
            self.a[i], self.a[j] = self.a[j], self.a[i]

    def sort_by_name(self):

        def get_item_name(item_index):
            return items[item_index].name.lower() if item_index is not None else None

        items_ = zip(self.n, self.a)

        sorted_items = sorted(
            items_,
            key=lambda item: (get_item_name(item[0]) is None, get_item_name(item[0]))
        )

        self.n, self.a = zip(*sorted_items) if sorted_items else ([], [])
        self.n = list(self.n)
        self.a = list(self.a)

    def sort_by_quantity(self):

        items_ = zip(self.n, self.a)

        sorted_items = sorted(
            items_,
            key=lambda item: item[1],
            reverse=True
        )

        self.n, self.a = zip(*sorted_items) if sorted_items else ([], [])
        self.n = list(self.n)
        self.a = list(self.a)

    def append(self, item_name: str, amount: int = 1) :
        if self.logging:
            print("append", item_name, amount)
        for s in range(amount) :
            added = False
            for i, n in enumerate(self.n) :
                if n == item_name and self.a[i] < items[n].stack_size :
                    self.a[i] += 1
                    added = True
                    break
            if not added :
                for i, n in enumerate(self.n) :
                    if n is None :
                        self.n[i] = item_name
                        self.a[i] = 1
                        if self.is_main and item_name not in self.parent.all_got_items :
                            self.parent.all_got_items.append(item_name)
                            self.parent.update_achievements()
                        break

    def append_m(self, items: list[list[str, int], ...]):

        for item, amount in items:
            self.append(item, amount)

    def pop(self, item_name: str, item_amount: int = 1):

        items_to_del = item_amount
        for i, item in enumerate(self.n):
            if item == item_name:
                while self.a[i] > 0 and items_to_del > 0:
                    self.a[i] -= 1
                    items_to_del -= 1
                if self.a[i] == 0:
                    self.n[i] = None

    def pop_m(self, items: list[list[str, int], ...]):

        for item, amount in items:
            self.pop(item, amount)

    def update(self):

        if self.__animation_counter < 1:
            self.__animation_counter += 0.1

    def reset_animation(self):

        self.__animation_counter = 0

    def draw(self):

        for i, (n, a) in enumerate(zip(self.n, self.a)):

            y = INVENTORY_POS.y - (sin(self.__animation_counter) * 15 if i == self.parent.player.inventory_cursor else (
                15 - sin(self.__animation_counter) * 15 if i == self.last_active else 0))
            pos = Vector(INVENTORY_POS.x + i * INVENTORY_SCREEN_SIZE.y, y)
            if i == 0:
                self.parent.screen.blit(LEFT_TEXTURE, pos.as_tuple())
            elif i == self.size - 1:
                self.parent.screen.blit(RIGHT_TEXTURE, pos.as_tuple())
            else:
                self.parent.screen.blit(CENTER_TEXTURE, pos.as_tuple())
            if n:
                self.parent.screen.blit(pg.transform.scale(items[n].texture, INVENTORY_SCREEN_SIZE.as_tuple()), pos.as_tuple())
                if a > 1: write(screen, FONT, f"{a}", pos + INVENTORY_SCREEN_SIZE / Vector(8, 8) * Vector(1.5, 1.5))

    def has(self, item_name: str, item_amount: int) -> bool:

        for n, item in enumerate(self.n):
            if item == item_name and self.a[n] >= item_amount:
                return True

        return False

    def has_m(self, items: list[list[str, int], ...]):

        return all([self.has(item_name, item_amount) for item_name, item_amount in items])

    def can_fit(self, item_name, amount) :

        if amount <= 0 :
            return True

        stack_size = items[item_name].stack_size
        remaining = amount

        for i, (current_item, current_count) in enumerate(zip(self.n, self.a)) :
            if current_item is None :
                remaining -= stack_size
            elif current_item == item_name :
                space_left = stack_size - current_count
                remaining -= space_left

            if remaining <= 0 :
                return True

        empty_slots = self.n.count(None)
        if remaining > 0 and empty_slots > 0 :
            if remaining <= empty_slots * stack_size :
                return True

        return False

    def can_fit_m(self, items_list):
        """
        Проверяет, можно ли разместить все предметы из списка в инвентаре.

        :param items_list: Список предметов в формате [["item_name", item_amount], ...].
        :return: True, если все предметы можно разместить, иначе False.
        """
        # Создаем копии инвентаря для симуляции
        simulated_n = deepcopy(self.n)
        simulated_a = list(self.a)

        for item_name, item_amount in items_list :
            stack_size = items[item_name].stack_size  # Максимальный размер стека предмета
            remaining = item_amount  # Сколько осталось разместить

            for i in range(len(simulated_n)) :
                if simulated_n[i] is None :
                    # Пустая ячейка: можно поместить новый предмет
                    if remaining > 0 :
                        to_add = min(remaining, stack_size)
                        simulated_n[i] = item_name
                        simulated_a[i] = to_add
                        remaining -= to_add
                elif simulated_n[i] == item_name :
                    # Уже занята этим предметом: добавляем в существующий стек
                    space_left = stack_size - simulated_a[i]
                    if space_left > 0 and remaining > 0 :
                        to_add = min(remaining, space_left)
                        simulated_a[i] += to_add
                        remaining -= to_add

                if remaining <= 0 :
                    break

            # Если после всех проверок остались предметы, вернуть False
            if remaining > 0 :
                return False

        # Если все предметы удалось разместить, вернуть True
        return True

    def pop_from_slot(self, slot_id: int, a: int = 1):

        if self.a[slot_id] < a:
            raise RuntimeError(f"too mush to pop from slot {slot_id}")
        else:
            self.a[slot_id] -= a
            if self.a[slot_id] < 1:
                self.n[slot_id] = None

    def dumb(self) -> dict:

        return {
            "amounts": [int(i) for i in self.a],
            "names": [i for i in self.n],
            "is_main": self.is_main
        }

    def load(self, data: dict):

        self.a = np.array(data["amounts"], dtype="uint8")
        self.n = data["names"]
        self.is_main = data["is_main"]
        if self.logging:
            print(list(self.a), self.n, ":", data["amounts"], data["names"])

    def __len__(self):

        return len(self.n)
