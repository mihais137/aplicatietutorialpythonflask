from . import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    numeEchipa = db.Column(db.String(150), unique=True)
    parola = db.Column(db.String(150))
    nume=db.Column(db.String(150))
    color = db.Column(db.String(30))
    punctaj = db.Column(db.Integer)
    config = db.Column(db.Integer)
    cart_config = db.Column(db.String(100))
    clasament=db.relationship('Clasament')

    def __init__(self, username, password, points = 0, nume = 'Echipa', cart_config= '', config = '', color = '6600ff'):
        self.username = username
        self.password = password
        self.points = points
        self.name = nume
        self.cart_config = cart_config
        self.config = config
        self.color=color

    def change_name(self, name):
        self.name = name

    def change_points(self, points):
        self.points = points

    def change_color(self, color):
        self.color = color

    def add_cart_config(self, new_prod):
        self.cart_config =  new_prod

    def add_config(self, new_prod):
        self.config =  new_prod



class Drona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descriere = db.Column(db.String(150))
    pret = db.Column(db.Integer)
    poza = db.Column(db.String(1000))
    
    def __init__(self, image, name, descriere, pret, code,stoc):
        self.pret =pret
        self.image = image
        self.name = name
        self.descriere = descriere
        self.code = code
        self.stoc = stoc

    def change_stoc(self, stoc):
        self.stoc = stoc

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
    username_id=db.Column(db.Integer,db.ForeignKey(User.id))
    loc=db.Column(db.Integer)

class Pozitie(db.Model):
    id=db.Column(db.Integer,priamry_key=True)
    pozitie=db.column(db.Integer)
    poz=Pozitie.first()
    poz.pozitie=1

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numeAdmin = db.Column(db.String(150), unique=True)
    parolaAdmin = db.Column(db.String(150))
