from flask import Blueprint, render_template, flash, request, redirect,url_for, session
from flask_login import login_required, current_user
from . import db
from website.models import Drona
from website.models import Clasament
#from website.models import Pozitie
import random
import datetime

views = Blueprint('views', __name__)

@views.route('/')
def home():

    return render_template('home.html', team = current_user)


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

    return render_template('team.html', team = current_user, config=config)
    
@views.route('shop', methods = ['GET', 'POST'])
@login_required

def shop():

    products = Drona.query.all()
    if request.method == "POST":
        code = request.form.get('button')
        obj = Drona.query.filter_by(code = code).first()
        poz=Pozitie.first()
        if obj.stoc == 0:
            flash('Acest obiect nu se mai afla pe stoc', category='error')
        elif current_user.loc!=poz.pozitie:
            flash('Nu e randul tau',category='error')
        else:
            current_user.add_cart_config(code)
            poz.pozitie=poz.pozitie+1
            db.session.commit()        

    return render_template('shop.html', team = current_user, products = products)


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


    return render_template('shop_cart.html', team = current_user, config_cart=config_cart)


@views.route('/check_quiz', methods=['GET', 'POST'])
def check_quiz():

    actual_time = 3 #timpul / ora curenta
    quiz_time = 3 #ora la care e disponibil testul


    return render_template("check_quiz.html", actual_time = actual_time, quiz_time = quiz_time)

@views.route('/quiz', methods=['GET', 'POST'])
def quiz():

    target_date = datetime.datetime(2023, 3, 1, 0, 0, 0) # set the target date for the countdown timer
    now = datetime.datetime.now() # get the current date and time
    time_left = target_date - now # calculate the time left until the target date
    days_left = time_left.days # get the number of days left
    seconds_left = time_left.seconds # get the number of seconds left
    
    #return render_template('home.html', days_left=days_left, seconds_left=seconds_left)

    actual_time = 3
    quiz_time = 3
    
    if actual_time != quiz_time:
       return redirect("/check_quiz") 

    intrebari = {"Intrebarea 1?": [["rasp1", "rasp2", "rasp3"], "rasp_c"], "Intrebarea 2?": [["rasp1", "rasp2", "rasp3"], "rasp_c"], 
                "Intrebarea 3?": [["rasp1", "rasp2", "rasp3"], "rasp_c"]} #vor fi luate din baza de date
    

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
    raspunsuri1_lista.append(raspunsuri1[1])
    random.shuffle(raspunsuri1_lista) #noua aditie: am randomizat lista de raspunsuri ca sa nu mai fie cel corect ultimul mereu

    intrebare2 = session["intrebare2"]
    raspunsuri2 = intrebari[intrebare2]
    raspuns_corect2 = raspunsuri2[1]
    raspunsuri2_lista = [item for item in raspunsuri2[0]]
    raspunsuri2_lista.append(raspunsuri2[1])
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
                               raspunsuri2_lista = raspunsuri2_lista, days_left=days_left, seconds_left=seconds_left)
    

@views.route('/results', methods = ['GET', 'POST'])
def results():

    intrebari = {"Intrebarea 1?": [["rasp1", "rasp2", "rasp3"], "rasp_c"], "Intrebarea 2?": [["rasp1", "rasp2", "rasp3"], "rasp_c"], 
                "Intrebarea 3?": [["rasp1", "rasp2", "rasp3"], "rasp_c"]}
    intrebare1 = session["intrebare1"]
    rasp_corect1 = intrebari[intrebare1][1]
    intrebare2 = session["intrebare2"]
    rasp_corect2 = intrebari[intrebare2][1]

    punctaj = session["punctaj"]

    return render_template('results.html', punctaj = punctaj, rasp_corect1 = rasp_corect1, intrebare1 = intrebare1,
                           rasp_corect2 = rasp_corect2, intrebare2 = intrebare2)