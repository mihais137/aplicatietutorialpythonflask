from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from .models import User
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
        parola = request.form.get('parola')
        level = request.form.get('level')

        new_user = User(username = username, parola = parola, level = level)
        db.session.add(new_user)
        db.session.commit()

    return render_template('admin_add_teams.html', user = current_user)


@admin.route('/admin_test', methods=['GET', 'POST'])
@login_required
def admin_test():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))

    return render_template('admin_test.html', user = current_user)


@admin.route('/admin_shop', methods=['GET', 'POST'])
@login_required
def admin_shop():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))

    return render_template('admin_shop.html', user = current_user)


@admin.route('/admin_error', methods=['GET', 'POST'])
@login_required
def admin_error():

    if current_user.level != 'admin':
        return redirect(url_for('admin.admin_error'))

    return render_template('admin_error.html', user = current_user)