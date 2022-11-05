from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired
from tables import Ingredient, db
from flask_sqlalchemy import SQLAlchemy

AMOUNT_OPTIONS = [("", ""), ("0.25", "1/4"), ("0.33", "1/3"), ("0.5", "1/2"), ("0.66", "2/3"), ("0.75", "3/4"),
                  ("1", "1"), ("1.5", "1.5"), ("2", "2"), ("Fill", "Fill")]


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

    submit = SubmitField("Save")


class CustomDrink(FlaskForm):
    amount_1 = SelectField(choices=AMOUNT_OPTIONS)
    ingredient_1 = SelectField()

    amount_2 = SelectField(choices=AMOUNT_OPTIONS)
    ingredient_2 = SelectField()

    amount_3 = SelectField(choices=AMOUNT_OPTIONS)
    ingredient_3 = SelectField()

    amount_4 = SelectField(choices=AMOUNT_OPTIONS)
    ingredient_4 = SelectField()

    amount_5 = SelectField(choices=AMOUNT_OPTIONS)
    ingredient_5 = SelectField()

    amount_6 = SelectField(choices=AMOUNT_OPTIONS)
    ingredient_6 = SelectField()
