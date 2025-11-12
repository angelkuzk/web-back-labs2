from flask import Blueprint, render_template, request, redirect, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    username = session.get('login', 'anonymous')
    return render_template('lab5/lab5.html', username=username)


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
    real_name = request.form.get('real_name', '')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все обязательные поля')
    
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
            cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);", (login, password_hash, real_name))
        else:
            cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);", (login, password_hash, real_name))

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
        session['user_id'] = user['id']
        db_close(conn, cur)
        return render_template('lab5/success_login.html', login=login)
    
    except Exception as e:
        return render_template('lab5/login.html', error=f'Ошибка базы данных: {str(e)}')


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    return redirect('/lab5/')
    

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('/lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('/lab5/create_article.html', error='Заполните название и текст статьи')

    if len(title.strip()) == 0 or len(article_text.strip()) == 0:
        return render_template('/lab5/create_article.html', error='Название и текст статьи не могут быть пустыми')

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
            cur.execute("INSERT INTO articles (user_id, title, article_text, is_public) VALUES (%s, %s, %s, %s);", 
                       (user_id, title.strip(), article_text.strip(), False))
        else:
            cur.execute("INSERT INTO articles (user_id, title, article_text, is_public) VALUES (?, ?, ?, ?);", 
                       (user_id, title.strip(), article_text.strip(), False))
            
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
            cur.execute("SELECT * FROM articles WHERE user_id=%s  ORDER BY is_favorite DESC, id DESC;", (user_id,))
        else:
            cur.execute("SELECT * FROM articles WHERE user_id=? ORDER BY is_favorite DESC, id DESC;", (user_id,))
            
        articles = cur.fetchall()

        db_close(conn, cur)
        if not articles:
            return render_template('/lab5/articles.html', articles=articles, no_articles=True)
        
        return render_template('/lab5/articles.html', articles=articles, no_articles=False)
    
    except Exception as e:
        return f"Ошибка базы данных: {str(e)}"
    

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    try:
        conn, cur = db_connect()

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT a.*, u.login FROM articles a JOIN users u ON a.user_id = u.id WHERE a.id=%s AND u.login=%s;", 
                       (article_id, login))
        else:
            cur.execute("SELECT a.*, u.login FROM articles a JOIN users u ON a.user_id = u.id WHERE a.id=? AND u.login=?;", 
                       (article_id, login))
            
        article = cur.fetchone()

        if not article:
            db_close(conn, cur)
            return redirect('/lab5/list')

        if request.method == 'GET':
            db_close(conn, cur)
            return render_template('/lab5/edit_article.html', article=article)

        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_public = request.form.get('is_public') == 'on'
        is_favorite = request.form.get('is_favorite') == 'on'

        if not title or not article_text:
            db_close(conn, cur)
            return render_template('/lab5/edit_article.html', article=article, error='Заполните название и текст статьи')

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("UPDATE articles SET title=%s, article_text=%s, is_public=%s, is_favorite=%s WHERE id=%s;", 
                       (title.strip(), article_text.strip(), is_public, is_favorite, article_id))
        else:
            cur.execute("UPDATE articles SET title=?, article_text=?, is_public=?, is_favorite=? WHERE id=?;", 
                       (title.strip(), article_text.strip(), is_public, is_favorite, article_id))
            
        db_close(conn, cur)
        return redirect('/lab5/list')
    
    except Exception as e:
        return render_template('/lab5/edit_article.html', article=article, error=f'Ошибка базы данных: {str(e)}')

@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    try:
        conn, cur = db_connect()

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT a.*, u.login FROM articles a JOIN users u ON a.user_id = u.id WHERE a.id=%s AND u.login=%s;", 
                       (article_id, login))
        else:
            cur.execute("SELECT a.*, u.login FROM articles a JOIN users u ON a.user_id = u.id WHERE a.id=? AND u.login=?;", 
                       (article_id, login))
            
        article = cur.fetchone()

        if not article:
            db_close(conn, cur)
            return redirect('/lab5/list')

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
        else:
            cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

        db_close(conn, cur)
        return redirect('/lab5/list')
    
    except Exception as e:
        return f"Ошибка при удалении: {str(e)}"
    

@lab5.route('/lab5/users')
def users_list():
    try:
        conn, cur = db_connect()
        
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT login, real_name FROM users ORDER BY login;")
        else:
            cur.execute("SELECT login, real_name FROM users ORDER BY login;")
            
        users = cur.fetchall()
        db_close(conn, cur)
        
        return render_template('lab5/users.html', users=users)
    
    except Exception as e:
        return f"Ошибка базы данных: {str(e)}"
    

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    try:
        conn, cur = db_connect()

        if request.method == 'GET':
            if current_app.config.get('DB_TYPE') == 'postgres':
                cur.execute("SELECT real_name FROM users WHERE login=%s;", (login,))
            else:
                cur.execute("SELECT real_name FROM users WHERE login=?;", (login,))
                
            user = cur.fetchone()
            current_real_name = user['real_name'] if user else ''
            
            db_close(conn, cur)
            return render_template('lab5/profile.html', current_real_name=current_real_name)

        real_name = request.form.get('real_name', '')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password and new_password != confirm_password:
            db_close(conn, cur)
            return render_template('lab5/profile.html', 
                                 current_real_name=real_name,
                                 error='Пароли не совпадают')

        if new_password:
            password_hash = generate_password_hash(new_password)
            if current_app.config.get('DB_TYPE') == 'postgres':
                cur.execute("UPDATE users SET real_name=%s, password=%s WHERE login=%s;", 
                           (real_name, password_hash, login))
            else:
                cur.execute("UPDATE users SET real_name=?, password=? WHERE login=?;", 
                           (real_name, password_hash, login))
        else:
            if current_app.config.get('DB_TYPE') == 'postgres':
                cur.execute("UPDATE users SET real_name=%s WHERE login=%s;", (real_name, login))
            else:
                cur.execute("UPDATE users SET real_name=? WHERE login=?;", (real_name, login))

        db_close(conn, cur)
        return render_template('lab5/profile.html', 
                             current_real_name=real_name,
                             success='Данные успешно обновлены')

    except Exception as e:
        return render_template('lab5/profile.html', 
                             current_real_name=request.form.get('real_name', ''),
                             error=f'Ошибка базы данных: {str(e)}')
    

@lab5.route('/lab5/public')
def public_articles():
    try:
        conn, cur = db_connect()

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("""
                SELECT a.*, u.login as author_login, u.real_name as author_name 
                FROM articles a 
                JOIN users u ON a.user_id = u.id 
                WHERE a.is_public = TRUE 
                ORDER BY a.is_favorite DESC, a.id DESC;
            """)
        else:
            cur.execute("""
                SELECT a.*, u.login as author_login, u.real_name as author_name 
                FROM articles a 
                JOIN users u ON a.user_id = u.id 
                WHERE a.is_public = 1 
                ORDER BY a.is_favorite DESC, a.id DESC;
            """)
            
        articles = cur.fetchall()
        db_close(conn, cur)
        
        return render_template('lab5/public_articles.html', 
                             articles=articles, 
                             no_articles=not articles)
    
    except Exception as e:
        return f"Ошибка базы данных: {str(e)}"