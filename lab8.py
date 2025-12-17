from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from db import db
from db.models import User, Article

lab8 = Blueprint('lab8', __name__, template_folder='templates/lab8')

@lab8.route('/')  
def lab():
    if current_user.is_authenticated:
        username = current_user.login
    else:
        username = 'anonymous'
    return render_template('lab8.html', username=username)

@lab8.route('/login', methods=['GET', 'POST'])  
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember_me') == 'on'
    
    if not login_form or not login_form.strip():
        return render_template('login.html', error='Введите логин!')
    if not password_form or not password_form.strip():
        return render_template('login.html', error='Введите пароль!')
    
    user = User.query.filter_by(login=login_form).first()
    
    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember_me)
        return redirect('/lab8/')
    
    return render_template('login.html', error='Ошибка входа: логин и/или пароль неверны')

@lab8.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/register', methods=['GET', 'POST'])  
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or not login_form.strip():
        return render_template('register.html', error='Введите логин!')
    if not password_form or not password_form.strip():
        return render_template('register.html', error='Введите пароль!')

    login_exists = User.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = User(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user, remember=False)
    
    return redirect('/lab8/')

@lab8.route('/articles')  
@login_required
def articles():
    return "список статей"

@lab8.route('/create')  
@login_required
def create():
    return render_template('create.html')