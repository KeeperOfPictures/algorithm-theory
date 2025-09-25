import pytest
from circle import calculate_circle_area, is_in_circle

def test_calculate_circle_area():
    assert calculate_circle_area(1) == pytest.approx(3.1416, rel=1e-4)
    assert calculate_circle_area(2) == pytest.approx(12.5664, rel=1e-4)

def test_is_in_circle():
    assert is_in_circle(5, 0, 0) is True
    assert is_in_circle(5, 3, 4) is True
    assert is_in_circle(5, 6, 0) is False