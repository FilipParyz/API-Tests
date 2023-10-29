
import matplotlib.pyplot as plt
import requests
import json

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

if __name__ == '__main__':
    jsonValue = fetch_data('https://jsonplaceholder.typicode.com/posts/')

    if jsonValue:
        output = ""
        for element in jsonValue:
            output+= element['body']
        letter_count = count_letters(output)
        print('Letter count in all body parts: \n' + json.dumps(letter_count, indent=4, sort_keys=True))

    generate_graph_of_occurances(letter_count)