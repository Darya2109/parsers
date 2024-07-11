import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://books.toscrape.com/'

# Timeout на запросы к сайту
r = requests.get(url, verify=False, timeout=10)

soup = BeautifulSoup(r.content, 'html.parser')

df = pd.DataFrame({
    'book_name':[],
    'price':[],
    'url':[],
})


def get_books(soup, data=df):
    divs = soup.find_all('li', attrs={'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

    # ограничение на количество вытянутых записей
    for div in divs:
        if len(df) >= 1000:
            return

        book = {}
        book['book_name'] = div.find('h3').find('a').get('title')
        book['price'] = div.find('p', class_='price_color').text
        book['url'] = 'https://books.toscrape.com/catalogue/' + div.find('h3').find('a').get('href')
        df.loc[len(df)] = book


url = 'https://books.toscrape.com/catalogue/page-'
i = 1
while True:
    print(f'Parsing page N:{i}')
    r = requests.get(url + str(i) + '.html', timeout=10)
    soup = BeautifulSoup(r.content, 'html.parser')

    get_books(soup, df)
    time.sleep(1)

    # ограничение на количество вытянутых записей
    if len(df) >= 1000:
        break
    i += 1

print('Parsing done!')
print(f'Total length DataFrame: {len(df)}')

df.to_csv('books.csv')