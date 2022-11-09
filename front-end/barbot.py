from tables import Ingredient


class BarBot:
    def __init__(self):
        self.gun = [None, None, None, None, None, None, None, None]
        self.cooler = [None, None, None, None, None, None]
        self.base = [None, None]

        self.gun_position = 0

        self.cooler_pumps_primed = False
        self.base_pumps_primed = False

    def go_home(self):
        # TODO: rotate gun to 0 position
        pass

    def dispense_gun(self, index, amount):
        # TODO: rotate to index and send serial to controller
        pass

    def dispense_cooler(self, index, amount):
        # TODO send serial to controller
        if index == 0:
            pass
        elif index == 1:
            pass
        elif index == 2:
            pass
        elif index == 3:
            pass
        elif index == 4:
            pass
        elif index == 5:
            pass

    def dispense_base(self, index, num_pumps):
        # TODO send serial to controller
        if index == 0:
            pass
        elif index == 1:
            pass

    def set_gun(self, ingredient: Ingredient, index):
        self.gun[index] = ingredient

    def set_cooler(self, ingredient: Ingredient, index):
        self.cooler[index] = ingredient

    def set_base(self, ingredient: Ingredient, index):
        self.base[index] = ingredient

    def prime_base_pumps(self):
        print("Base pumps primed")
        self.base_pumps_primed = True
        # TODO tell controller to prime base pumps

    def depressurize_base_pumps(self):
        print("Depressurized base pumps")
        self.base_pumps_primed = False
        # TODO tell controller to depressurize base pumps

    def prime_cooler_pumps(self):
        print("Cooler pumps primed")
        self.cooler_pumps_primed = True
        # TODO tell controller to prime cooler pumps

    def depressurize_cooler_pumps(self):
        print("Depressurized cooler pumps")
        self.cooler_pumps_primed = False
        # TODO tell controller to depressurize cooler pumps
