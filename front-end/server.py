from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from tables import Recipe, Ingredient, db
from forms import ConfigureInventory, CustomDrink
from barbot import BarBot
import pandas

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

bot = BarBot()


@app.route("/")
def root():
    return render_template("index.html")


@app.route('/menu')
def menu():
    available_ingredients = [None]
    available_ingredients += [ingredient.id for ingredient in bot.gun if ingredient is not None]
    available_ingredients += [ingredient.id for ingredient in bot.cooler if ingredient is not None]
    available_ingredients += [ingredient.id for ingredient in bot.base if ingredient is not None]

    recipes = db.session.query(Recipe) \
        .filter(or_(Recipe.ingredient_1_id.in_(available_ingredients), Recipe.ingredient_1_id.is_(None))) \
        .filter(or_(Recipe.ingredient_2_id.in_(available_ingredients), Recipe.ingredient_2_id.is_(None))) \
        .filter(or_(Recipe.ingredient_3_id.in_(available_ingredients), Recipe.ingredient_3_id.is_(None))) \
        .filter(or_(Recipe.ingredient_4_id.in_(available_ingredients), Recipe.ingredient_4_id.is_(None))) \
        .filter(or_(Recipe.ingredient_5_id.in_(available_ingredients), Recipe.ingredient_5_id.is_(None))) \
        .filter(or_(Recipe.ingredient_6_id.in_(available_ingredients), Recipe.ingredient_6_id.is_(None))) \
        .all()

    return render_template("menu.html", page="Menu", recipes=recipes)


@app.route("/build-your-own", methods=["GET", "POST"])
def build_your_own():
    available_ingredients = [("", "None")]
    available_ingredients += [(ingredient.id, ingredient.name) for ingredient in bot.gun if ingredient is not None]
    available_ingredients += [(ingredient.id, ingredient.name) for ingredient in bot.cooler if ingredient is not None]
    available_ingredients += [(ingredient.id, ingredient.name) for ingredient in bot.base if ingredient is not None]

    form = CustomDrink()

    form.ingredient_1.choices = available_ingredients
    form.ingredient_2.choices = available_ingredients
    form.ingredient_3.choices = available_ingredients
    form.ingredient_4.choices = available_ingredients
    form.ingredient_5.choices = available_ingredients
    form.ingredient_6.choices = available_ingredients

    if form.validate_on_submit():
        custom_recipe = Recipe()

        if form.ingredient_1.data is not None:
            custom_recipe.amount_1 = form.amount_1.data
            custom_recipe.ingredient_1 = db.session.query(Ingredient).get(form.ingredient_1.data)

        if form.ingredient_2.data is not None:
            custom_recipe.amount_2 = form.amount_2.data
            custom_recipe.ingredient_2 = db.session.query(Ingredient).get(form.ingredient_2.data)

        if form.ingredient_3.data is not None:
            custom_recipe.amount_3 = form.amount_3.data
            custom_recipe.ingredient_3 = db.session.query(Ingredient).get(form.ingredient_3.data)

        if form.ingredient_4.data is not None:
            custom_recipe.amount_4 = form.amount_4.data
            custom_recipe.ingredient_4 = db.session.query(Ingredient).get(form.ingredient_4.data)

        if form.ingredient_5.data is not None:
            custom_recipe.amount_5 = form.amount_5.data
            custom_recipe.ingredient_5 = db.session.query(Ingredient).get(form.ingredient_5.data)

        if form.ingredient_6.data is not None:
            custom_recipe.amount_6 = form.amount_6.data
            custom_recipe.ingredient_6 = db.session.query(Ingredient).get(form.ingredient_6.data)

        custom_recipe.custom = True
        custom_recipe.fixed_size = True

        if form.save_recipe.data:
            custom_recipe.name = form.name.data if form.name.data is not None else None
            db.session.add(custom_recipe)
            db.session.commit()

        bot.make_recipe(custom_recipe, False)

    return render_template("build-your-own.html", page="BYO", ingredients=available_ingredients, form=form)


@app.route("/settings")
def settings():
    return render_template("settings.html", cooler_pressurized=bot.cooler_primed,
                           base_pressurized=bot.base_primed)


