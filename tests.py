
import matplotlib.pyplot as plt
import requests
import json
import sqlite3

def fetch_data(link):
    response = requests.get(link)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def count_letters(string):
    letter_count = {}
    for letter in string:
        if letter.isalpha():
            if letter.lower() in letter_count:
                letter_count[letter.lower()] += 1
            else:
                letter_count[letter.lower()] = 1
    letter_count = dict(sorted(letter_count.items()))
    return letter_count

def generate_graph_of_occurances(letter_count):
    plt.bar(range(len(letter_count)), list(letter_count.values()), align='center')
    plt.xticks(range(len(letter_count)), list(letter_count.keys()))
    #Add title and axis names
    plt.title('Letter count in all body parts')
    plt.xlabel('Letter')
    plt.ylabel('Occurances')
    plt.savefig('letter_count.png')

def drop_tables():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''DROP TABLE IF EXISTS users''')
        c.execute('''DROP TABLE IF EXISTS posts''')
        c.execute('''DROP TABLE IF EXISTS comments''')

def create_database():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()

        # Create tables with Primary Keys
        c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name text, username text, email text, address_street text, address_suite text, address_city text, address_zipcode text, address_geo_lat real, address_geo_lng real, phone text, website text, company_name text, company_catchPhrase text, company_bs text)''')
        c.execute('''CREATE TABLE posts (id INTEGER PRIMARY KEY, userId INTEGER, title TEXT, body TEXT, FOREIGN KEY (userId) REFERENCES users(id))''')
        c.execute('''CREATE TABLE comments (id INTEGER PRIMARY KEY, postId INTEGER, name TEXT, email TEXT, body TEXT, FOREIGN KEY (postId) REFERENCES posts(id))''')

def fill_database():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()

        jsonValue = fetch_data('https://jsonplaceholder.typicode.com/users/')
        if jsonValue:
            for element in jsonValue:
                c.execute(f'''INSERT INTO users (name, username, email, address_street, address_suite, address_city, address_zipcode, address_geo_lat, address_geo_lng, phone, website, company_name, company_catchPhrase, company_bs)
                VALUES ("{element['name']}", "{element['username']}", "{element['email']}", "{element['address']['street']}", "{element['address']['suite']}", "{element['address']['city']}", "{element['address']['zipcode']}", "{element['address']['geo']['lat']}", "{element['address']['geo']['lng']}", "{element['phone']}", "{element['website']}", "{element['company']['name']}", "{element['company']['catchPhrase']}", "{element['company']['bs']}")''')

        jsonValue = fetch_data('https://jsonplaceholder.typicode.com/posts/')
        if jsonValue:
            for element in jsonValue:
                c.execute(f'''INSERT INTO posts (userId, title, body)
                VALUES ("{element['userId']}", "{element['title']}", "{element['body']}")''')

        jsonValue = fetch_data('https://jsonplaceholder.typicode.com/comments/')
        if jsonValue:
            for element in jsonValue:
                c.execute(f'''INSERT INTO comments (postId, name, email, body)
                VALUES ("{element['postId']}", "{element['name']}", "{element['email']}", "{element['body']}")''')


if __name__ == '__main__':
    jsonValue = fetch_data('https://jsonplaceholder.typicode.com/posts/')

    if jsonValue:
        output = ""
        for element in jsonValue:
            output+= element['body']
        letter_count = count_letters(output)

    generate_graph_of_occurances(letter_count)
    print("Graph generated and saved as letter_count.png")

    drop_tables()
    create_database()
    fill_database()
    print("Database created and filled with data")