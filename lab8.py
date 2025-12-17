from flask import Blueprint, render_template, request, redirect, session, current_app, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from os import path
from db import db
from db.models import User, Article

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    username = session.get('login', 'anonymous')
    return render_template('lab8/lab8.html', username=username)

@lab8.route('/lab8/login')
def login():
    return render_template('lab8/login.html')


@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or not login_form.strip():
        return render_template('lab8/register.html', error='Введите логин!')
    if not password_form or not password_form.strip():
        return render_template('lab8/register.html', error='Введите пароль!')

    login_exists = User.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = User(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    session['login'] = login_form
    session['user_id'] = new_user.id
    
    return redirect('/lab8/')


@lab8.route('/lab8/articles')
def articles():
    return render_template('lab8/articles.html')


@lab8.route('/lab8/create')
def create():
    return render_template('lab8/create.html')