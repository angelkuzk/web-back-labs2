import sqlite3
import sys
from tabulate import tabulate

def view_database():
    try:
        conn = sqlite3.connect('films.db')
        cursor = conn.cursor()
        
        # 1. Показать все таблицы
        print("🔍 ТАБЛИЦЫ В БАЗЕ ДАННЫХ:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            print(f"   📁 {table[0]}")
        
        # 2. Показать структуру таблицы films
        print("\n📊 СТРУКТУРА ТАБЛИЦЫ films:")
        cursor.execute("PRAGMA table_info(films)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"   • {col[1]} ({col[2]})")
        
        # 3. Показать данные
        print("\n🎬 ДАННЫЕ В ТАБЛИЦЕ films:")
        cursor.execute("SELECT * FROM films")
        rows = cursor.fetchall()
        
        if not rows:
            print("   ⚠️ Таблица пуста!")
        else:
            # Получаем названия столбцов
            cursor.execute("PRAGMA table_info(films)")
            headers = [col[1] for col in cursor.fetchall()]
            
            # Формируем данные для таблицы
            table_data = []
            for row in rows:
                # Обрезаем описание для читаемости
                row_list = list(row)
                if len(str(row_list[4])) > 50:
                    row_list[4] = str(row_list[4])[:47] + "..."
                table_data.append(row_list)
            
            # Выводим таблицу
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            print(f"\n📈 Всего записей: {len(rows)}")
        
        conn.close()
        
    except sqlite3.OperationalError as e:
        print(f"❌ Ошибка: {e}")
        print("Возможно, файл films.db не существует или поврежден.")
        
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

if __name__ == "__main__":
    view_database()