from . import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    numeEchipa = db.Column(db.String(150), unique=True)
    parola = db.Column(db.String(150))
    punctajEchipa = db.Column(db.Integer)
    configuratie = db.Column(db.Integer)
    def __init__(self, punctajEchipa = '0', configuratie = 'nicio configuratie'):
        self.punctajEchipa = punctajEchipa
        self.configuratie = configuratie



class Drona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descriere = db.Column(db.String(150))
    pret = db.Column(db.Integer)
    poza = db.Column(db.String(1000))
    def __init__(self, descriere = 'nu ai pus o descriere', pret = '99.99'):
        self.descriere = descriere
        self.pret = pret

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tip = db.Column(db.String(150))
    intrebari = db.relationship('Intrebari')

class Intrebari(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raspuns_corect = db.Column(db.String)
    tip_test = db.Column(db.String, db.ForeignKey(Test.tip))
    raspunsuri = db.relationship('Raspunsuri')

class Raspunsuri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raspuns1 = db.Column(db.String)
    raspuns2 = db.Column(db.String)
    raspuns3 = db.Column(db.String)
    raspuns4 = db.Column(db.String)
    id_intrebare = db.Column(db.Integer, db.ForeignKey(Intrebari.id))

class Clasament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loc1 = db.Column(db.String(150))
    loc2 = db.Column(db.String(150))
    loc3 = db.Column(db.String(150))
    loc4 = db.Column(db.String(150))
    loc5 = db.Column(db.String(150))
    loc6 = db.Column(db.String(150))
    loc7 = db.Column(db.String(150))
    loc8 = db.Column(db.String(150))
    loc9 = db.Column(db.String(150))
    loc10 = db.Column(db.String(150))

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numeAdmin = db.Column(db.String(150), unique=True)
    parolaAdmin = db.Column(db.String(150))
