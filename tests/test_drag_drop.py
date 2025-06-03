# tests/test_drag_drop.py

import unittest
from unittest.mock import MagicMock
import interface

class TestDragDrop(unittest.TestCase):
    def test_drag_to_done(self):
        app = interface.TaskManager()
        app.task_widgets = {"To Do": [], "In Progress": [], "Done": []}

        # Создаем фрейм задачи с методами winfo_x, winfo_y, winfo_width, winfo_height
        task_frame = MagicMock()
        task_frame.winfo_x.return_value = 100
        task_frame.winfo_y.return_value = 50
        task_frame.winfo_width.return_value = 300
        task_frame.winfo_height.return_value = 100

        app.task_widgets["To Do"].append(task_frame)

        event = MagicMock()
        event.x = 10
        event.y = 10
        event.x_root = 150
        event.y_root = 75

        event.widget = task_frame
        app.start_drag(event)
        app.do_drag(event)
        app.end_drag(event, task_frame, "To Do", 1)

        self.assertIn(task_frame, app.task_widgets["To Do"])

if __name__ == "__main__":
    unittest.main()