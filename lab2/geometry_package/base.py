from abc import ABC, abstractmethod
from typing import Dict, Any
from .materials import Material

class Shape3D(ABC):
    #Абстрактный базовый класс для 3D фигур
    
    def __init__(self, material: Material = None):
        self._material = material
        self._volume = None
        self._surface_area = None
    
    @property
    def material(self) -> Material:
        return self._material
    
    @material.setter
    def material(self, value: Material):
        if not isinstance(value, Material):
            raise TypeError("Материал класса не найден.")
        self._material = value
    
    @property
    def volume(self) -> float:
        if self._volume is None:
            self._volume = self._calculate_volume()
        return self._volume
    
    @property
    def surface_area(self) -> float:
        if self._surface_area is None:
            self._surface_area = self._calculate_surface_area()
        return self._surface_area
    
    @property
    def mass(self) -> float:
        if self.material is None:
            raise ValueError("Материал не задан")
        return self.volume * self.material.density
    
    @abstractmethod
    def _calculate_volume(self) -> float:
        pass
    
    @abstractmethod
    def _calculate_surface_area(self) -> float:
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(объём={self.volume:.2f}, площадь={self.surface_area:.2f})"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
    
    def to_dict(self) -> Dict[str, Any]:
        #Возвращает словарь с параметрами фигуры
        return {
            'type': self.__class__.__name__,
            'volume': round(self.volume, 4),
            'surface_area': round(self.surface_area, 4),
            'mass': round(self.mass, 4) if self.material else None,
            'material': self.material.name if self.material else None
        }