from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import sqlite3
from contextlib import closing


lab7 = Blueprint('lab7', __name__)

def init_db():
    with closing(sqlite3.connect('films.db')) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS films (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                title_ru TEXT NOT NULL,
                year INTEGER NOT NULL,
                description TEXT NOT NULL
            )
        ''')
        
        cursor.execute("SELECT COUNT(*) FROM films")
        if cursor.fetchone()[0] == 0:
            initial_films = [
                ("The Shawshank Redemption", "Побег из Шоушенка", 1994, "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к охранникам, так и к заключённым, добиваясь их особого к себе расположения. Он не теряет надежду и продолжает верить в то, что рано или поздно обретёт свободу и добьётся справедливости."),
                ("Parasite", "Паразиты", 2019, "Обычное корейское семейство Ки-тхэков бедствует, перебиваясь случайными подработками. Однажды сыну семейства, Ки-ву, друзья предлагают подменить их в богатом доме Пак, занимаясь репетиторством с юной наследницей. Проникнув в дом, Ки-ву решает, что и его близким такая жизнь не помешает. Хитростью и обманом они устраиваются в семью Пак на разные должности, но их идеальному существованию наступает внезапный и ужасный конец."),
                ("Spirited Away", "Унесённые призраками", 2001, "Маленькая Тихиро вместе с мамой и папой переезжает в новый дом. Заблудившись по дороге, они оказываются в странном опустевшем городе, где наедаются вкусной едой без разрешения и превращаются в свиней. Теперь Тихиро должна придумать, как спасти своих родителей и вернуться в мир людей, для чего ей придётся работать в таинственном доме для духов, которым управляет жестокая ведьма Юбаба."),
                ("Dune", "Дюна", 2021, "Человечество расселилось по далёким планетам, а власть над космосом держит древний орден. Наследник знатного дома Пол Атрейдес вместе с семьёй отправляется на самую опасную планету во Вселенной — Дюну, источник особой специи, необходимой для межзвёздных путешествий. Здесь разворачивается жестокая борьба за власть и ресурсы, а сам Пол оказывается в центре многовекового пророчества, способного изменить судьбу всего человечества."),
                ("Se7en", "Семь", 1995, "Детектив Уильям Сомерсет — ветеран полиции, мечтающий уйти на пенсию и уехать подальше от греха и смрада города. Но перед этим ему приходится взяться за обучение молодого напарника — импульсивного Дэвида Миллса. Вместе они расследуют серию жестоких убийств, каждое из которых символически основано на одном из семи смертных грехов. По мере продвижения расследования становится ясно, что убийца не остановится, пока не исполнит свой чудовищный план до конца.")
            ]
            cursor.executemany(
                "INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)",
                initial_films
            )
        conn.commit()

init_db()

def get_db_connection():
    conn = sqlite3.connect('films.db')
    conn.row_factory = sqlite3.Row
    return conn

def validate_film_data(film_data):
    errors = {}
    
    title_ru = film_data.get('title_ru', '').strip()
    if not title_ru:
        errors['title_ru'] = 'Русское название обязательно'
    
    title = film_data.get('title', '').strip()
    if not title and not title_ru:
        errors['title'] = 'Название на оригинальном языке обязательно, если русское название пустое'
    
    year_str = film_data.get('year', '')
    try:
        year = int(year_str)
        current_year = datetime.now().year
        if year < 1895 or year > current_year + 1:
            errors['year'] = f'Год должен быть от 1895 до {current_year + 1}'
    except (ValueError, TypeError):
        errors['year'] = 'Год должен быть числом'
    
    description = film_data.get('description', '').strip()
    if not description:
        errors['description'] = 'Описание обязательно'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'
    
    return errors

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn = get_db_connection()
    films = conn.execute('SELECT * FROM films').fetchall()
    conn.close()
    
    films_list = []
    for film in films:
        films_list.append({
            'id': film['id'],
            'title': film['title'],
            'title_ru': film['title_ru'],
            'year': film['year'],
            'description': film['description']
        })

    return jsonify(films_list)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_films_by_id(id):
    conn = get_db_connection()
    film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if film is None:
        return jsonify({"error": "Фильм не найден"}), 404

    return jsonify({
        'id': film['id'],
        'title': film['title'],
        'title_ru': film['title_ru'],
        'year': film['year'],
        'description': film['description']
    })


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn = get_db_connection()
    
    film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    if film is None:
        conn.close()
        return jsonify({"error": "Фильм не найден"}), 404

    conn.execute('DELETE FROM films WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    conn = get_db_connection()
    
    film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    if film is None:
        conn.close()
        return jsonify({"error": "Фильм не найден"}), 404

    film_data = request.get_json()

    if not film_data:
        conn.close()
        return jsonify({"error": "Не предоставлены данные для обновления"}), 400

    errors = validate_film_data(film_data)
    if errors:
        return jsonify(errors), 400
    
    title = film_data.get('title', '').strip()
    title_ru = film_data.get('title_ru', '').strip()
    if not title.strip() and title_ru.strip():
        film_data['title'] = title_ru

    conn.execute(
        'UPDATE films SET title = ?, title_ru = ?, year = ?, description = ? WHERE id = ?',
        (film_data['title'], film_data['title_ru'], film_data['year'], film_data['description'], id)
    )
    conn.commit()

    updated_film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    return jsonify({
        'id': updated_film['id'],
        'title': updated_film['title'],
        'title_ru': updated_film['title_ru'],
        'year': updated_film['year'],
        'description': updated_film['description']
    })


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film_data = request.get_json()

    if not film_data:
        return jsonify({"error": "Не предоставлены данные фильма"}), 400
    errors = validate_film_data(film_data)
    if errors:
        return jsonify(errors), 400
    
    title = film_data.get('title', '').strip()
    title_ru = film_data.get('title_ru', '').strip()
    if not title.strip() and title_ru.strip():
        film_data['title'] = title_ru

    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)',
        (film_data['title'], film_data['title_ru'], film_data['year'], film_data['description'])
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({"id": new_id}), 201