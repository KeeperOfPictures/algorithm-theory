from garden import garden

def test_garden_flowers():
    all_flowers, common_flowers, garden_only, meadow_only = garden()

    assert all_flowers == {'ромашка', 'роза', 'одуванчик', 'гладиолус', 'подсолнух', 'клевер', 'мак'}
    assert common_flowers == {'ромашка', 'одуванчик'}
    assert garden_only == {'роза', 'гладиолус', 'подсолнух'}
    assert meadow_only == {'клевер', 'мак'}