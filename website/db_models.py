from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    stocks = db.relationship('Stock')

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(5))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
        