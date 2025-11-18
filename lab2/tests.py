import pytest
import math
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from geometry_package import Parallelepiped, Tetrahedron, Sphere, Steel, Aluminum, Copper


class TestShapeBasicProperties:
    """Тесты базовых свойств фигур"""
    
    def test_parallelepiped_creation(self):
        """Тест создания параллелепипеда"""
        p = Parallelepiped(2.0, 3.0, 4.0)
        assert p.length == 2.0
        assert p.width == 3.0
        assert p.height == 4.0
    
    def test_tetrahedron_creation(self):
        """Тест создания тетраэдра"""
        t = Tetrahedron(5.0)
        assert t.edge == 5.0
    
    def test_sphere_creation(self):
        """Тест создания сферы"""
        s = Sphere(3.5)
        assert s.radius == 3.5


class TestVolumeCalculations:
    """Тесты расчета объемов"""
    
    def test_parallelepiped_volume(self):
        """Тест объема параллелепипеда"""
        p = Parallelepiped(2, 3, 4)
        expected_volume = 2 * 3 * 4
        assert p.volume == expected_volume
    
    def test_tetrahedron_volume(self):
        """Тест объема тетраэдра"""
        t = Tetrahedron(2)
        expected_volume = (2**3) * math.sqrt(2) / 12
        assert abs(t.volume - expected_volume) < 1e-10
    
    def test_sphere_volume(self):
        """Тест объема сферы"""
        s = Sphere(3)
        expected_volume = (4/3) * math.pi * (3**3)
        assert abs(s.volume - expected_volume) < 1e-10
    
    def test_volume_caching(self):
        """Тест кэширования объема"""
        p = Parallelepiped(2, 3, 4)
        initial_volume = p.volume
        assert p.volume == initial_volume


class TestSurfaceAreaCalculations:
    """Тесты расчета площадей поверхности"""
    
    def test_parallelepiped_surface_area(self):
        """Тест площади поверхности параллелепипеда"""
        p = Parallelepiped(2, 3, 4)
        expected_area = 2 * (2*3 + 2*4 + 3*4)
        assert p.surface_area == expected_area
    
    def test_tetrahedron_surface_area(self):
        """Тест площади поверхности тетраэдра"""
        t = Tetrahedron(2)
        expected_area = math.sqrt(3) * (2**2)
        assert abs(t.surface_area - expected_area) < 1e-10
    
    def test_sphere_surface_area(self):
        """Тест площади поверхности сферы"""
        s = Sphere(3)
        expected_area = 4 * math.pi * (3**2)
        assert abs(s.surface_area - expected_area) < 1e-10
    
    def test_surface_area_caching(self):
        """Тест кэширования площади поверхности"""
        s = Sphere(5)
        initial_area = s.surface_area
        # Второй вызов должен вернуть то же значение без пересчета
        assert s.surface_area == initial_area


class TestMaterialIntegration:
    """Тесты интеграции с материалами"""
    
    def test_shape_with_steel_material(self):
        """Тест фигуры со стальным материалом"""
        p = Parallelepiped(1, 1, 1, Steel())
        assert p.material.name == "Сталь"
        assert p.material.density == 7850.0
    
    def test_shape_with_aluminum_material(self):
        """Тест фигуры с алюминиевым материалом"""
        t = Tetrahedron(2, Aluminum())
        assert t.material.name == "Алюминий"
        assert t.material.density == 2700.0
    
    def test_shape_with_copper_material(self):
        """Тест фигуры с медным материалом"""
        s = Sphere(1, Copper())
        assert s.material.name == "Медь"
        assert s.material.density == 8960.0
    
    def test_material_assignment_after_creation(self):
        """Тест присвоения материала после создания фигуры"""
        p = Parallelepiped(1, 1, 1)
        p.material = Steel()
        assert p.material.name == "Сталь"
    
    def test_mass_calculation_with_material(self):
        """Тест расчета массы с материалом"""
        # Параллелепипед 1x1x1 = объем 1 м³
        p = Parallelepiped(1, 1, 1, Steel())
        expected_mass = 1 * 7850  # volume * density
        assert abs(p.mass - expected_mass) < 1e-10
        
        # Тетраэдр с ребром 2
        t = Tetrahedron(2, Aluminum())
        tetra_volume = (2**3) * math.sqrt(2) / 12
        expected_mass = tetra_volume * 2700
        assert abs(t.mass - expected_mass) < 1e-10
        
        # Сфера радиусом 1
        s = Sphere(1, Copper())
        sphere_volume = (4/3) * math.pi * (1**3)
        expected_mass = sphere_volume * 8960
        assert abs(s.mass - expected_mass) < 1e-10


