from flask import Blueprint, render_template, flash, request, redirect,url_for
from flask_login import login_required, current_user
from . import db
from website.models import Drona
from website.models import User


views = Blueprint('views', __name__)

@views.route('/')
def home():

    #calculare_clasament()
    
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
    
    clasament=User.query.sort_values(by="punctaj", ascending=False).all()

    for x in range(len(clasament)):
        clasament[x]=clasament[x].id
    
    for x, i in clasament, range(len(clasament)):
        user=User.query.filter_by(id=x).first()
        user.pozitie=i+1

    for i in range(len(clasament)):
        user=User.query.filter_by(pozitie=i).first()
        if user.config=="":
            poz=user.pozitie
            return poz
        else:
            continue