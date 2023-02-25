from flask import Blueprint, render_template, flash, request, redirect,url_for, session
from flask_login import login_required, current_user
from . import db
from website.models import Drona, Test, Intrebari, Raspunsuri
from website.models import User
#from sqlalchemy import desc

import random
import datetime

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():

    return render_template('home.html', user = current_user)



@views.route('team', methods = ['GET', 'POST'])
@login_required
def team():

    config_code = current_user.config
    

    config = Drona.query.filter_by(code = config_code).first()
    

    if request.method == 'POST':
        nume = request.form.get('id_team')
        color = request.form.get('color_team')
        current_user.change_nume(nume)
        current_user.change_color(color)
        #db.session.update()
        db.session.commit()
        flash('Nume actualizat', category='succes')

    return render_template('team.html', user = current_user, config=config)
    
@views.route('shop', methods = ['GET', 'POST'])
@login_required
def shop():

    products = Drona.query.all()
    if request.method == "POST":
        code = request.form.get('button')
        obj = Drona.query.filter_by(code = code).first()
        #poz=Pozitie.first()
        if obj.stoc == 0:
            flash('Acest obiect nu se mai afla pe stoc', category='error')
        elif cine_alege()!=current_user.pozitie:
        #current_user.loc!=poz.pozitie:
            flash('Nu e randul tau',category='error')
        else:
            current_user.add_cart_config(code)
            #poz.pozitie=poz.pozitie+1
            db.session.commit()        

    return render_template('shop.html', user = current_user, products = products)


@views.route('shop_cart', methods = ['GET', 'POST'])
@login_required
def shop_cart():

    config_cart_code = current_user.cart_config
    

    print(config_cart_code)

    config_cart = Drona.query.filter_by(code = config_cart_code).first()
    

    if not config_cart:
        config_cart = 'null'
    

    print(config_cart)

    if request.method == 'POST':
        check = request.form.get('button')
        if check == 'config':
            current_user.add_cart_config('')
            db.session.commit()
            return redirect(url_for('views.shop_cart'))
        if check == 'confirm':
            config_cart = Drona.query.filter_by(code = config_cart_code).first()
            if current_user.cart_config == '':
                 flash('Nu ai obiecte in cos', category='error')
                 return redirect(url_for('views.shop_cart'))
            elif current_user.punctaj < (config_cart.pret):
                flash('Nu ai suficiente puncte', category='error')  
                return redirect(url_for('views.shop_cart'))
            elif config_cart.stoc == 0:
                flash('Produsul din cos nu mai este pe stoc', category='error')
                return redirect(url_for('views.shop_cart'))         
            elif current_user.cart_config != '':
                current_user.add_config(current_user.cart_config)
                current_user.add_cart_config('')
                current_user.change_points(current_user.points - (config_cart.pret))
                config_cart.change_stoc(config_cart.stoc - 1)
                db.session.commit()
                return redirect(url_for('views.team'))


    return render_template('shop_cart.html', user = current_user, config_cart=config_cart)

#def calculare_clasament():
    users=User.query.all()
    places=Clasament.query.all()
    maxim1=0
    maxim2=1000
    i=1
    for place in places:
        for user in users:
            if user.punctaj>maxim1 and user.punctaj<=maxim2:
                maxim1=user.punctaj
        for user in users:
            if user.punctaj==maxim1:
                place.username=user.username
                place.loc=i
        i=i+1
        maxim2=maxim1
        maxim1=0

    db.session.commit()

    return 0

def cine_alege():
    
    clasament=User.query.order_by(desc(User.punctaj)).all()

    for x in range(len(clasament)):
        clasament[x]=clasament[x].id
    
    for x, i in clasament, range(len(clasament)):
        user=User.query.filter_by(id=x).first()
        user.pozitie=i+1

    for i in range(len(clasament)):
        user=User.query.filter_by(pozitie=i).first()
        if user.config=="":
            return user.pozitie
        else:
            continue

@views.route('/check_quiz', methods=['GET', 'POST'])
@login_required
def check_quiz():

    actual_time = 3 #timpul / ora curenta
    quiz_time = 3 #ora la care e disponibil testul

    test = Test.query.filter_by(status = 'activ').first()
    if test:
        tip_test = test.tip
        #return render_template("check_quiz.html")
    else:
        tip_test = "null"
        #return render_template("check_quiz.html")

    return render_template("check_quiz.html", tip_test = tip_test, user = current_user)

