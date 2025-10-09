import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any

class GeometryDatabase:
    def __init__(self, db_path: str = "geometry_calculations.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shape_type TEXT NOT NULL,
                volume REAL NOT NULL,
                surface_area REAL NOT NULL,
                mass REAL NOT NULL,
                material TEXT NOT NULL,
                parameters TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                density REAL NOT NULL
            )
        ''')
        
        # Добавляем базовые материалы если их нет
        base_materials = [
            ('Сталь', 7850.0),
            ('Алюминий', 2700.0),
            ('Медь', 8960.0)
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO materials (name, density) VALUES (?, ?)
        ''', base_materials)
        
        conn.commit()
        conn.close()
    
    def save_calculation(self, shape_data: Dict[str, Any], parameters: Dict[str, float]):
        """Сохранение расчета в базу данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO calculations 
            (shape_type, volume, surface_area, mass, material, parameters)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            shape_data['type'],
            shape_data['volume'],
            shape_data['surface_area'],
            shape_data['mass'],
            shape_data['material'],
            str(parameters)
        ))
        
        conn.commit()
        conn.close()
    
    def get_all_calculations(self) -> List[Dict[str, Any]]:
        """Получение всех расчетов из базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM calculations ORDER BY created_at DESC
        ''')
        
        calculations = []
        for row in cursor.fetchall():
            calculations.append({
                'id': row[0],
                'shape_type': row[1],
                'volume': row[2],
                'surface_area': row[3],
                'mass': row[4],
                'material': row[5],
                'parameters': row[6],
                'created_at': row[7]
            })
        
        conn.close()
        return calculations
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получение статистики по расчетам"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM calculations')
        total_calculations = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT shape_type) FROM calculations')
        unique_shapes = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT material) FROM calculations')
        unique_materials = cursor.fetchone()[0]
        
        cursor.execute('SELECT MAX(created_at) FROM calculations')
        last_calculation = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_calculations': total_calculations,
            'unique_shapes': unique_shapes,
            'unique_materials': unique_materials,
            'last_calculation': last_calculation
        }