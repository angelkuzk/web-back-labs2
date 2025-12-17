import sqlite3

conn = sqlite3.connect('angelina_kuznetosva_orm.db')
cursor = conn.cursor()

print("Создание таблиц в angelina_kuznetosva_orm.db")

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(162) NOT NULL,
    real_name VARCHAR(100)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login_id INTEGER,
    title VARCHAR(50) NOT NULL,
    article_text TEXT NOT NULL,
    is_favorite BOOLEAN,
    is_public BOOLEAN,
    likes INTEGER,
    FOREIGN KEY(login_id) REFERENCES users (id)
)
''')

conn.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("\nСозданы таблицы:")
for table in tables:
    print(f"  - {table[0]}")
    cursor.execute(f"PRAGMA table_info({table[0]})")
    columns = cursor.fetchall()
    for col in columns:
        print(f"    {col[1]} ({col[2]})")

conn.close()