@views.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():

    target_date_str = request.args.get('target_date')
    if target_date_str:
        target_date = datetime.fromisoformat(target_date_str)
    else:
        target_date = datetime.datetime.now() + datetime.timedelta(minutes=20)
        target_date_str = target_date.isoformat()

    actual_time = 3
    quiz_time = 3
    
    test = Test.query.filter_by(status = 'activ').first()
    if not test:
       return redirect(url_for('views.check_quiz'))

    #intrebari = {"Intrebarea 1?": [["rasp1", "rasp2", "rasp3"], "rasp_c"], "Intrebarea 2?": [["rasp1", "rasp2", "rasp3"], "rasp_c"], 
                #"Intrebarea 3?": [["rasp1", "rasp2", "rasp3"], "rasp_c"]} #vor fi luate din baza de date
    
    intrebari_nush = test.intrebari
    intrebari_text = []
    intrebari = {} #are de fapt si raspunsurile

    raspuns = Raspunsuri.query.filter_by(id_intrebare = 1).first()
    raspunsuri = []
    raspunsuri.append(raspuns.raspuns1)
    raspunsuri.append(raspuns.raspuns2)
    raspunsuri.append(raspuns.raspuns3)
    raspunsuri.append(raspuns.raspuns4)
    
    for i in intrebari_nush:
        intrebari_text.append(i.intrebare)
        intrebari[i.intrebare] = [raspunsuri, i.raspuns_corect]

    print(intrebari)

    lista_intrebari = []
    if "intrebare1" not in session:
        session["intrebare1"] = random.choice(list(intrebari.keys()))
    lista_intrebari.append(session["intrebare1"])
    if "intrebare2" not in session:
        session["intrebare2"] = random.choice(list(intrebari.keys()))
        while True:
            if session["intrebare2"] in lista_intrebari:
                session["intrebare2"] = random.choice(list(intrebari.keys()))
            else:
                break
    lista_intrebari.append(session["intrebare2"])
    #trebuie facut pentru n intrebari
    
    intrebare1 = session["intrebare1"]
    raspunsuri1 = intrebari[intrebare1]
    raspuns_corect1 = raspunsuri1[1]
    raspunsuri1_lista = [item for item in raspunsuri1[0]]
    #raspunsuri1_lista.append(raspunsuri1[1])
    random.shuffle(raspunsuri1_lista) #noua aditie: am randomizat lista de raspunsuri ca sa nu mai fie cel corect ultimul mereu

    intrebare2 = session["intrebare2"]
    raspunsuri2 = intrebari[intrebare2]
    raspuns_corect2 = raspunsuri2[1]
    raspunsuri2_lista = [item for item in raspunsuri2[0]]
    #raspunsuri2_lista.append(raspunsuri2[1])
    random.shuffle(raspunsuri2_lista)

    # trebuie facut pentru n intrebari
    
    session["punctaj"] = 0
    if request.method == 'POST':
        selected_option_1 = request.form.get('select_option1')
        print (selected_option_1)
        if selected_option_1 == raspuns_corect1:
            print("a")
            session["punctaj"] += 50 # se va adauga in db punctajul
        else:
            session["punctaj"] += 0
            print("b")

        selected_option_2 = request.form.get('select_option2')
        print (selected_option_2)
        if selected_option_2 == raspuns_corect2:
            print("da")
            session["punctaj"] += 50
        else:
            print("nu")
            session["punctaj"] += 0
        return redirect(url_for('views.results'))
    else:
        return render_template('quiz.html', intrebare1 = intrebare1, raspunsuri1_lista = raspunsuri1_lista, intrebare2 = intrebare2,
                               raspunsuri2_lista = raspunsuri2_lista, target_date = target_date_str, user = current_user)
    

@views.route('/results', methods = ['GET', 'POST'])
@login_required
def results():

    test = Test.query.filter_by(status = 'activ').first()
    if not test:
       return redirect(url_for('views.check_quiz'))
  
    intrebari_nush = test.intrebari
    intrebari_text = []
    intrebari = {} #are de fapt si raspunsurile

    raspuns = Raspunsuri.query.filter_by(id_intrebare = 1).first()
    raspunsuri = []
    raspunsuri.append(raspuns.raspuns1)
    raspunsuri.append(raspuns.raspuns2)
    raspunsuri.append(raspuns.raspuns3)
    raspunsuri.append(raspuns.raspuns4)
    
    for i in intrebari_nush:
        intrebari_text.append(i.intrebare)
        intrebari[i.intrebare] = [raspunsuri, i.raspuns_corect]

    #intrebari = {"Intrebarea 1?": [["rasp1", "rasp2", "rasp3"], "rasp_c"], "Intrebarea 2?": [["rasp1", "rasp2", "rasp3"], "rasp_c"], 
                #"Intrebarea 3?": [["rasp1", "rasp2", "rasp3"], "rasp_c"]}
    intrebare1 = session["intrebare1"]
    rasp_corect1 = intrebari[intrebare1][1]
    intrebare2 = session["intrebare2"]
    rasp_corect2 = intrebari[intrebare2][1]

    punctaj = session["punctaj"]

    return render_template('results.html', punctaj = punctaj, rasp_corect1 = rasp_corect1, intrebare1 = intrebare1,
                           rasp_corect2 = rasp_corect2, intrebare2 = intrebare2, user = current_user)


def get_questions(nr_intrebari):


    pass
    #return lista intrebari, raspunsuri