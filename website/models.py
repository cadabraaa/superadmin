from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_code = db.Column(db.String(3), unique=True, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True)
    mobile = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(150))
    establishment_year = db.Column(db.String(4))