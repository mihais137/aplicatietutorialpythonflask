from . import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    numeEchipa = db.Column(db.String(150), unique=True)
    parola = db.Column(db.String(150))
    punctajEchipa = db.Column(db.Integer)
    configuratie = db.Column(db.Integer)

class Drona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descriere = db.Column(db.String(150))
    pret = db.Column(db.Integer)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tip = db.Column(db.String(150))
# de completat aici
# de completat aici
# de completat aici
# de completat aici
# de completat aici

class Clasament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
# de completat aici
# de completat aici
# de completat aici
# de completat aici
# de completat aici

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numeAdmin = db.Column(db.String(150), unique=True)
    parolaAdmin = db.Column(db.String(150))

# pentru ora inceput, tutorial website python Tim 1:23:28