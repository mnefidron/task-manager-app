# tests/test_settings.py

import unittest
import json
import os
import interface
from pathlib import Path
import customtkinter as ctk

class TestSettings(unittest.TestCase):
    def setUp(self):
        """Создаем временную настройку темы"""
        self.settings_path = Path("settings.json")
        self.test_settings = {"theme": "Dark"}
        
        # Сохраняем временные настройки
        with open(self.settings_path, "w") as f:
            json.dump(self.test_settings, f)

    def test_theme_change(self):
        """Проверка смены темы и сохранения в файл"""
        app = interface.TaskManager()
        app.save_settings("dark")
        
        with open("settings.json", "r") as f:
            settings = json.load(f)
            self.assertEqual(settings["theme"], "dark")

    def test_theme_persists(self):
        """Проверка загрузки сохранённой темы при перезапуске"""
        # Создаём экземпляр TaskManager
        app = interface.TaskManager()
        app.load_settings()  # Загружаем настройки из файла
        
        # Проверяем, что тема загружена из settings.json
        self.assertEqual(ctk.get_appearance_mode(), "Dark")
        
        # Очистка: удаляем временный файл
        if self.settings_path.exists():
            self.settings_path.unlink()