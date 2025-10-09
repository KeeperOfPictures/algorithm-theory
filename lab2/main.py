from geometry_package import Parallelepiped, Tetrahedron, Sphere, Steel, Aluminum, Copper
from database import GeometryDatabase
import os
import json

class ConsoleGeometryCalculator:
    def __init__(self):
        self.shapes = {
            "1": {"name": "Параллелепипед", "class": Parallelepiped},
            "2": {"name": "Тетраэдр", "class": Tetrahedron},
            "3": {"name": "Шар", "class": Sphere}
        }
        
        self.materials = {
            "1": {"name": "Сталь", "obj": Steel()},
            "2": {"name": "Алюминий", "obj": Aluminum()},
            "3": {"name": "Медь", "obj": Copper()}
        }
        
        self.current_shape = None
        self.current_results = None
        self.current_parameters = None
        self.db = GeometryDatabase()
        
    def clear_screen(self):
        """Очистка экрана консоли"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """Отображение заголовка"""
        print("=" * 50)
        print("       КАЛЬКУЛЯТОР ГЕОМЕТРИЧЕСКИХ ФИГУР")
        print("=" * 50)
        print()
    
    def get_user_choice(self, options, prompt):
        """Получение выбора пользователя из меню"""
        while True:
            print(prompt)
            for key, value in options.items():
                print(f"  {key}. {value['name']}")
            
            choice = input(f"\nВведите ваш выбор (1-{len(options)}): ")
            
            if choice in options:
                return choice
            else:
                print("Неверный выбор! Пожалуйста, попробуйте снова.\n")
    
    def get_float_input(self, prompt):
        """Получение числового ввода от пользователя"""
        while True:
            try:
                value = float(input(prompt))
                if value <= 0:
                    print("Значение должно быть положительным! Пожалуйста, попробуйте снова.")
                    continue
                return value
            except ValueError:
                print("Пожалуйста, введите корректное число!")
    
    def select_shape(self):
        """Выбор фигуры"""
        self.clear_screen()
        self.display_header()
        print("📐 ВЫБОР ФИГУРЫ")
        print("-" * 30)
        
        choice = self.get_user_choice(self.shapes, "Доступные фигуры:")
        shape_info = self.shapes[choice]
        
        print(f"\nВыбрано: {shape_info['name']}")
        
        # Получение параметров фигуры
        parameters = {}
        if shape_info['name'] == "Параллелепипед":
            print("\nВведите размеры параллелепипеда:")
            length = self.get_float_input("Длина (м): ")
            width = self.get_float_input("Ширина (м): ")
            height = self.get_float_input("Высота (м): ")
            shape = shape_info['class'](length, width, height)
            parameters = {'length': length, 'width': width, 'height': height}
            
        elif shape_info['name'] == "Тетраэдр":
            print("\nВведите размеры тетраэдра:")
            edge = self.get_float_input("Длина ребра (м): ")
            shape = shape_info['class'](edge)
            parameters = {'edge': edge}
            
        elif shape_info['name'] == "Шар":
            print("\nВведите размеры шара:")
            radius = self.get_float_input("Радиус (м): ")
            shape = shape_info['class'](radius)
            parameters = {'radius': radius}
        
        return shape, parameters
    
    def select_material(self):
        """Выбор материала"""
        self.clear_screen()
        self.display_header()
        print("ВЫБОР МАТЕРИАЛА")
        print("-" * 30)
        
        choice = self.get_user_choice(self.materials, "Доступные материалы:")
        material_info = self.materials[choice]
        
        print(f"\nВыбрано: {material_info['name']}")
        return material_info['obj']
    
    def calculate_properties(self, shape, material):
        """Расчёт свойств фигуры"""
        shape.material = material
        return shape.to_dict()
    
    def display_results(self, results, shape):
        """Отображение результатов"""
        self.clear_screen()
        self.display_header()
        print("РЕЗУЛЬТАТЫ РАСЧЁТА")
        print("-" * 40)
        
        print(f"Тип фигуры:      {results['type']}")
        print(f"Объём:          {results['volume']:.6f} м³")
        print(f"Площадь поверхности: {results['surface_area']:.6f} м²")
        print(f"Масса:          {results['mass']:.2f} кг")
        print(f"Материал:       {results['material']}")
        
        # Дополнительная информация
        print("\n" + "=" * 40)
        print("Дополнительная информация:")
        print(f"  - Плотность {results['material']}: {shape.material.density} кг/м³")
        
        if results['type'] == 'Parallelepiped':
            print(f"  - Размеры: {shape.length} × {shape.width} × {shape.height} м")
        elif results['type'] == 'Tetrahedron':
            print(f"  - Длина ребра: {shape.edge} м")
        elif results['type'] == 'Sphere':
            print(f"  - Радиус: {shape.radius} м")
    
    def save_to_database(self, results, parameters):
        """Сохранение расчета в базу данных"""
        try:
            self.db.save_calculation(results, parameters)
            print("Расчет сохранен в базу данных")
        except Exception as e:
            print(f"Ошибка при сохранении в базу данных: {str(e)}")
    
    def view_calculation_history(self):
        """Просмотр истории расчетов"""
        self.clear_screen()
        self.display_header()
        print("ИСТОРИЯ РАСЧЕТОВ")
        print("-" * 30)
        
        calculations = self.db.get_all_calculations()
        
        if not calculations:
            print("История расчетов пуста.")
            input("\nНажмите Enter для продолжения...")
            return
        
        for calc in calculations:
            print(f"\nID: {calc['id']}")
            print(f"  Фигура: {calc['shape_type']}")
            print(f"  Материал: {calc['material']}")
            print(f"  Объём: {calc['volume']:.4f} м³")
            print(f"  Масса: {calc['mass']:.2f} кг")
            print(f"  Дата: {calc['created_at']}")
            print("-" * 30)
        
        print(f"\nВсего расчетов: {len(calculations)}")
        input("\nНажмите Enter для продолжения...")
    
    def show_statistics(self):
        """Показать статистику"""
        self.clear_screen()
        self.display_header()
        print("СТАТИСТИКА")
        print("-" * 20)
        
        stats = self.db.get_statistics()
        
        print(f"Всего расчетов: {stats['total_calculations']}")
        print(f"Уникальных фигур: {stats['unique_shapes']}")
        print(f"Уникальных материалов: {stats['unique_materials']}")
        print(f"Последний расчет: {stats['last_calculation'] or 'Нет данных'}")
        
        input("\nНажмите Enter для продолжения...")
    
    def save_report(self, results, shape):
        """Сохранение отчёта"""
        print("\nСОХРАНЕНИЕ ОТЧЁТА")
        print("-" * 25)
        print("1. Сохранить как TEXT файл")
        print("2. Сохранить как CSV файл")
        print("3. Сохранить в базу данных")
        print("4. Не сохранять")
        
        choice = input("\nВведите ваш выбор (1-4): ")
        
        if choice == "1":
            filename = "geometry_report.txt"
            self.save_as_text(results, shape, filename)
            print(f"Отчёт сохранён как {filename}")
            
        elif choice == "2":
            filename = "geometry_report.csv"
            self.save_as_csv(results, shape, filename)
            print(f"Отчёт сохранён как {filename}")
            
        elif choice == "3":
            self.save_to_database(results, self.current_parameters)
            
        elif choice == "4":
            print("Отчёт не сохранён")
        else:
            print("Неверный выбор!")
    
    def save_as_text(self, results, shape, filename):
        """Сохранение в текстовом формате"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("ОТЧЁТ ПО РАСЧЁТУ ГЕОМЕТРИЧЕСКИХ ФИГУР\n")
            f.write("=" * 45 + "\n\n")
            f.write(f"Тип фигуры:      {results['type']}\n")
            f.write(f"Объём:          {results['volume']:.6f} м³\n")
            f.write(f"Площадь поверхности: {results['surface_area']:.6f} м²\n")
            f.write(f"Масса:          {results['mass']:.2f} кг\n")
            f.write(f"Материал:       {results['material']}\n")
            f.write(f"Плотность материала: {shape.material.density} кг/м³\n")
            
            # Добавляем информацию о размерах
            if results['type'] == 'Parallelepiped':
                f.write(f"Размеры:        {shape.length} × {shape.width} × {shape.height} м\n")
            elif results['type'] == 'Tetrahedron':
                f.write(f"Длина ребра:    {shape.edge} м\n")
            elif results['type'] == 'Sphere':
                f.write(f"Радиус:         {shape.radius} м\n")
    
    def save_as_csv(self, results, shape, filename):
        """Сохранение в CSV формате"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Параметр,Значение,Единица измерения\n")
            f.write(f"Тип фигуры,{results['type']},\n")
            f.write(f"Объём,{results['volume']:.6f},м³\n")
            f.write(f"Площадь поверхности,{results['surface_area']:.6f},м²\n")
            f.write(f"Масса,{results['mass']:.2f},кг\n")
            f.write(f"Материал,{results['material']},\n")
            f.write(f"Плотность материала,{shape.material.density},кг/м³\n")
            
            # Добавляем информацию о размерах
            if results['type'] == 'Parallelepiped':
                f.write(f"Длина,{shape.length},м\n")
                f.write(f"Ширина,{shape.width},м\n")
                f.write(f"Высота,{shape.height},м\n")
            elif results['type'] == 'Tetrahedron':
                f.write(f"Длина ребра,{shape.edge},м\n")
            elif results['type'] == 'Sphere':
                f.write(f"Радиус,{shape.radius},м\n")
    
    def show_main_menu(self):
        """Главное меню"""
        while True:
            self.clear_screen()
            self.display_header()
            print("ГЛАВНОЕ МЕНЮ")
            print("-" * 20)
            print("1. Новый расчёт")
            print("2. Посмотреть последние результаты")
            print("3. История расчетов")
            print("4. Статистика")
            print("5. Сохранить последний отчёт")
            print("6. Выход")
            
            choice = input("\nВведите ваш выбор (1-6): ")
            
            if choice == "1":
                self.run_calculation()
            elif choice == "2":
                if self.current_shape and self.current_results:
                    self.display_results(self.current_results, self.current_shape)
                    input("\nНажмите Enter для продолжения...")
                else:
                    print("Нет доступных результатов расчёта!")
                    input("\nНажмите Enter для продолжения...")
            elif choice == "3":
                self.view_calculation_history()
            elif choice == "4":
                self.show_statistics()
            elif choice == "5":
                if self.current_shape and self.current_results:
                    self.save_report(self.current_results, self.current_shape)
                    input("\nНажмите Enter для продолжения...")
                else:
                    print("Нет результатов для сохранения!")
                    input("\nНажмите Enter для продолжения...")
            elif choice == "6":
                print("\nСпасибо за использование калькулятора геометрических фигур!")
                break
            else:
                print("Неверный выбор! Пожалуйста, попробуйте снова.")
                input("\nНажмите Enter для продолжения...")
    
    def run_calculation(self):
        """Запуск полного процесса расчёта"""
        try:
            # Выбор фигуры
            shape, parameters = self.select_shape()
            
            # Выбор материала
            material = self.select_material()
            
            # Расчёт
            results = self.calculate_properties(shape, material)
            
            # Сохранение для последующего использования
            self.current_shape = shape
            self.current_results = results
            self.current_parameters = parameters
            
            # Отображение результатов
            self.display_results(results, shape)
            
            # Предложение сохранить
            save_choice = input("\nХотите сохранить этот отчёт? (д/н): ").lower()
            if save_choice in ['д', 'да', 'y', 'yes']:
                self.save_report(results, shape)
            
            input("\nНажмите Enter для возврата в главное меню...")
            
        except Exception as e:
            print(f"\nПроизошла ошибка: {str(e)}")
            input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    calculator = ConsoleGeometryCalculator()
    calculator.show_main_menu()