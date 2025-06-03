import unittest
import crud
import database
from datetime import datetime, timedelta

class TestTaskManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        database.init_db()
    
    def test_crud_operations(self):
        # Тест создания задачи
        title = "Тестовая задача"
        description = "Это тестовая задача"
        deadline = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        priority = "средний"
        status = "To Do"
        assignees = ["Иван Иванов", "Мария Петрова"]
        
        crud.create_task(title, description, deadline, priority, status, assignees)
        
        # Тест получения задач
        tasks = crud.get_tasks()
        self.assertGreater(len(tasks), 0)
        
        # Получаем последнюю задачу
        task = tasks[-1]
        task_id = task[0]
        
        # Тест обновления задачи
        new_title = "Обновленная тестовая задача"
        new_description = "Обновленное описание"
        new_deadline = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        new_priority = "высокий"
        new_status = "In Progress"
        new_assignees = ["Алексей Смирнов"]
        
        crud.update_task(task_id, new_title, new_description, new_deadline, new_priority, new_status, new_assignees)
        
        # Проверяем обновленную задачу
        updated_tasks = crud.get_tasks()
        updated_task = next(t for t in updated_tasks if t[0] == task_id)
        
        self.assertEqual(updated_task[1], new_title)
        self.assertEqual(updated_task[2], new_description)
        self.assertEqual(updated_task[3], new_deadline)
        self.assertEqual(updated_task[4], new_priority)
        self.assertEqual(updated_task[5], new_status)
        self.assertEqual(updated_task[6], ",".join(new_assignees))
        
        # Тест удаления задачи
        crud.delete_task(task_id)
        deleted_tasks = crud.get_tasks()
        self.assertEqual(len([t for t in deleted_tasks if t[0] == task_id]), 0)

if __name__ == '__main__':
    unittest.main()