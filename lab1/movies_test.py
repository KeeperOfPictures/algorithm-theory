from favorite_movies import get_movies

def test_get_movies():
    slice1, slice2, slice3, slice4 = get_movies()
    
    assert slice1 == 'Терминатор'
    assert slice2 == 'Назад в будущее'
    assert slice3 == 'Пятый элемент'
    assert slice4 == 'Чужие'