from . import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(150), unique=True)
    level = db.Column(db.String(150))
    parola = db.Column(db.String(150))
    nume=db.Column(db.String(150))
    color = db.Column(db.String(30))
    punctaj = db.Column(db.Integer)
    config = db.Column(db.Integer)
    frame = db.Column(db.String(100))
    cart_config = db.Column(db.String(100))
    cart_frame = db.Column(db.String(100))
    last_test = db.Column(db.String)
 #   clasament=db.relationship('Clasament')

    def __init__(self, username, password, punctaj = 0, nume = 'Echipa', cart_config= '',cart_frame='', config = 'no',frame='no', color = '6600ff',  level = 'team', last_test = ''):
        self.username = username
        self.parola = password
        self.punctaj = punctaj
        self.nume = nume
        self.cart_config = cart_config
        self.cart_frame= cart_frame
        self.config = config
        self.frame= frame
        self.color= color
        self.level = level
        self.last_test = last_test

    def change_name(self, nume):
        self.nume = nume

    def change_points(self, punctaj):
        self.punctaj = punctaj

    def change_color(self, color):
        self.color = color

    def add_cart_config(self, new_prod):
        self.cart_config =  new_prod

    def add_config(self, new_prod):
        self.config =  new_prod

    def change_last_test(self, new_test):
        self.last_test = new_test
    
    def add_cart_frame(self, new_prod):
        self.cart_frame =  new_prod

    def add_frame(self, new_prod):
        self.frame =  new_prod


class Drona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descriere = db.Column(db.String(150))
    nume=db.Column(db.String(30))
    stoc=db.Column(db.Integer)
    poza = db.Column(db.String(1000))
    
    def __init__(self, poza, nume, descriere, stoc):
        self.poza = poza
        self.nume = nume
        self.descriere = descriere
        self.stoc = stoc

    def change_stoc(self, stoc):
        self.stoc = stoc

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tip = db.Column(db.String(150))
    status = db.Column(db.String)
    durata = db.Column(db.Integer)
    intrebari = db.relationship('Intrebari')

    def change_status(self, new_status):
        self.status =  new_status


class Intrebari(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intrebare = db.Column(db.String)
    raspuns_corect = db.Column(db.String)
    tip_test = db.Column(db.String, db.ForeignKey(Test.id))
    raspunsuri = db.relationship('Raspunsuri')

class Raspunsuri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raspuns1 = db.Column(db.String)
    raspuns2 = db.Column(db.String)
    raspuns3 = db.Column(db.String)
    raspuns4 = db.Column(db.String)
    id_intrebare = db.Column(db.Integer, db.ForeignKey(Intrebari.id))


#class Clasament(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    username_id=db.Column(db.Integer,db.ForeignKey(User.id))
#   loc=db.Column(db.Integer)

#class Pozitie(db.Model):
#    id=db.Column(db.Integer,primary_key=True)
#    pozitie=db.column(db.Integer)

# #    def __init__(self,pozitie=1):
##     #     self.pozitie=pozitie
##     poz=Pozitie.first()
##     poz.pozitie=1

# class Admin(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     numeAdmin = db.Column(db.String(150), unique=True)
#     parolaAdmin = db.Column(db.String(150))
