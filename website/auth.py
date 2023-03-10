from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User

auth = Blueprint('auth', __name__)
 

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        numeEchipa = request.form.get('numeEchipa')
        parola = request.form.get('parolaEchipa')    

        print(numeEchipa, parola)   

        user = User.query.filter_by(username = numeEchipa).first()
        if user:
            if user.parola == parola:
                flash('Bine ai venit in aplicatia DroWo23', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Parola incorecta.', category='error')
        else:
            flash('Aceasta echipa nu exista in baza de date', category='error')


    return render_template("login.html", user=current_user)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

    