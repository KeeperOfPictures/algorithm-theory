from PySide6.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                              QPushButton, QTextEdit, QLineEdit, QLabel, 
                              QHBoxLayout, QProgressBar)
from PySide6.QtCore import QThread, Signal
import time
from lib.tasks import circle_areas_generator, email_generator, filter_string
from lib.tasks_parallel import parallel_circle_areas, parallel_email_generator, parallel_filter_string
import random

class CircleTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        title = QLabel("Генератор площадей кругов")
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(title)
        
        btn = QPushButton("Сгенерировать все площади кругов")
        btn.clicked.connect(self.generate)
        layout.addWidget(btn)
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Результаты появятся здесь...")
        layout.addWidget(self.output)
        
        self.setLayout(layout)

    def generate(self):
        try:
            self.output.clear()
            gen = circle_areas_generator()
            result = ""
            for radius in range(10, 101):
                area = next(gen)
                result += f"R = {radius}, S = {area:.2f}\n"
            self.output.setText(result)
        except Exception as e:
            self.output.setText(f"Ошибка: {e}")


class EmailTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        title = QLabel("Генератор email-адресов")
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(title)
        
        btn = QPushButton("Сгенерировать 10 email")
        btn.clicked.connect(self.generate)
        layout.addWidget(btn)
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Сгенерированные email-адреса появятся здесь...")
        layout.addWidget(self.output)
        
        self.setLayout(layout)

    def generate(self):
        self.output.clear()
        gen = email_generator()
        result = ""
        for _ in range(10):
            email = next(gen)
            result += f"{email}\n"
        self.output.setText(result)


class FilterTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        title = QLabel("Фильтр двузначных чисел")
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(title)
        
        
        layout.addWidget(QLabel("Введите числа через пробел:"))
        self.input = QLineEdit()
        self.input.setPlaceholderText("Например: 10 25 100 5 99 123 45")
        layout.addWidget(self.input)
        
        btn = QPushButton("Отфильтровать")
        btn.clicked.connect(self.filter)
        layout.addWidget(btn)
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Отфильтрованные числа появятся здесь...")
        layout.addWidget(self.output)
        
        self.setLayout(layout)

    def filter(self):
        try:
            self.output.clear()
            result = filter_string(self.input.text())
            self.output.setText(f"Результат: {result}")
        except Exception as e:
            self.output.setText(f"Ошибка: {e}")


class PerformanceWorker(QThread):
    finished = Signal(str)
    progress = Signal(int)
    
    def __init__(self):
        super().__init__()
    
    def run(self):
        try:
            results = []
            
            self.progress.emit(25)
            start = time.perf_counter()
            list(circle_areas_generator())
            exec_time_base = time.perf_counter() - start
            exec_time_parallel = parallel_circle_areas()
            speedup1 = exec_time_base / exec_time_parallel if exec_time_parallel > 0 else 0
            results.append(f"1. Площади кругов:\n   Обычный: {exec_time_base:.6f}с\n   Параллельный: {exec_time_parallel:.6f}с\n   Ускорение: {speedup1:.2f}x")
            
            self.progress.emit(50)
            gen = email_generator()
            start = time.perf_counter()
            [next(gen) for _ in range(1000)]
            exec_time_base = time.perf_counter() - start
            exec_time_parallel = parallel_email_generator(1000)
            speedup2 = exec_time_base / exec_time_parallel if exec_time_parallel > 0 else 0
            results.append(f"2. Email генератор (1000 адресов):\n   Обычный: {exec_time_base:.6f}с\n   Параллельный: {exec_time_parallel:.6f}с\n   Ускорение: {speedup2:.2f}x")
            
            self.progress.emit(75)
            data = ' '.join(str(random.randint(-500, 500)) for _ in range(100000))
            start = time.perf_counter()
            filter_string(data)
            exec_time_base = time.perf_counter() - start
            exec_time_parallel = parallel_filter_string(data)
            speedup3 = exec_time_base / exec_time_parallel if exec_time_parallel > 0 else 0
            results.append(f"3. Фильтр чисел (100000 чисел):\n   Обычный: {exec_time_base:.6f}с\n   Параллельный: {exec_time_parallel:.6f}с\n   Ускорение: {speedup3:.2f}x")
            
            self.progress.emit(100)
            self.finished.emit("\n\n".join(results))
            
        except Exception as e:
            self.finished.emit(f"Ошибка при тестировании: {e}")


class PerformanceTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        title = QLabel("Сравнение производительности")
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(title)
        
        
        self.btn_run = QPushButton("Запустить тесты производительности")
        self.btn_run.clicked.connect(self.run_performance_test)
        layout.addWidget(self.btn_run)
        
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("")
        layout.addWidget(self.output)
        
        self.setLayout(layout)
        
        self.worker = None

    def run_performance_test(self):
        self.btn_run.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.output.clear()
        
        self.worker = PerformanceWorker()
        self.worker.finished.connect(self.on_test_finished)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.start()

    def on_test_finished(self, results):
        self.btn_run.setEnabled(True)
        self.progress.setVisible(False)
        self.output.setText(results)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лаба 3")
        self.setGeometry(100, 100, 700, 500)
        
        tabs = QTabWidget()
        tabs.addTab(CircleTab(), "Площади кругов")
        tabs.addTab(EmailTab(), "Генератор email")
        tabs.addTab(FilterTab(), "Фильтр чисел")
        tabs.addTab(PerformanceTab(), "Сравнение производительности")
        
        self.setCentralWidget(tabs)