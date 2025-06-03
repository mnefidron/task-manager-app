# tests/test_crud.py

import unittest
import crud
import database
from datetime import datetime, timedelta

class TestCRUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        database.init_db()

    def test_create_task(self):
        crud.create_task("Test Task", "Description", (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"), "низкий", "To Do", ["Иван"])
        tasks = crud.get_tasks()
        self.assertGreater(len(tasks), 0)

    def test_update_status(self):
        crud.create_task("Test Task 2", "Description", (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"), "средний", "To Do", ["Мария"])
        task_id = crud.get_tasks()[-1][0]
        crud.update_task_status(task_id, "In Progress")
        updated_tasks = crud.get_tasks()
        self.assertEqual(next(t[5] for t in updated_tasks if t[0] == task_id), "In Progress")

    def test_delete_task(self):
        crud.create_task("Test Task 3", "Description", (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"), "высокий", "To Do", ["Петр"])
        task_id = crud.get_tasks()[-1][0]
        crud.delete_task(task_id)
        tasks = crud.get_tasks()
        self.assertEqual(len([t for t in tasks if t[0] == task_id]), 0)

if __name__ == "__main__":
    unittest.main()