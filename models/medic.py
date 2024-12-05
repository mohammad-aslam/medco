

from utils.db import db


class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    bmi = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    charges = db.Column(db.Integer, nullable=False)
    region = db.Column(db.String(100), nullable=False)




