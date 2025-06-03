# run_all_tests.py

import unittest
import coverage

# Инициализация покрытия кода
cov = coverage.Coverage()
cov.start()

# Автоматически находим и загружаем все тесты из папки tests
loader = unittest.TestLoader()
suite = loader.discover(start_dir="tests", pattern="test_*.py")

# Запускаем тесты
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# Останавливаем покрытие кода и выводим отчет
cov.stop()
cov.save()

print("\n📊 Отчет о покрытии кода:")
cov.report()

print("\n📁 Генерация HTML-отчета...")
cov.html_report(directory='htmlcov')

print("✅ HTML-отчет сохранен в папке htmlcov/index.html")