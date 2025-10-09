import math
from .base import Shape3D

class Parallelepiped(Shape3D):
    #Класс параллелепипеда
    
    def __init__(self, length: float, width: float, height: float, material=None):
        super().__init__(material)
        self._length = length
        self._width = width
        self._height = height
    
    @property
    def length(self) -> float:
        return self._length
    
    @property
    def width(self) -> float:
        return self._width
    
    @property
    def height(self) -> float:
        return self._height
    
    def _calculate_volume(self) -> float:
        return self._length * self._width * self._height
    
    def _calculate_surface_area(self) -> float:
        return 2 * (self._length * self._width + 
                   self._length * self._height + 
                   self._width * self._height)
    
    def __eq__(self, other):
        if not isinstance(other, Parallelepiped):
            return False
        return (self._length == other._length and 
                self._width == other._width and 
                self._height == other._height)
    
    def __add__(self, other):
        #Сложение объёмов двух параллелепипедов
        if not isinstance(other, Parallelepiped):
            raise TypeError("Можно сложить только два параллелепипеда")
        return self.volume + other.volume

class Tetrahedron(Shape3D):
    #Класс правильного тетраэдра
    
    def __init__(self, edge: float, material=None):
        super().__init__(material)
        self._edge = edge
    
    @property
    def edge(self) -> float:
        return self._edge
    
    def _calculate_volume(self) -> float:
        return (self._edge ** 3) * math.sqrt(2) / 12
    
    def _calculate_surface_area(self) -> float:
        return math.sqrt(3) * (self._edge ** 2)
    
    def __eq__(self, other):
        if not isinstance(other, Tetrahedron):
            return False
        return self._edge == other._edge
    
    def __lt__(self, other):
        #Сравнение по объёму
        if not isinstance(other, Tetrahedron):
            raise TypeError("Можно сложить только два тетраэдра")
        return self.volume < other.volume

class Sphere(Shape3D):
    #Класс сферы
    
    def __init__(self, radius: float, material=None):
        super().__init__(material)
        self._radius = radius
    
    @property
    def radius(self) -> float:
        return self._radius
    
    def _calculate_volume(self) -> float:
        return (4/3) * math.pi * (self._radius ** 3)
    
    def _calculate_surface_area(self) -> float:
        return 4 * math.pi * (self._radius ** 2)
    
    def __eq__(self, other):
        if not isinstance(other, Sphere):
            return False
        return self._radius == other._radius
    
    def __mul__(self, factor):
        #Умножение радиуса на коэффициент
        if not isinstance(factor, (int, float)):
            raise TypeError("Коэф. должен быть числом.")
        return Sphere(self._radius * factor, self.material)