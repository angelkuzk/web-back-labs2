from flask import Blueprint, render_template, request, make_response, redirect, session, current_app, abort, jsonify
import psycopg2
from datetime import datetime
from psycopg2.extras import RealDictCursor
import sqlite3
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