@app.route("/settings/configure-inventory", methods=["GET", "POST"])
def configure_inventory():
    gun_ingredients = db.session.query(Ingredient).filter(Ingredient.location == "gun").all()
    gun_list = [(ingredient.id, ingredient.name) for ingredient in gun_ingredients]
    gun_list.insert(0, (None, "None"))

    cooler_ingredients = db.session.query(Ingredient).filter(Ingredient.location == "cooler").all()
    cooler_list = [(ingredient.id, ingredient.name) for ingredient in cooler_ingredients]
    cooler_list.insert(0, (None, "None"))

    base_ingredients = db.session.query(Ingredient).filter(Ingredient.location == "base").all()
    base_list = [(ingredient.id, ingredient.name) for ingredient in base_ingredients]
    base_list.insert(0, (None, "None"))

    form = ConfigureInventory(gun_0=bot.gun[0].id if bot.gun[0] is not None else None,
                              gun_1=bot.gun[1].id if bot.gun[1] is not None else None,
                              gun_2=bot.gun[2].id if bot.gun[2] is not None else None,
                              gun_3=bot.gun[3].id if bot.gun[3] is not None else None,
                              gun_4=bot.gun[4].id if bot.gun[4] is not None else None,
                              gun_5=bot.gun[5].id if bot.gun[5] is not None else None,
                              gun_6=bot.gun[6].id if bot.gun[6] is not None else None,
                              gun_7=bot.gun[7].id if bot.gun[7] is not None else None,
                              cooler_0=bot.cooler[0].id if bot.cooler[0] is not None else None,
                              cooler_1=bot.cooler[1].id if bot.cooler[1] is not None else None,
                              cooler_2=bot.cooler[2].id if bot.cooler[2] is not None else None,
                              cooler_3=bot.cooler[3].id if bot.cooler[3] is not None else None,
                              cooler_4=bot.cooler[4].id if bot.cooler[4] is not None else None,
                              cooler_5=bot.cooler[5].id if bot.cooler[5] is not None else None,
                              base_0=bot.base[0].id if bot.base[0] is not None else None,
                              base_1=bot.base[1].id if bot.base[1] is not None else None)

    form.gun_0.choices = gun_list
    form.gun_1.choices = gun_list
    form.gun_2.choices = gun_list
    form.gun_3.choices = gun_list
    form.gun_4.choices = gun_list
    form.gun_5.choices = gun_list
    form.gun_6.choices = gun_list
    form.gun_7.choices = gun_list

    form.cooler_0.choices = cooler_list
    form.cooler_1.choices = cooler_list
    form.cooler_2.choices = cooler_list
    form.cooler_3.choices = cooler_list
    form.cooler_4.choices = cooler_list
    form.cooler_5.choices = cooler_list

    form.base_0.choices = base_list
    form.base_1.choices = base_list

    if form.validate_on_submit():
        bot.set_gun(db.session.query(Ingredient).get(form.gun_0.data), index=0)
        bot.set_gun(db.session.query(Ingredient).get(form.gun_1.data), index=1)
        bot.set_gun(db.session.query(Ingredient).get(form.gun_2.data), index=2)
        bot.set_gun(db.session.query(Ingredient).get(form.gun_3.data), index=3)
        bot.set_gun(db.session.query(Ingredient).get(form.gun_4.data), index=4)
        bot.set_gun(db.session.query(Ingredient).get(form.gun_5.data), index=5)
        bot.set_gun(db.session.query(Ingredient).get(form.gun_6.data), index=6)
        bot.set_gun(db.session.query(Ingredient).get(form.gun_7.data), index=7)

        bot.set_cooler(db.session.query(Ingredient).get(form.cooler_0.data), index=0)
        bot.set_cooler(db.session.query(Ingredient).get(form.cooler_1.data), index=1)
        bot.set_cooler(db.session.query(Ingredient).get(form.cooler_2.data), index=2)
        bot.set_cooler(db.session.query(Ingredient).get(form.cooler_3.data), index=3)
        bot.set_cooler(db.session.query(Ingredient).get(form.cooler_4.data), index=4)
        bot.set_cooler(db.session.query(Ingredient).get(form.cooler_5.data), index=5)

        bot.set_base(db.session.query(Ingredient).get(form.base_0.data), index=0)
        bot.set_base(db.session.query(Ingredient).get(form.base_1.data), index=1)

        return render_template("configure-inventory.html", form=form, success=True)

    return render_template("configure-inventory.html", form=form, success=False)


@app.route("/settings/pressurize-cooler-pumps")
def prime_cooler_pumps():
    bot.prime_cooler_pumps()
    return render_template("settings.html", cooler_pressurized=bot.cooler_primed,
                           base_pressurized=bot.base_primed)


@app.route("/settings/depressurize-cooler-pumps")
def depressurize_cooler_pumps():
    bot.depressurize_cooler_pumps()
    return render_template("settings.html", cooler_pressurized=bot.cooler_primed,
                           base_pressurized=bot.base_primed)


