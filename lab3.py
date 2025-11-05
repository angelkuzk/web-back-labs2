from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name = name if name else "Аноним"
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    age = age if age else "Неизвестно"
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if user == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    drink_name = ''

    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    additions = []
    if request.args.get('milk') == 'on':
        price += 30
        additions.append('молоко')
    if request.args.get('sugar') == 'on':
        price += 10
        additions.append('сахар')
    
    return render_template('lab3/pay.html', price=price, drink_name=drink_name, additions=additions)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    current_color = request.cookies.get('color', '#000000')
    current_bg_color = request.cookies.get('bg_color', '#ffffff')
    current_font_size = request.cookies.get('font_size', '16')
    current_font_family = request.cookies.get('font_family', 'Arial, sans-serif')

    new_color = request.args.get('color')
    new_bg_color = request.args.get('bg_color')
    new_font_size = request.args.get('font_size')
    new_font_family = request.args.get('font_family')

    if new_color or new_bg_color or new_font_size or new_font_family:
        color_to_use = new_color if new_color is not None else current_color
        bg_color_to_use = new_bg_color if new_bg_color is not None else current_bg_color
        font_size_to_use = new_font_size if new_font_size is not None else current_font_size
        font_family_to_use = new_font_family if new_font_family is not None else current_font_family
        
        resp = make_response(render_template('lab3/settings.html', 
                                            color=color_to_use,
                                            bg_color=bg_color_to_use,
                                            font_size=font_size_to_use,
                                            font_family=font_family_to_use))

        if new_color:
            resp.set_cookie('color', new_color, max_age=60*60*24*365)
        if new_bg_color:
            resp.set_cookie('bg_color', new_bg_color, max_age=60*60*24*365)
        if new_font_size:
            resp.set_cookie('font_size', new_font_size, max_age=60*60*24*365)
        if new_font_family:
            resp.set_cookie('font_family', new_font_family, max_age=60*60*24*365)
        
        return resp
    
    return render_template('lab3/settings.html', 
                          color=current_color, 
                          bg_color=current_bg_color, 
                          font_size=current_font_size,
                          font_family=current_font_family)


