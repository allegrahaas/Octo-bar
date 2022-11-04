import datetime

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
import pandas

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)


class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    custom = db.Column(db.Boolean, nullable=False)

    ingredient_1_id = db.Column(db.Integer, ForeignKey("ingredients.id"))
    ingredient_2_id = db.Column(db.Integer, ForeignKey("ingredients.id"), nullable=True)
    ingredient_3_id = db.Column(db.Integer, ForeignKey("ingredients.id"), nullable=True)
    ingredient_4_id = db.Column(db.Integer, ForeignKey("ingredients.id"), nullable=True)
    ingredient_5_id = db.Column(db.Integer, ForeignKey("ingredients.id"), nullable=True)
    ingredient_6_id = db.Column(db.Integer, ForeignKey("ingredients.id"), nullable=True)

    amount_1 = db.Column(db.String(10), nullable=False)
    amount_2 = db.Column(db.String(10), nullable=True)
    amount_3 = db.Column(db.String(10), nullable=True)
    amount_4 = db.Column(db.String(10), nullable=True)
    amount_5 = db.Column(db.String(10), nullable=True)
    amount_6 = db.Column(db.String(10), nullable=True)

    ingredient_1 = relationship("Ingredient", lazy=False, foreign_keys=[ingredient_1_id])
    ingredient_2 = relationship("Ingredient", lazy=False, foreign_keys=[ingredient_2_id])
    ingredient_3 = relationship("Ingredient", lazy=False, foreign_keys=[ingredient_3_id])
    ingredient_4 = relationship("Ingredient", lazy=False, foreign_keys=[ingredient_4_id])
    ingredient_5 = relationship("Ingredient", lazy=False, foreign_keys=[ingredient_5_id])
    ingredient_6 = relationship("Ingredient", lazy=False, foreign_keys=[ingredient_6_id])


class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)


ingredients = None


@app.route("/")
def root():
    return render_template("index.html")

@app.route('/menu')
def menu():
    # TODO: Get relevant recipes
    return render_template("menu.html", page="Menu")

@app.route("/build-your-own")
def build_your_own():

    return render_template("build-your-own.html", page="BYO")

@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    pass


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
                       amount_1="1",
                       ingredient_1=db.session.query(Ingredient).filter(Ingredient.name == "Tequila").first(),
                       amount_2="0.5",
                       ingredient_2=db.session.query(Ingredient).filter(Ingredient.name == "Triple Sec").first(),
                       amount_3="1",
                       ingredient_3=db.session.query(Ingredient).filter(Ingredient.name == "Lime Juice").first())
    save_drink(margarita)

    rum_and_cola = Recipe(name="Rum and Cola",
                          custom=False,
                          amount_1="1",
                          ingredient_1=db.session.query(Ingredient).filter(Ingredient.name == "Rum").first(),
                          amount_2="Fill",
                          ingredient_2=db.session.query(Ingredient).filter(Ingredient.name == "Cola").first())
    save_drink(rum_and_cola)

    vodka_soda = Recipe(name="Vodka Soda",
                        custom=False,
                        amount_1="1",
                        ingredient_1=db.session.query(Ingredient).filter(Ingredient.name == "Vodka").first(),
                        amount_2="Fill",
                        ingredient_2=db.session.query(Ingredient).filter(Ingredient.name == "Soda").first())
    save_drink(vodka_soda)

    gin_and_tonic = Recipe(name="Gin and Tonic",
                           custom=False,
                           amount_1="1",
                           ingredient_1=db.session.query(Ingredient).filter(Ingredient.name == "Gin").first(),
                           amount_2="Fill",
                           ingredient_2=db.session.query(Ingredient).filter(Ingredient.name == "Tonic Water").first())
    save_drink(gin_and_tonic)

    scotch = Recipe(name="Scotch",
                    custom=False,
                    amount_1="1",
                    ingredient_1=db.session.query(Ingredient).filter(Ingredient.name == "Scotch").first())
    save_drink(scotch)


def init_app():
    ingredients = db.session.query(Ingredient)


if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
        init_db()
        init_app()

    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)
