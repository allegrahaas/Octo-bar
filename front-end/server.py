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

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CONNECT TO DB
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


# with app.app_context():
#     db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


def init_db():
    ingredients = ["Vodka", "Scotch", "Rum", "Gin", "Tequila", "Triple Sec", "Club Soda", "Tonic Water", "Cola"]

    for ingredient in ingredients:
        db_ingredient = Ingredient(name=ingredient)
        try:
            db.session.add(db_ingredient)
            db.session.commit()
        except IntegrityError:
            # Ingredient already exists
            pass




if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
        init_db()

    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)
