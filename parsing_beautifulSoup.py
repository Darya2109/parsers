import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://quotes.toscrape.com/'

r = requests.get(url, verify=False, timeout=10)

soup = BeautifulSoup(r.content, 'html.parser')

# Вывести полный код страницы
# print(soup.prettify())

# Вывести первый div
# print(divs[0].prettyfy())

# Вывести весь текст страницы
# print(soup.get_text())

# Получение всех тегов <p>
# soup.find_all('p')

# Получение первого тега <h1>
# soup.find('h1')

# Получение всех элементов с классом 'content'
# soup.find_all(class_='content')

# Получение элемента с идентификатором 'main'
# soup.find(id='main')

# Получение текста из первого тега <p>
# soup.find('p').text

# Получение всех элементов с тэгом div и атрибутами class с значением quote
# divs = soup.find_all('div', attrs={'class':'quote'})

# Вывести первый div из divs
# print(divs[0].prettify())

df = pd.DataFrame({
    'text':[],
    'author':[],
    'author_url':[],
    'tags':[],
})

def get_quotes(soup, data=df):
    divs = soup.find_all('div', attrs={'class': 'quote'})

    for div in divs:
        quote = {}
        quote['text'] = div.find('span', class_='text').text
        quote['author'] = div.find('small', class_='author').text
        quote['author_url'] = 'https://quotes.toscrape.com' + div.find_all('span')[1].find('a').get('href')
        tags = []
        for a_tag in div.find('div', class_='tags').find_all('a', class_='tag'):
            tags.append(a_tag.text)
        quote['tags'] = ', '.join(tags)
        df.loc[len(df)] = quote


url = 'https://quotes.toscrape.com/page/'
i = 1

while True:
    print(f'Parsing page N:{i}')
    r = requests.get(url + str(i), timeout=10)
    soup = BeautifulSoup(r.content, 'html.parser')

    get_quotes(soup, df)
    time.sleep(1)

    if 'No quotes found!' in soup.text:
        break
    i += 1

print('Parsing done!')
print(f'Total length DataFrame: {len(df)}')

df.tail(10)