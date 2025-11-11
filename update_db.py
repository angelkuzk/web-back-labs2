import psycopg2

def update_database():
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='angelina_kuznetsova_knowledge_base',  
            user='angelina_kuznetsova_knowledge_base',      
            password='123',
            port=5432
        )
        cur = conn.cursor()

        cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS real_name TEXT;")
        
        cur.execute("ALTER TABLE articles ADD COLUMN IF NOT EXISTS is_favorite BOOLEAN DEFAULT FALSE;")
        
        conn.commit()
        cur.close()
        conn.close()
        print("База данных успешно обновлена!")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    update_database()