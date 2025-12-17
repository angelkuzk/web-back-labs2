from app import app
from db import db
from db.models import User, Article

# Создаем все таблицы
with app.app_context():
    db.create_all()
    print("✅ Таблицы успешно созданы!")
    print("📊 Созданы таблицы: users, articles")