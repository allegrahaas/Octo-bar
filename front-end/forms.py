from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired, InputRequired, NoneOf

AMOUNT_OPTIONS = [("", ""), ("0.25", "1/4 oz."), ("0.33", "1/3 oz."), ("0.5", "1/2 oz."), ("0.66", "2/3 oz."),
                  ("0.75", "3/4 oz."), ("1", "1 oz."), ("1.5", "1.5 oz."), ("2", "2 oz."), ("Fill", "Fill")]


class RequiredIf(InputRequired):
    # TODO: test validator
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)


class ConfigureInventory(FlaskForm):
    gun_0 = SelectField("Bottle 1")
    gun_1 = SelectField("Bottle 2")
    gun_2 = SelectField("Bottle 3")
    gun_3 = SelectField("Bottle 4")
    gun_4 = SelectField("Bottle 5")
    gun_5 = SelectField("Bottle 6")
    gun_6 = SelectField("Bottle 7")
    gun_7 = SelectField("Bottle 8")

    cooler_0 = SelectField("Cooler 1")
    cooler_1 = SelectField("Cooler 2")
    cooler_2 = SelectField("Cooler 3")
    cooler_3 = SelectField("Cooler 4")
    cooler_4 = SelectField("Cooler 5")
    cooler_5 = SelectField("Cooler 6")

    base_0 = SelectField("Base 1")
    base_1 = SelectField("Base 2")


class CustomDrink(FlaskForm):
    ingredient_1 = SelectField("Ingredient 1",
                               validators=[NoneOf(message="Please select at least one ingredient.",
                                                  values=[""])])
    amount_1 = SelectField(choices=AMOUNT_OPTIONS,
                           validators=[NoneOf(message="Please select an amount for ingredient 1.",
                                              values=[""])])

    ingredient_2 = SelectField("Ingredient 2")
    amount_2 = SelectField(choices=AMOUNT_OPTIONS,
                           validators=[RequiredIf("ingredient_2",
                                                  message="Please select an amount for ingredient 2 or select None "
                                                          "for ingredient.")])

    ingredient_3 = SelectField("Ingredient 3")
    amount_3 = SelectField(choices=AMOUNT_OPTIONS,
                           validators=[RequiredIf("ingredient_3",
                                                  message="Please select an amount for ingredient 3 or select None "
                                                          "for ingredient.")])

    ingredient_4 = SelectField("Ingredient 4")
    amount_4 = SelectField(choices=AMOUNT_OPTIONS,
                           validators=[RequiredIf("ingredient_4",
                                                  message="Please select an amount for ingredient 4 or select None "
                                                          "for ingredient.")])

    ingredient_5 = SelectField("Ingredient 5")
    amount_5 = SelectField(choices=AMOUNT_OPTIONS,
                           validators=[RequiredIf("ingredient_5",
                                                  message="Please select an amount for ingredient 5 or select None "
                                                          "for ingredient.")])

    ingredient_6 = SelectField("Ingredient 6")
    amount_6 = SelectField(choices=AMOUNT_OPTIONS,
                           validators=[RequiredIf("ingredient_6",
                                                  message="Please select an amount for ingredient 6 or select None "
                                                          "for ingredient.")])

    save_recipe = BooleanField("Save custom recipe")

    name = StringField("Name", validators=[RequiredIf("save_recipe",
                                                      message="Please enter a name or uncheck \"Save custom recipe\"")])