@app.route("/settings/pressurize-base-pumps")
def prime_base_pumps():
    bot.prime_base_pumps()
    return render_template("settings.html", cooler_pressurized=bot.cooler_primed,
                           base_pressurized=bot.base_primed)


@app.route("/settings/depressurize-base-pumps")
def depressurize_base_pumps():
    bot.depressurize_base_pumps()
    return render_template("settings.html", cooler_pressurized=bot.cooler_primed,
                           base_pressurized=bot.base_primed)


@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    drink_recipe = db.session.query(Recipe).get(recipe_id)
    return render_template("recipe.html", recipe=drink_recipe)


@app.route("/recipe/<int:recipe_id>/pour_drink/<double>")
def make_recipe(recipe_id, double):
    drink_recipe = db.session.query(Recipe).get(recipe_id)
    bot.make_recipe(drink_recipe, bool(double))
    return render_template("recipe.html", recipe=drink_recipe)


def save_drink(drink: Recipe):
    try:
        db.session.add(drink)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def init_db():
    table = pandas.read_csv("static/initialization/ingredients_and_locations.csv")

    for row in table.itertuples():
        db_ingredient = Ingredient(name=row.liquor, location=row.location)
        try:
            db.session.add(db_ingredient)
            db.session.commit()
        except IntegrityError:
            # Ingredient already exists
            db.session.rollback()

    margarita = Recipe(name="Margarita",
                       custom=False,
                       fixed_size=True,
                       amount_1="1",
                       ingredient_1=db.session.query(Ingredient).filter(Ingredient.name == "Tequila").first(),
                       amount_2="0.5",
                       ingredient_2=db.session.query(Ingredient).filter(Ingredient.name == "Triple Sec").first(),
                       amount_3="1",
                       ingredient_3=db.session.query(Ingredient).filter(Ingredient.name == "Lime Juice").first())
    save_drink(margarita)

    rum_and_cola = Recipe(name="Rum and Cola",
                          custom=False,
                          fixed_size=False,
                          amount_1="1",
                          ingredient_1=db.session.query(Ingredient).filter(Ingredient.name == "Rum - Light").first(),
                          amount_2="Fill",
                          ingredient_2=db.session.query(Ingredient).filter(Ingredient.name == "Cola").first())
    save_drink(rum_and_cola)

    vodka_soda = Recipe(name="Vodka Soda",
                        custom=False,
                        fixed_size=False,
                        amount_1="1",
                        ingredient_1=db.session.query(Ingredient).filter(Ingredient.name == "Vodka").first(),
                        amount_2="Fill",
                        ingredient_2=db.session.query(Ingredient).filter(Ingredient.name == "Club Soda").first())
    save_drink(vodka_soda)

    gin_and_tonic = Recipe(name="Gin and Tonic",
                           custom=False,
                           fixed_size=False,
                           amount_1="1",
                           ingredient_1=db.session.query(Ingredient).filter(Ingredient.name == "Gin").first(),
                           amount_2="Fill",
                           ingredient_2=db.session.query(Ingredient).filter(Ingredient.name == "Tonic Water").first())
    save_drink(gin_and_tonic)

    scotch = Recipe(name="Scotch",
                    custom=False,
                    fixed_size=False,
                    amount_1="1",
                    ingredient_1=db.session.query(Ingredient).filter(Ingredient.name == "Scotch").first())
    save_drink(scotch)


def init_bot():
    bot.gun[0] = db.session.query(Ingredient).get(66)  # Vodka
    bot.gun[1] = db.session.query(Ingredient).get(54)  # Rum - Light
    bot.gun[2] = db.session.query(Ingredient).get(63)  # Tequila
    bot.gun[3] = db.session.query(Ingredient).get(57)  # Scotch
    bot.gun[4] = db.session.query(Ingredient).get(27)  # Gin
    bot.gun[5] = db.session.query(Ingredient).get(24)  # Dry Vermouth
    bot.gun[6] = db.session.query(Ingredient).get(48)  # Orange Liqueur
    bot.gun[7] = db.session.query(Ingredient).get(62)  # Sweet Vermouth

    bot.cooler[0] = db.session.query(Ingredient).get(58)  # Simple Syrup
    bot.cooler[1] = db.session.query(Ingredient).get(64)  # Tonic Water
    bot.cooler[2] = db.session.query(Ingredient).get(17)  # Cola
    bot.cooler[3] = db.session.query(Ingredient).get(14)  # Club Soda
    bot.cooler[3] = db.session.query(Ingredient).get(40)  # Lime Juice

    bot.base[0] = db.session.query(Ingredient).get(6)  # Bitters
    bot.base[1] = db.session.query(Ingredient).get(46)  # Orange Bitters


if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
        init_db()
        init_bot()

    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)
