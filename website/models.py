from time import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Spent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.String(10000))
    amount = db.Column(db.Numeric(precision=2, scale=None,
                       decimal_return_scale=None, asdecimal=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    Spents = db.relationship('Spent')
