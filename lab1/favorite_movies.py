#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть строка с перечислением фильмов
def get_movies():
    my_favorite_movies = 'Терминатор, Пятый элемент, Аватар, Чужие, Назад в будущее'

    # Выведите на консоль с помощью индексации строки, последовательно:
    #   первый фильм
    #   последний
    #   второй
    #   второй с конца

    # Запятая не должна выводиться.  Переопределять my_favorite_movies нельзя
    # Использовать .split() или .find()или другие методы строки нельзя - пользуйтесь только срезами,
    # как указано в задании!
    list = []
    first_movie = my_favorite_movies[:10]
    list.append(first_movie)

    last_movie = my_favorite_movies[-15:]
    list.append(last_movie)

    second_movie = my_favorite_movies[12:25]
    list.append(second_movie)

    second_from_end = my_favorite_movies[35:40]
    list.append(second_from_end)
    return list