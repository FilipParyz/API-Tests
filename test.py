from main import count_letters

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