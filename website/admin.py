from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
import pandas as pd
from .models import User, Test, Drona
from . import db
admin = Blueprint('admin', __name__)


@admin.route('/admin_page', methods=['GET', 'POST'])
@login_required
def admin_page():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))

    return render_template('admin_page.html', user = current_user)


@admin.route('/admin_add_teams', methods=['GET', 'POST'])
@login_required
def admin_add_teams():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))

    if request.method == "POST":
        username = request.form.get('username')
        level = request.form.get('level')
        password = request.form.get('password')
        
        if username == '' or level == '' or password == '':
            flash('Toate cele 3 campuri trebuie sa fie completate pentru a putea adauga o echipa', category='error')
            return(redirect(url_for('admin.admin_add_teams')))

        if level != 'team':
            flash('Poti adauga doar useri cu level = "team" ', category = 'error')
            return(redirect(url_for('admin.admin_add_teams')))

        new_team = User(username=username, level=level, password=password)
        db.session.add(new_team)
        db.session.commit()
        flash('Ai adaugat o noua echipa', category='succes')

    return render_template('admin_add_teams.html', user = current_user)


@admin.route('/admin_test', methods=['GET', 'POST'])
@login_required
def admin_test():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))


    tests = Test.query.all()

    if request.method == "POST":
        test_id = request.form.get('change_value')

        test = Test.query.filter_by(id = test_id).first()
        if test.status == "activ":
            test.change_status("inactiv")
        else:
            test.change_status("activ")

        flash('Schimbarea a fost facuta')
        db.session.commit()


    return render_template('admin_test.html', user = current_user, tests = tests)


@admin.route('/admin_shop', methods=['GET', 'POST'])
@login_required
def admin_shop():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))

    if request.method == "POST":
        descriere = request.form.get('descriereDrona')
        nume = request.form.get('numeDrona')
        stoc = request.form.get('stocDrona')
        poza = request.form.get('pozaDrona')
        flash("Ai bagat o drona cu succes coae", category='success')
        print(descriere, nume, stoc, poza)

        new_Drona = Drona(nume = nume, descriere = descriere, stoc = stoc, poza = poza)
        db.session.add(new_Drona)
        db.session.commit()


    return render_template('admin_shop.html', user = current_user)


@admin.route('/admin_error', methods=['GET', 'POST'])
@login_required
def admin_error():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))

    return render_template('admin_error.html', user = current_user)


@admin.route('/admin_sign_up', methods=['GET', 'POST'])
def admin_sign_up():
    
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        code = request.form.get('code')

        if code != "DROWO23ADMIN":
            return redirect(url_for("views.home"))
        flash("Ai creat un cont de admin cu succes!", 'message')
        admin = User(username=username, password=password, level = "admin")
        db.session.add(admin)
        db.session.commit()

    return render_template('admin_sign_up.html', user = current_user)


@admin.route('/admin_reset', methods=['GET', 'POST'])
@login_required
def admin_reset():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))
    
    test = Test.query.filter_by(status = 'activ').first()
    durata = test.durata

    return render_template('admin_reset.html', user = current_user, durata = durata)

@admin.route('/admin_add_tests', methods=['GET', 'POST'])
@login_required
def admin_add_tests():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))
    
    if request.method == "POST":
        file = request.form.get('filename')
        data = pd.read_excel(file)

        

    return render_template('admin_add_tests.html', user = current_user)