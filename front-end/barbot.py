from tables import Ingredient, Recipe


class BarBot:
    def __init__(self):
        self.gun = [None, None, None, None, None, None, None, None]
        self.cooler = [None, None, None, None, None, None]
        self.base = [None, None]

        self.gun_position = 0

        self.cooler_primed = False
        self.base_primed = False

    def go_home(self):
        self.rotate_gun(0)

    def dispense_gun(self, index, amount, double):
        self.rotate_gun(index)
        # TODO: send serial to controller

        if double:
            pass
        # TODO: send serial to controller

    def dispense_cooler(self, index, amount):
        # TODO send serial to controller
        pass

    def dispense_base(self, index):
        # TODO send serial to controller
        pass

    def set_gun(self, ingredient: Ingredient, index):
        self.gun[index] = ingredient

    def set_cooler(self, ingredient: Ingredient, index):
        self.cooler[index] = ingredient

    def set_base(self, ingredient: Ingredient, index):
        self.base[index] = ingredient

    def prime_base_pumps(self):
        print("Base pumps primed")
        self.base_primed = True
        # TODO tell controller to prime base pumps

    def depressurize_base_pumps(self):
        print("Depressurized base pumps")
        self.base_primed = False
        # TODO tell controller to depressurize base pumps

    def prime_cooler_pumps(self):
        print("Cooler pumps primed")
        self.cooler_primed = True
        # TODO tell controller to prime cooler pumps

    def depressurize_cooler_pumps(self):
        print("Depressurized cooler pumps")
        self.cooler_primed = False
        # TODO tell controller to depressurize cooler pumps

    def rotate_gun(self, target_index: int):
        if self.gun_position == target_index:
            return None

        num_steps = 0

        cw_index = self.gun_position
        ccw_index = self.gun_position

        while cw_index != target_index and ccw_index != target_index:
            cw_index += 1
            ccw_index -= 1
            num_steps += 1

            if cw_index == 8:
                index = 0

            if ccw_index == -1:
                index = 7

        if cw_index == target_index:
            pass
            # TODO send serial to rotate cw num_steps
        else:
            pass
            # TODO send serial to rotate ccw num_steps

    def add_ingredient(self, ingredient: Ingredient, amount: str, double: bool):
        if ingredient.location == "gun":
            for index, bottle in enumerate(self.gun):
                if bottle is not None and bottle.id == ingredient.id:
                    gun_index = index
                    self.dispense_gun(gun_index, amount, double)
        elif ingredient.location == "cooler":
            for index, bottle in enumerate(self.cooler):
                if bottle is not None and bottle.id == ingredient.id:
                    cooler_index = index
                    self.dispense_cooler(cooler_index, amount)
        elif ingredient.location == "base":
            for index, bottle in enumerate(self.base):
                if bottle is not None and bottle.id == ingredient.id:
                    base_index = index
                    self.dispense_base(index)

    def make_recipe(self, recipe: Recipe, double: bool):
        self.add_ingredient(recipe.ingredient_1, recipe.amount_1, double)

        if recipe.ingredient_2 is not None:
            self.add_ingredient(recipe.ingredient_2, recipe.amount_2, double)

        if recipe.ingredient_3 is not None:
            self.add_ingredient(recipe.ingredient_3, recipe.amount_3, double)

        if recipe.ingredient_4 is not None:
            self.add_ingredient(recipe.ingredient_4, recipe.amount_4, double)

        if recipe.ingredient_5 is not None:
            self.add_ingredient(recipe.ingredient_5, recipe.amount_5, double)

        if recipe.ingredient_6 is not None:
            self.add_ingredient(recipe.ingredient_6, recipe.amount_6, double)
