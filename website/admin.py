from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from .models import User, Test
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
        
        print(username, level, password)

        new_team = User(username=username, level=level, password=password)
        db.session.add(new_team)
        db.session.commit()

    return render_template('admin_add_teams.html', user = current_user)


@admin.route('/admin_test', methods=['GET', 'POST'])
@login_required
def admin_test():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))

    #se preiau toate teste cu Test.query.all()
    #se afiseaza toate
    #fiecare au un buton in dreptul lor cu Activ/Inactiv si asa putem porni testele  

    tests = Test.query.all()

    return render_template('admin_test.html', user = current_user, tests = tests)


@admin.route('/admin_shop', methods=['GET', 'POST'])
@login_required
def admin_shop():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))

    #formular prin care se adauga noi produse

    return render_template('admin_shop.html', user = current_user)


@admin.route('/admin_error', methods=['GET', 'POST'])
@login_required
def admin_error():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))

    return render_template('admin_error.html', user = current_user)


@admin.route('/admin_sign_up', methods=['GET', 'POST'])
def admin_sign_up():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))
    
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        code = request.form.get('code')

        if code != "DROWO23ADMIN":
            return redirect(url_for("views.home"))
        
        admin = User(username=username, password=password)
        db.session.add(admin)
        db.session.commit()

    return render_template('admin_sign_up.html', user = current_user)