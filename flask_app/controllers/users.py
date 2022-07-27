from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models import user,recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/user/register', methods=["POST"])
def register():
    if not user.User.validate_register(request.form):
        return redirect('/')

    data={
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
    }
    userId = user.User.save_new_user(data)
    session['user_id'] = userId
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('dashboard.html', recipes=recipe.Recipe.get_recipes())

@app.route('/user/login', methods=["POST"])
def login():
    if not user.User.validate_login(request.form):
        return redirect('/')
    userId = user.User.get_by_email(request.form)
    session['user_id'] = userId.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')