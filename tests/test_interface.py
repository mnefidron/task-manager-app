# tests/test_interface.py

import unittest
import interface
from customtkinter import CTk

class TestInterface(unittest.TestCase):
    def test_load_tasks(self):
        app = interface.TaskManager()
        app.load_tasks()
        self.assertIn("To Do", app.task_widgets)
        self.assertIn("In Progress", app.task_widgets)
        self.assertIn("Done", app.task_widgets)

if __name__ == "__main__":
    unittest.main()