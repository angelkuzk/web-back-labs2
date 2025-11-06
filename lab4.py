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

def check_auth():
    return 'login' in session


def get_current_user():
    if 'login' in session:
        return next((u for u in users if u['login'] == session['login']), None)
    return None


@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    name = request.form.get('name')
    gender = request.form.get('gender')

    if not login:
        return render_template('lab4/register.html', error='Не введён логин', login=login, name=name)
    
    if not name:
        return render_template('lab4/register.html', error='Не введено имя', login=login, name=name)
    
    if not password:
        return render_template('lab4/register.html', error='Не введён пароль', login=login, name=name)
    
    if password != password_confirm:
        return render_template('lab4/register.html', error='Пароли не совпадают', login=login, name=name)
    
    if any(user['login'] == login for user in users):
        return render_template('lab4/register.html', error='Пользователь с таким логином уже существует', login=login, name=name)
    
    new_user = {
        'login': login,
        'password': password,
        'name': name,
        'gender': gender
    }
    users.append(new_user)
    
    session['login'] = login
    return redirect('/lab4/users')


@lab4.route('/lab4/users')
def users_list():
    if not check_auth():
        return redirect('/lab4/login')
    
    current_user = get_current_user()
    return render_template('lab4/users.html', users=users, current_user=current_user)


@lab4.route('/lab4/delete_user', methods=['POST'])
def delete_user():
    if not check_auth():
        return redirect('/lab4/login')
    
    current_login = session['login']
    global users
    users = [user for user in users if user['login'] != current_login]
    
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/edit_user', methods=['GET', 'POST'])
def edit_user():
    if not check_auth():
        return redirect('/lab4/login')
    
    current_user = get_current_user()
    
    if request.method == 'GET':
        return render_template('lab4/edit_user.html', user=current_user)
    
    login = request.form.get('login')
    name = request.form.get('name')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    gender = request.form.get('gender')

    if not login:
        return render_template('lab4/edit_user.html', user=current_user, error='Не введён логин')
    
    if not name:
        return render_template('lab4/edit_user.html', user=current_user, error='Не введено имя')
    
    if login != current_user['login'] and any(user['login'] == login for user in users):
        return render_template('lab4/edit_user.html', user=current_user, error='Пользователь с таким логином уже существует')
    
    if password or password_confirm:
        if password != password_confirm:
            return render_template('lab4/edit_user.html', user=current_user, error='Пароли не совпадают')
        if not password:
            return render_template('lab4/edit_user.html', user=current_user, error='Не введён пароль')
    
    for user in users:
        if user['login'] == current_user['login']:
            user['login'] = login
            user['name'] = name
            user['gender'] = gender
            if password:
                user['password'] = password
            break
    
    if login != current_user['login']:
        session['login'] = login
    
    return redirect('/lab4/users')

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')
    
    temperature = request.form.get('temperature')
    
    if not temperature:
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')
    
    try:
        temp = int(temperature)
    except ValueError:
        return render_template('lab4/fridge.html', error='Ошибка: температура должна быть числом')

    if temp < -12:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    elif temp > -1:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
    elif -12 <= temp <= -9:
        snowflakes = 3
        message = f'Установлена температура: {temp}°C'
    elif -8 <= temp <= -5:
        snowflakes = 2
        message = f'Установлена температура: {temp}°C'
    elif -4 <= temp <= -1:
        snowflakes = 1
        message = f'Установлена температура: {temp}°C'
    else:
        snowflakes = 0
        message = f'Установлена температура: {temp}°C'
    
    return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes, temperature=temperature)


@lab4.route('/lab4/zerno', methods=['GET', 'POST'])
def grain():
    if request.method == 'GET':
        return render_template('lab4/zerno.html')
    
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')
    
    prices = {
        'barley': 12000,   
        'oats': 8500,      
        'wheat': 9000,     
        'rye': 15000       
    }
    
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    if not weight:
        return render_template('lab4/zerno.html', error='Ошибка: не указан вес')
    
    try:
        weight_num = float(weight)
    except ValueError:
        return render_template('lab4/zerno.html', error='Ошибка: вес должен быть числом')
    
    if weight_num <= 0:
        return render_template('lab4/zerno.html', error='Ошибка: вес должен быть больше 0')
    
    if weight_num > 100:
        return render_template('lab4/zerno.html', error='Такого объёма сейчас нет в наличии')
    
    price_per_ton = prices.get(grain_type)
    if not price_per_ton:
        return render_template('lab4/zerno.html', error='Ошибка: не выбран тип зерна')
    
    total = weight_num * price_per_ton
    discount = 0
    discount_applied = False
    
    if weight_num > 10:
        discount = total * 0.1
        total -= discount
        discount_applied = True
    
    grain_name = grain_names.get(grain_type)
    
    return render_template('lab4/zerno.html', 
                         success=True,
                         grain_name=grain_name,
                         weight=weight_num,
                         total=total,
                         discount_applied=discount_applied,
                         discount=discount,
                         grain_type=grain_type)