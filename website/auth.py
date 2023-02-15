from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        numeEchipa = request.form.get('numeEchipa')
        parola = request.form.get('parola')        
    return render_template("login.html", boolean=True)

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    return "<p>Logout</p>"

# @auth.route('/testare', methods=['GET', 'POST'])
# def testare():
#     return render_template("testare.html")
    
@auth.route('/shop', methods=['GET', 'POST'])
def shop():
    return render_template("shop.html")
    
@auth.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template("admin.html")
