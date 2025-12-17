from flask import Blueprint, render_template, request, redirect, session, current_app, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from os import path

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    username = session.get('login', 'anonymous')
    return render_template('lab8/lab8.html', username=username)

@lab8.route('/lab8/login')
def login():
    return render_template('lab8/login.html')


@lab8.route('/lab8/register')
def register():
    return render_template('lab8/register.html')


@lab8.route('/lab8/articles')
def articles():
    return render_template('lab8/articles.html')


@lab8.route('/lab8/create')
def create():
    return render_template('lab8/create.html')