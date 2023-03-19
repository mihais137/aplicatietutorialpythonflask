from flask import Blueprint, render_template, flash, request, redirect,url_for, session
from flask_login import login_required, current_user
from . import db
from website.models import Drona, Test, Intrebari, Raspunsuri
from website.models import User
from sqlalchemy import desc
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
    frame_code = current_user.frame
    clasament = get_clasament()
    
    config = Drona.query.filter_by(id = config_code).first()
    frame = Drona.query.filter_by(id = frame_code).first()
    if request.method == 'POST':
        nume = request.form.get('id_team')
        color = request.form.get('color_team')
        current_user.change_nume(nume)
        current_user.change_color(color)
        db.session.commit()
        flash('Nume actualizat', category='succes')

    return render_template('team.html', user = current_user, config=config, frame=frame,clasament = clasament)
    

@views.route('shop', methods = ['GET', 'POST'])
@login_required
def shop():

    products = Drona.query.all()
    if request.method == "POST":
        code = request.form.get('button')
        obj = Drona.query.filter_by(id = code).first()
        if obj.stoc == 0:
            flash('Acest obiect nu se mai afla pe stoc', category='error')         
        elif cine_alege()!=current_user.id:
            flash('Nu e randul tau', category='error')
        elif obj.nume.startswith('CONFIG'):
            current_user.add_cart_config(code)
            db.session.commit()        
        elif obj.nume.startswith('FRAME'):
            current_user.add_cart_frame(code)
            db.session.commit()

    return render_template('shop.html', user = current_user, products = products)


@views.route('shop_cart', methods = ['GET', 'POST'])
@login_required
def shop_cart():

    config_cart_code = current_user.cart_config
    frame_cart_code = current_user.cart_frame

    frame_cart= Drona.query.filter_by(id = frame_cart_code).first()
    config_cart = Drona.query.filter_by(id = config_cart_code).first()
    
    if not config_cart:
        config_cart = 'null'
    
    if not frame_cart:
        frame_cart = 'null'
    
    if request.method == 'POST':
        check = request.form.get('button')

        if check == 'config':
            current_user.add_cart_config('')
            db.session.commit()
            return redirect(url_for('views.shop_cart'))
        
        if check == 'frame':
            current_user.add_cart_frame('')
            db.session.commit()
            return redirect(url_for('views.shop_cart'))
        
        if check == 'confirm':
            config_cart = Drona.query.filter_by(id = config_cart_code).first()
            frame_cart = Drona.query.filter_by(id = frame_cart_code).first()
            if current_user.cart_config== '' or current_user.cart_frame == '':
                 flash('Nu ai destule obiecte in cos', category='error')
                 return redirect(url_for('views.shop_cart'))
            elif config_cart.stoc== 0 or frame_cart.stoc== 0:
                flash('Produsul din cos nu mai este pe stoc', category='error')
                return redirect(url_for('views.shop_cart'))         
            elif current_user.cart_config!='' and current_user.cart_frame != '':
                current_user.add_frame(current_user.cart_frame)
                current_user.add_config(current_user.cart_config)
                current_user.add_cart_config('')
                current_user.add_cart_frame('')
                config_cart.change_stoc(config_cart.stoc - 1)
                frame_cart.change_stoc(frame_cart.stoc - 1)
                db.session.commit()
                return redirect(url_for('views.team'))

    return render_template('shop_cart.html', user = current_user, config_cart=config_cart, frame_cart=frame_cart)


@views.route('/check_quiz', methods=['GET', 'POST'])
@login_required
def check_quiz():

    test = Test.query.filter_by(status = 'activ').first()
    if test:
        tip_test = test.tip
    else:
        tip_test = "null"

    return render_template("check_quiz.html", tip_test = tip_test, user = current_user)


@views.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():

    test = Test.query.filter_by(status = 'activ').first()
    if not test:
       return redirect(url_for('views.check_quiz'))

    if current_user.last_test == test.tip:
        flash('Ai dat deja acest test', category="error")
        return redirect(url_for('views.results'))
    
    durata = test.durata

    if 'questions' not in session:
        questions = random.sample(test.intrebari, k=5)
        questions_id = []
        for q in questions:
            questions_id.append(q.id)
        session['questions'] = questions_id

    questions = []
    for q in session['questions']:
        questions.append(Intrebari.query.filter_by(id = q).first())
    
    if request.method == "POST":
        current_user.change_last_test = test.tip
        answer_q1 = request.form.get(questions[0].intrebare)
        answer_q2 = request.form.get(questions[1].intrebare)
        answer_q3 = request.form.get(questions[2].intrebare)
        answer_q4 = request.form.get(questions[3].intrebare)
        answer_q5 = request.form.get(questions[4].intrebare)

        points = 0

        if answer_q1 == questions[0].raspuns_corect:

            points += 20
        if answer_q2 == questions[1].raspuns_corect:
            points += 20
        if answer_q3 == questions[2].raspuns_corect:
            points += 20
        if answer_q4 == questions[3].raspuns_corect:
            points += 20
        if answer_q5 == questions[4].raspuns_corect:
            points += 20

        # remaining_time = request.form.get('remaining_time')
        # remaining_time_points = remaining_time * 0.01
        # points += remaining_time_points
        # remaining_time = request.get_json()
        # points += remaining_time

        session['points'] = points

        current_user.change_points(current_user.punctaj + points)
        db.session.commit()
        flash('Test finalizat', category="succes")
        return redirect(url_for('views.results'))
                         
    return render_template('quiz.html', user = current_user, questions = questions, durata = durata)


@views.route('/results', methods = ['GET', 'POST'])
@login_required
def results():

    test = Test.query.filter_by(status = 'activ').first()
    if not test:
       return redirect(url_for('views.check_quiz'))

    if test.tip != current_user.last_test:
        current_user.change_last_test(test.tip)
        db.session.commit()

    if 'questions' in session and 'points' in session:
        questions = session['questions']
        print(questions)
        points = session['points']
    else:
        return redirect(url_for('views.home')) 


    return render_template('results.html', user = current_user, questions = questions, points = points)


def cine_alege():

    alege = User.query.filter_by(level = 'team').filter_by(config = 'no',frame= 'no').order_by(desc(User.punctaj)).first()

    return alege.id

def get_clasament():
        
    clasament = User.query.filter_by(level = 'team').order_by(desc(User.punctaj)).all()

    return clasament