@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    bedding = request.args.get('bedding')
    baggage = request.args.get('baggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    if not fio:
        errors['fio'] = 'Заполните поле'
    if not shelf:
        errors['shelf'] = 'Выберите полку'
    if not age:
        errors['age'] = 'Заполните поле'
    elif not age.isdigit() or not (1 <= int(age) <= 120):
        errors['age'] = 'Возраст должен быть от 1 до 120 лет'
    if not departure:
        errors['departure'] = 'Заполните поле'
    if not destination:
        errors['destination'] = 'Заполните поле'
    if not date:
        errors['date'] = 'Заполните поле'
    
    if errors or not all([fio, shelf, age, departure, destination, date]):
        return render_template('lab3/ticket_form.html', 
                             errors=errors,
                             fio=fio, shelf=shelf, bedding=bedding, 
                             baggage=baggage, age=age, departure=departure,
                             destination=destination, date=date, insurance=insurance)
    
    if int(age) < 18:
        base_price = 700
        ticket_type = 'Детский билет'
    else:
        base_price = 1000
        ticket_type = 'Взрослый билет'
    
    total_price = base_price
    
    if shelf in ['lower', 'lower-side']:
        total_price += 100
    if bedding == 'on':
        total_price += 75
    if baggage == 'on':
        total_price += 250
    if insurance == 'on':
        total_price += 150
    
    return render_template('lab3/ticket_result.html',
                         fio=fio, shelf=shelf, bedding=bedding,
                         baggage=baggage, age=age, departure=departure,
                         destination=destination, date=date, insurance=insurance,
                         ticket_type=ticket_type, total_price=total_price)


@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.set_cookie('color', '', expires=0)
    resp.set_cookie('bg_color', '', expires=0)
    resp.set_cookie('font_size', '', expires=0)
    resp.set_cookie('font_family', '', expires=0)
    return resp


products = [
    {'name': 'iPhone 15 Pro Max', 'price': 133990, 'brand': 'Apple', 'color': 'Титановый', 'storage': '512GB'},
    {'name': 'Samsung Galaxy S25', 'price': 62990, 'brand': 'Samsung', 'color': 'Черный', 'storage': '128GB'},
    {'name': 'Xiaomi 14', 'price': 49990, 'brand': 'Xiaomi', 'color': 'Белый', 'storage': '1TB'},
    {'name': 'Google Pixel 9', 'price': 56990, 'brand': 'Google', 'color': 'Серый', 'storage': '256GB'},
    {'name': 'OnePlus 12', 'price': 69990, 'brand': 'OnePlus', 'color': 'Зеленый', 'storage': '256GB'},
    {'name': 'iPhone 14', 'price': 49990, 'brand': 'Apple', 'color': 'Синий', 'storage': '128GB'},
    {'name': 'Samsung Galaxy A56', 'price': 29990, 'brand': 'Samsung', 'color': 'Фиолетовый', 'storage': '128GB'},
    {'name': 'Xiaomi Redmi 13', 'price': 9990, 'brand': 'Xiaomi', 'color': 'Черный', 'storage': '128GB'},
    {'name': 'Realme 11 Pro+', 'price': 32990, 'brand': 'Realme', 'color': 'Золотой', 'storage': '256GB'},
    {'name': 'Nothing Phone 2', 'price': 27990, 'brand': 'Nothing', 'color': 'Оранжевый', 'storage': '256GB'},
    {'name': 'iPhone 13', 'price': 67990, 'brand': 'Apple', 'color': 'Розовый', 'storage': '256GB'},
    {'name': 'Samsung Galaxy Z Flip 7 FE', 'price': 74990, 'brand': 'Samsung', 'color': 'Сиреневый', 'storage': '256GB'},
    {'name': 'Xiaomi Poco X7 Pro', 'price': 29990, 'brand': 'Xiaomi', 'color': 'Желтый', 'storage': '512GB'},
    {'name': 'Google Pixel 7a', 'price': 27990, 'brand': 'Google', 'color': 'Голубой', 'storage': '128GB'},
    {'name': 'OnePlus Ace 5', 'price': 41990, 'brand': 'OnePlus', 'color': 'Серый', 'storage': '512GB'},
    {'name': 'iPhone SE 3', 'price': 32990, 'brand': 'Apple', 'color': 'Красный', 'storage': '64GB'},
    {'name': 'Samsung Galaxy A26', 'price': 19990, 'brand': 'Samsung', 'color': 'Кремовый', 'storage': '256GB'},
    {'name': 'OnePlus 13T', 'price': 44990, 'brand': 'OnePlus', 'color': 'Розовый', 'storage': '256GB'},
    {'name': 'Realme GT7', 'price': 39990, 'brand': 'Realme', 'color': 'Фиолетовый', 'storage': '512GB'},
    {'name': 'iPhone 11', 'price': 35990, 'brand': 'Apple', 'color': 'Черный', 'storage': '64GB'}
]
@lab3.route('/lab3/products')
def products_search():
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')
    
    all_prices = [product['price'] for product in products]
    real_min_price = min(all_prices)
    real_max_price = max(all_prices)
    
    min_price_input = request.args.get('min_price', '')
    max_price_input = request.args.get('max_price', '')
    
    if 'reset' in request.args:
        resp = make_response(render_template('lab3/products.html',
                                           products=products,
                                           min_price='',
                                           max_price='',
                                           real_min_price=real_min_price,
                                           real_max_price=real_max_price,
                                           filtered_count=len(products),
                                           total_count=len(products)))
        resp.set_cookie('min_price', '', expires=0)
        resp.set_cookie('max_price', '', expires=0)
        return resp
    
    if min_price_input or max_price_input:
        min_price = int(min_price_input) if min_price_input else real_min_price
        max_price = int(max_price_input) if max_price_input else real_max_price
        
        if min_price > max_price:
            min_price, max_price = max_price, min_price
        
        filtered_products = [
            product for product in products 
            if min_price <= product['price'] <= max_price
        ]
        
        resp = make_response(render_template('lab3/products.html',
                                           products=filtered_products,
                                           min_price=min_price,
                                           max_price=max_price,
                                           real_min_price=real_min_price,
                                           real_max_price=real_max_price,
                                           filtered_count=len(filtered_products),
                                           total_count=len(products)))
        resp.set_cookie('min_price', str(min_price), max_age=60*60*24*30)
        resp.set_cookie('max_price', str(max_price), max_age=60*60*24*30)
        return resp
    
    if min_price_cookie and max_price_cookie:
        min_price = int(min_price_cookie)
        max_price = int(max_price_cookie)
        
        filtered_products = [
            product for product in products 
            if min_price <= product['price'] <= max_price
        ]
        
        return render_template('lab3/products.html',
                             products=filtered_products,
                             min_price=min_price,
                             max_price=max_price,
                             real_min_price=real_min_price,
                             real_max_price=real_max_price,
                             filtered_count=len(filtered_products),
                             total_count=len(products))
    
    return render_template('lab3/products.html',
                         products=products,
                         min_price='',
                         max_price='',
                         real_min_price=real_min_price,
                         real_max_price=real_max_price,
                         filtered_count=len(products),
                         total_count=len(products))