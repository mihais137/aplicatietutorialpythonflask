from flask import Blueprint, render_template, request, redirect, url_for, session
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
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                session['error'] = "Parola incorecta"
                return redirect(url_for('views.error'))
        else:
            session['error'] = "Aceasta echipa nu exista in baza de date"
            return redirect(url_for('views.error'))


    return render_template("login.html", user=current_user)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

    