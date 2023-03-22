from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import User, Test, Drona, Intrebari, Raspunsuri
import pandas as pd
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
        file = request.files['filename']
        file.save(file.filename)

        data =  pd.read_excel(file)
        add_tests(data)

    return render_template('admin_add_tests.html', user = current_user)

@admin.route('/admin_delete_table', methods=['GET', 'POST'])
@login_required
def admin_delete_table():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))
    
    tables = {"test": Test, "user" : User, "intrebari": Intrebari, "raspunsuri": Raspunsuri, "drona" : Drona}
    
    if request.method == 'POST':
        table_delete = request.form.get("table_delete")
        tables[table_delete].query.delete()
        db.session.commit()

    return render_template('admin_delete_table.html', user = current_user)

@admin.route('/admin_delete_drones', methods=['GET', 'POST'])
@login_required
def admin_delete_drones():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))
    
    drone = Drona.query.all()
    
    if request.method == 'POST':
        id_drona = request.form.get("remove_value")
        old_drona = Drona.query.filter_by(id = id_drona).first()
        db.session.delete(old_drona)
        db.session.commit()
        return redirect(url_for("admin.admin_delete_drones"))

    return render_template('admin_delete_drones.html', user = current_user, drone = drone)

@admin.route('/admin_add_points', methods=['GET', 'POST'])
@login_required
def admin_add_points():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))
    
    echipe = User.query.filter_by(level = "team").all()
    
    if request.method == 'POST':
        id_echipa = request.form.get("id_echipa")
        puncte = request.form.get("puncte")

        user = User.query.filter_by(id = id_echipa).first()
        user.change_points(user.punctaj + int(puncte))
        db.session.commit()
        return redirect(url_for("admin.admin_add_points"))


    return render_template('admin_add_points.html', user = current_user, echipe = echipe)


def add_tests(data):

    tests_obj = Test.query.all()
    tests = []
    for t in tests_obj:
        tests.append(t.tip)

    for test in data['Test']:
        if test in tests:
            continue
        else:
            new_test = Test(tip = test, status = "inactiv", durata = 15)
            tests.append(test)
            db.session.add(new_test)
            db.session.commit()
    
    for index, row in data.iterrows():
        # print(row['Test'], row['Intrebare'])
        new_question = Intrebari(intrebare = row['Intrebare'], raspuns_corect = row['RC'], tip_test = Test.query.filter_by(tip = row['Test']).first().id)
        db.session.add(new_question)
        db.session.commit()

    for index, row in data.iterrows():
        new_answer = Raspunsuri(raspuns1 = row['R1'], raspuns2 = row['R2'], raspuns3 = row['R3'], raspuns4 = row['R4'], id_intrebare = Intrebari.query.filter_by(intrebare = row['Intrebare']).first().id)
        db.session.add(new_answer)
        db.session.commit()

    return 0