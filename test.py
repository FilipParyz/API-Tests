from main import count_letters
from main import fetch_data
from main import drop_tables
from main import create_database

def test_count_letters():
    assert count_letters('hello') == {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    assert count_letters('world') == {'w': 1, 'o': 1, 'r': 1, 'l': 1, 'd': 1}
    assert count_letters('Python is awesome') == {'p': 1, 'y': 1, 't': 1, 'h': 1, 'o': 2, 'n': 1, 'i': 1, 's': 2, 'a': 1, 'w': 1, 'e': 2, 'm': 1}

def test_fetch_data():
    assert fetch_data('https://jsonplaceholder.typicode.com/posts/') != None

def test_drop_tables():
    assert drop_tables() == []

def test_create_database():
    assert create_database() == [('comments',), ('posts',), ('users',)]

def test_calculate_simple_moving_average():
    assert calculate_simple_moving_average([1, 2, 3, 4, 5]) == 3.0
    assert calculate_simple_moving_average([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 5.5
    assert calculate_simple_moving_average([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]) == 6.0

def test_calculate_expontential_moving_average():
    assert calculate_expontential_moving_average([1, 2]) == [1.5, 1.75]