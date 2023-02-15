from flask import Blueprint, render_template, request, redirect, session, url_for
import random

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/check_quiz', methods=['GET', 'POST'])
def check_quiz():

    actual_time = 3 #timpul / ora curenta
    quiz_time = 3 #ora la care e disponibil testul


    return render_template("check_quiz.html", actual_time = actual_time, quiz_time = quiz_time)

@views.route('/quiz', methods=['GET', 'POST'])
def quiz():

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

    # trebuie facut pentru n intrebari
    
    if request.method == 'POST':
        selected_option = request.form['select_option']
        if selected_option == raspuns_corect1:
            session["punctaj"] = 50 # se va adauga in db punctjul
        else:
            session["punctaj"] = 0
        return redirect(url_for('views.results'))
    else:
        return render_template('quiz.html', intrebare1 = intrebare1, raspunsuri1_lista = raspunsuri1_lista)
    

@views.route('/results', methods = ['GET', 'POST'])
def results():

    intrebari = {"Intrebarea 1?": [["rasp1", "rasp2", "rasp3"], "rasp_c"], "Intrebarea 2?": [["rasp1", "rasp2", "rasp3"], "rasp_c"], 
                "Intrebarea 3?": [["rasp1", "rasp2", "rasp3"], "rasp_c"]}
    intrebare1 = session["intrebare1"]
    rasp_corect1 = intrebari[intrebare1][1]

    punctaj = session["punctaj"]

    return render_template('results.html', punctaj = punctaj, rasp_corect1 = rasp_corect1, intrebare1 = intrebare1)