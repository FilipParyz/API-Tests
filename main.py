
import matplotlib.pyplot as plt
import requests
import json
import sqlite3
from fake_useragent import UserAgent

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
        # Check if tables were dropped
        c.execute('''SELECT name FROM sqlite_master WHERE type='table' ORDER BY name''')
        return c.fetchall()

def create_database():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()

        # Create tables with Primary Keys
        c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name text, username text, email text, address_street text, address_suite text, address_city text, address_zipcode text, address_geo_lat real, address_geo_lng real, phone text, website text, company_name text, company_catchPhrase text, company_bs text)''')
        c.execute('''CREATE TABLE posts (id INTEGER PRIMARY KEY, userId INTEGER, title TEXT, body TEXT, FOREIGN KEY (userId) REFERENCES users(id))''')
        c.execute('''CREATE TABLE comments (id INTEGER PRIMARY KEY, postId INTEGER, name TEXT, email TEXT, body TEXT, FOREIGN KEY (postId) REFERENCES posts(id))''')

        # Check if tables were created
        c.execute('''SELECT name FROM sqlite_master WHERE type='table' ORDER BY name''')
        return c.fetchall()

def fill_database():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()

        jsonValue = fetch_data('https://jsonplaceholder.typicode.com/users/')
        if jsonValue:
            for element in jsonValue:
                c.execute(f'''INSERT INTO users (name,
                                                username,
                                                email,
                                                address_street,
                                                address_suite,
                                                address_city,
                                                address_zipcode,
                                                address_geo_lat,
                                                address_geo_lng,
                                                phone,
                                                website,
                                                company_name,
                                                company_catchPhrase,
                                                company_bs)
                                        VALUES ("{element["name"]}",
                                                "{element["username"]}",
                                                "{element["email"]}",
                                                "{element["address"]["street"]}",
                                                "{element["address"]["suite"]}",
                                                "{element["address"]["city"]}",
                                                "{element["address"]["zipcode"]}",
                                                "{element["address"]["geo"]["lat"]}",
                                                "{element["address"]["geo"]["lng"]}",
                                                "{element["phone"]}",
                                                "{element["website"]}",
                                                "{element["company"]["name"]}",
                                                "{element["company"]["catchPhrase"]}",
                                                "{element["company"]["bs"]}")''')

        jsonValue = fetch_data('https://jsonplaceholder.typicode.com/posts/')
        if jsonValue:
            for element in jsonValue:
                c.execute(f'''INSERT INTO posts (userId, title, body)
                VALUES ("{element["userId"]}", "{element["title"]}", "{element["body"]}")''')

        jsonValue = fetch_data('https://jsonplaceholder.typicode.com/comments/')
        if jsonValue:
            for element in jsonValue:
                c.execute(f'''INSERT INTO comments (postId, name, email, body)
                VALUES ("{element["postId"]}", "{element["name"]}", "{element["email"]}", "{element["body"]}")''')

def download_file(url, file_name):
    try:
        ua_str = UserAgent().chrome
        response = requests.get(url, allow_redirects=True, headers={"User-Agent": ua_str})
        with open(file_name, "wb") as file:
            file.write(response.content)
        return True
    except:
        return False

def prepare_data(data, period):
    data = data.split("\n")
    data = data[-period:-1]
    data = [float(row.split(",")[-2]) for row in data]
    return data

def calculate_simple_moving_average(data):
    period = len(data)
    sma = sum(data)/period
    return sma

def calculate_expontential_moving_average(data):
    period = len(data)
    ema = []
    ema.append(sum(data)/period)
    multiplier = 2/(period+1)
    for i in range(0, period):
        ema.append((data[i]-ema[i-1])*multiplier+ema[i-1])
    return ema

if __name__ == '__main__':
    jsonValue = fetch_data('https://jsonplaceholder.typicode.com/posts/')

    if jsonValue:
        output = ""
        for element in jsonValue:
            output+= element["body"]
        letter_count = count_letters(output)

    generate_graph_of_occurances(letter_count)
    print("Graph generated and saved as letter_count.png")

    drop_tables()
    create_database()
    fill_database()
    print("Database created and filled with data")

    success = download_file("https://query1.finance.yahoo.com/v7/finance/download/BTC-USD?period1=1669408234&period2=1700944234&interval=1d&events=history&includeAdjustedClose=true", "BTC-USD.csv")
    if success:
        with open("BTC-USD.csv", "r") as file:
            data = file.read()

        data = prepare_data(data, 8)
        sma_results = calculate_simple_moving_average(data)
        ema_results = calculate_expontential_moving_average(data)
        print("SMA: ", sma_results)
        print("EMA: ", ema_results)
    else:
        print("Failed to download file.")