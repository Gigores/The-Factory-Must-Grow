class InventoryTank:

    def __init__(self, volume):

        self.max_volume = volume
        self.fill_level = 0
        self.current_liquid = None

    def pump_in(self, liquid_name, liqud_amount):

        if not self.can_pump_in(liquid_name, liqud_amount):
            raise ValueError(f"cant insert liqud {liquid_name}, tank is full of another fluid")

        self.current_liquid = liquid_name
        self.fill_level += liqud_amount

    def can_pump_in(self, liquid_name, liquid_amount):

        if self.current_liquid is None:
            if liquid_amount <= self.max_volume:
                return True
        elif liquid_name == self.current_liquid:
            if self.fill_level + liquid_amount <= self.max_volume:
                return True

        return False

    def pump_out(self, amount):

        if self.fill_level < amount:
            raise ValueError(f"dont have enough fluid to pump out: {amount}")

        self.fill_level -= amount

        if self.fill_level == 0:
            self.current_liquid = None

    def has(self, liquid_name, liquid_amount):

        if liquid_name is None:
            if liquid_amount > self.fill_level:
                return False
            return True

        if liquid_name != self.current_liquid:
            return False

        if liquid_amount > self.fill_level:
            return False

        return True

    def empty(self):

        self.fill_level = 0
        self.current_liquid = None

    def get_fill_percentage(self):

        return (self.fill_level / self.max_volume) * 100

    def dumb(self) -> dict:

        return {
            "name": self.current_liquid,
            "amount": self.fill_level,
            "volume": self.max_volume
        }

    def load(self, data):

        self.current_liquid = data["name"]
        self.fill_level = data["amount"]
        self.max_volume = data["volume"]


class InventiryTankArray(list[InventoryTank]):

    def __init__(self, tanks_amount, tanks_volume):

        super().__init__([InventoryTank(tanks_volume) for _ in range(tanks_amount)])

    def pump_in(self, liquid_name, liquid_amount):

        for tank in self:

            if tank.can_pump_in(liquid_name, liquid_amount):
                tank.pump_in(liquid_name, liquid_amount)
                break

        else:

            raise ValueError(f"cant insert liqud {liquid_name}, tanks are full of another fluid")

    def pump_in_m(self, liquids: list[list[str, int], ...]):

        for liquid, amount in liquids:
            self.pump_in(liquid, amount)

    def can_pump_in(self, liquid_name, liquid_amount):

        for tank in self:

            if tank.can_pump_in(liquid_name, liquid_amount):
                return True

        return False

    def can_pump_in_m(self, liquids: list[list[str, int], ...]):

        return all([self.can_pump_in(liquid_name, liquid_amount) for liquid_name, liquid_amount in liquids])

    def pump_out(self, liquid_name, liquid_amount):

        for tank in self:

            if tank.has(liquid_name, liquid_amount):
                tank.pump_out(liquid_amount)
                break

        else:

            raise ValueError(f"cant insert liqud {liquid_name}, tanks are full of another fluid")

    def pump_out_m(self, liquids: list[list[str, int], ...]):

        for liquid, amount in liquids:
            self.pump_out(liquid, amount)

    def has(self, liquid_name, liquid_amount):

        for tank in self:

            if tank.has(liquid_name, liquid_amount):
                return True

        return False

    def has_m(self, liquids: list[list[str, int], ...]):

        return all([self.has(liquid_name, liquid_amount) for liquid_name, liquid_amount in liquids])

    def dumb(self) -> dict:

        return {
            "tanks": [tank.dumb() for tank in self]
        }

    def load(self, data):

        for n, tank in enumerate(self):
            tank.load(data["tanks"][n])
