from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    custom = db.Column(db.Boolean, nullable=False)
    fixed_size = db.Column(db.Boolean, nullable=False)

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
    location = db.Column(db.String(30), nullable=False)