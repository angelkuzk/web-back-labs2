from flask import Blueprint, render_template, request, make_response, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div', methods = ['GET', 'POST'])
def div_form():
    if request.method == 'GET':
        return render_template('lab4/div.html')
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/div.html', error='Оба поля должны содержать числа!')
    
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result, show_result=True)


@lab4.route('/lab4/sum', methods=['GET', 'POST'])
def sum_form():
    if request.method == 'GET':
        return render_template('lab4/sum.html')
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 0
    if x2 == '':
        x2 = 0
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/sum.html', error='Поля должны содержать числа!')
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/ym', methods=['GET', 'POST'])
def mult_form():
    if request.method == 'GET':
        return render_template('lab4/ym.html')
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 1
    if x2 == '':
        x2 = 1
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/ym.html', error='Поля должны содержать числа!')  
    result = x1 * x2
    return render_template('lab4/ym.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/raz', methods=['GET', 'POST'])
def sub_form():
    if request.method == 'GET':
        return render_template('lab4/raz.html')
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/raz.html', error='Оба поля должны быть заполнены!')
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/raz.html', error='Оба поля должны содержать числа!')
    result = x1 - x2
    return render_template('lab4/raz.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/st', methods=['GET', 'POST'])
def pow_form():
    if request.method == 'GET':
        return render_template('lab4/st.html')
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/st.html', error='Оба поля должны быть заполнены!')
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/st.html', error='Оба поля должны содержать числа!')
    if x1 == 0 and x2 == 0:
        return render_template('lab4/st.html', error='Оба числа не могут быть нулями!')
    result = x1 ** x2
    return render_template('lab4/st.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)

    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login' : 'alex', 'password': '123', 'name': 'Александр Петров', 'gender': 'male'},
    {'login' : 'bob', 'password': '555', 'name': 'Боб Смит', 'gender': 'male'},
    {'login' : 'alina', 'password': '0308', 'name': 'Алина Геворкян', 'gender': 'female'},
    {'login' : 'angelkuz', 'password': '0204', 'name': 'Ангелина Кузнецова', 'gender': 'female'},
    {'login' : 'katya', 'password': '1711', 'name': 'Екатерина Атаманкина', 'gender': 'female'},
    {'login' : 'dima', 'password': '2501', 'name': 'Дмитрий Игуменшев', 'gender': 'male'},
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            user = next((u for u in users if u['login'] == session['login']), None)
            name = user['name'] if user else session['login']
        else:
            authorized = False
            name = ''
        return render_template("lab4/login.html", authorized=authorized, name=name)
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        return render_template('lab4/login.html', error='Не введён логин', login=login, authorized=False)
    
    if not password:
        return render_template('lab4/login.html', error='Не введён пароль', login=login, authorized=False)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')
    
    error = 'Неверный логин и/или пароль'
    return render_template('lab4/login.html', error=error, login=login, authorized=False)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')