# tests/test_calendar.py

import unittest
from unittest.mock import patch
from datetime import date
from interface import AddEditTaskWindow
from customtkinter import CTk

class TestCalendar(unittest.TestCase):
    def test_deadline_selection(self):
        root = CTk()
        window = AddEditTaskWindow(root, mode="add")
        window.deadline_picker.set_date(date(2025, 1, 1))
        self.assertEqual(window.deadline_picker.get_date().strftime("%Y-%m-%d"), "2025-01-01")
        root.destroy()

if __name__ == "__main__":
    unittest.main()