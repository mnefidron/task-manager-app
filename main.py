# main.py
from interface import TaskManager
import database  # Явно импортируйте модуль для инициализации БД

if __name__ == "__main__":
    # Убедитесь, что БД существует перед запуском приложения
    database.init_db()
    app = TaskManager()
    app.mainloop()