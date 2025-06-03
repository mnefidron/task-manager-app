import sqlite3
import os

def init_db():
    # Укажите полный путь к базе данных (например, в текущей директории)
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'task_manager.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  description TEXT,
                  deadline DATE,
                  priority TEXT,
                  status TEXT,
                  assignees TEXT)''')
    
    conn.commit()
    conn.close()

# Вызовите init_db() при импорте модуля
init_db()