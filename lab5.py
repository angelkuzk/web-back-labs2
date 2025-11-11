from flask import Blueprint, render_template, request, redirect, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', username=session.get('login', 'anonymous'))


def db_connect():
    if current_app.config.get('DB_TYPE') == 'postgres':
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='angelina_kuznetsova_knowledge_base',  
            user='angelina_kuznetsova_knowledge_base',      
            password='123',
            port=5432
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row 
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()  


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    try:
        conn, cur = db_connect()

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT login FROM users WHERE login=?;", (login,))

        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html',
                                error="Такой пользователь уже существует")
        
        password_hash = generate_password_hash(password)
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
        else:
            cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))

        db_close(conn, cur)
        return render_template('lab5/success.html', login=login)
    
    except Exception as e:
        return render_template('lab5/register.html', error=f'Ошибка базы данных: {str(e)}')
    

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error="Заполните все поля")
    
    try:
        conn, cur = db_connect()
        
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT * FROM users WHERE login=?;", (login,))

        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html',
                                error='Логин и/или пароль неверны')
        
        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html',
                                error='Логин и/или пароль неверны')
        
        session['login'] = login
        db_close(conn, cur)
        return render_template('lab5/success_login.html', login=login)
    
    except Exception as e:
        return render_template('lab5/login.html', error=f'Ошибка базы данных: {str(e)}')
    

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('/lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not (title and article_text):
        return render_template('/lab5/create_article.html', error='Заполните все поля')

    try:
        conn, cur = db_connect()

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT * FROM users WHERE login=?;", (login,))
       
        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return redirect('/lab5/login')
        
        user_id = user["id"]

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s);", 
                       (user_id, title, article_text))
        else:
            cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (?, ?, ?);", 
                       (user_id, title, article_text))
            
        db_close(conn, cur)
        return redirect('/lab5')    
    
    except Exception as e:
        return render_template('/lab5/create_article.html', error=f'Ошибка базы данных: {str(e)}')
    

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    try:
        conn, cur = db_connect()

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login=?;", (login,))
            
        user_result = cur.fetchone()
        
        if not user_result:
            db_close(conn, cur)
            return redirect('/lab5/login')
            
        user_id = user_result["id"]

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT * FROM articles WHERE user_id=%s;", (user_id,))
        else:
            cur.execute("SELECT * FROM articles WHERE user_id=?;", (user_id,))
            
        articles = cur.fetchall()
        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=articles)
    
    except Exception as e:
        return f"Ошибка базы данных: {str(e)}"