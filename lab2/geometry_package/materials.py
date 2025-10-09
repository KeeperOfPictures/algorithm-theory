class Material:
    def __init__(self, name: str, density: float):
        self._name = name
        self._density = density
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def density(self) -> float:
        return self._density
    
    def __str__(self) -> str:
        return f"{self._name} (плотность: {self._density} кг/м³)"
    
    def __repr__(self) -> str:
        return f"Material('{self._name}', {self._density})"

class Steel(Material):
    def __init__(self):
        super().__init__("Сталь", 7850.0)

class Aluminum(Material):
    def __init__(self):
        super().__init__("Алюминий", 2700.0)

class Copper(Material):
    def __init__(self):
        super().__init__("Медь", 8960.0)