class TestToDictMethod:
    """Тесты метода to_dict()"""
    
    def test_parallelepiped_to_dict(self):
        """Тест to_dict() для параллелепипеда"""
        p = Parallelepiped(2, 3, 4, Steel())
        result = p.to_dict()
        
        expected_keys = ['type', 'volume', 'surface_area', 'mass', 'material']
        for key in expected_keys:
            assert key in result
        
        assert result['type'] == 'Parallelepiped'
        assert result['volume'] == 24.0
        assert result['surface_area'] == 52.0
        assert result['material'] == 'Сталь'
        assert result['mass'] == 24.0 * 7850
    
    def test_tetrahedron_to_dict(self):
        """Тест to_dict() для тетраэдра"""
        t = Tetrahedron(3, Aluminum())
        result = t.to_dict()
        
        assert result['type'] == 'Tetrahedron'
        assert result['material'] == 'Алюминий'
        assert isinstance(result['volume'], float)
        assert isinstance(result['surface_area'], float)
        assert isinstance(result['mass'], float)
    
    def test_sphere_to_dict(self):
        """Тест to_dict() для сферы"""
        s = Sphere(2.5, Copper())
        result = s.to_dict()
        
        assert result['type'] == 'Sphere'
        assert result['material'] == 'Медь'
        assert result['volume'] > 0
        assert result['surface_area'] > 0
        assert result['mass'] > 0
    
    def test_to_dict_without_material(self):
        """Тест to_dict() без материала"""
        p = Parallelepiped(1, 2, 3)
        result = p.to_dict()
        
        assert result['type'] == 'Parallelepiped'
        assert result['material'] is None
        assert result['mass'] is None
        assert result['volume'] == 6.0
        assert result['surface_area'] == 22.0


class TestStringRepresentations:
    """Тесты строковых представлений"""
    
    
    def test_parallelepiped_repr(self):
        """Тест __repr__ для параллелепипеда"""
        p = Parallelepiped(2, 3, 4)
        repr_repr = repr(p)
        assert 'Parallelepiped' in repr_repr
    
    def test_material_str(self):
        """Тест __str__ для материалов"""
        steel = Steel()
        str_repr = str(steel)
        assert 'Сталь' in str_repr
        assert '7850' in str_repr
    
    def test_material_repr(self):
        """Тест __repr__ для материалов"""
        aluminum = Aluminum()
        repr_repr = repr(aluminum)
        assert 'Алюминий' in repr_repr
        assert '2700' in repr_repr


class TestComparisonOperations:
    """Тесты операций сравнения"""
    
    def test_parallelepiped_equality(self):
        """Тест равенства параллелепипедов"""
        p1 = Parallelepiped(2, 3, 4)
        p2 = Parallelepiped(2, 3, 4)
        p3 = Parallelepiped(1, 2, 3)
        
        assert p1 == p2
        assert p1 != p3
        assert not (p1 == p3)
    
    def test_tetrahedron_equality(self):
        """Тест равенства тетраэдров"""
        t1 = Tetrahedron(5)
        t2 = Tetrahedron(5)
        t3 = Tetrahedron(3)
        
        assert t1 == t2
        assert t1 != t3
    
    def test_sphere_equality(self):
        """Тест равенства сфер"""
        s1 = Sphere(4)
        s2 = Sphere(4)
        s3 = Sphere(2)
        
        assert s1 == s2
        assert s1 != s3
    
    def test_different_types_not_equal(self):
        """Тест что разные типы фигур не равны"""
        p = Parallelepiped(2, 2, 2)
        t = Tetrahedron(2)
        s = Sphere(1)
        
        assert p != t
        assert p != s
        assert t != s


class TestEdgeCases:
    """Тесты граничных случаев и обработки ошибок"""
    
    
    def test_very_small_dimensions(self):
        """Тест очень маленьких размеров"""
        p = Parallelepiped(0.001, 0.001, 0.001)
        assert p.volume > 0
        assert p.surface_area > 0
        
        t = Tetrahedron(0.001)
        assert t.volume > 0
        assert t.surface_area > 0
        
        s = Sphere(0.001)
        assert s.volume > 0
        assert s.surface_area > 0
    
    def test_very_large_dimensions(self):
        """Тест очень больших размеров"""
        p = Parallelepiped(1000, 1000, 1000)
        assert p.volume == 1e9
        assert p.surface_area == 6e6
        
        s = Sphere(1000)
        expected_volume = (4/3) * math.pi * (1000**3)
        assert abs(s.volume - expected_volume) < 1e-5


class TestMaterialProperties:
    """Тесты свойств материалов"""
    
    def test_steel_properties(self):
        """Тест свойств стали"""
        steel = Steel()
        assert steel.name == "Сталь"
        assert steel.density == 7850.0
    
    def test_aluminum_properties(self):
        """Тест свойств алюминия"""
        aluminum = Aluminum()
        assert aluminum.name == "Алюминий"
        assert aluminum.density == 2700.0
    
    def test_copper_properties(self):
        """Тест свойств меди"""
        copper = Copper()
        assert copper.name == "Медь"
        assert copper.density == 8960.0
    
    def test_material_immutability(self):
        """Тест что свойства материалов неизменяемы"""
        steel = Steel()
        
        # Попытка изменить свойство должна вызвать ошибку
        with pytest.raises(AttributeError):
            steel.name = "New Name"
        
        with pytest.raises(AttributeError):
            steel.density = 1000


if __name__ == "__main__":
    # Запуск тестов напрямую
    pytest.main([__file__, "-v"])