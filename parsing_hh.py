import requests
import pandas as pd

# https://api.hh.ru/openapi/redoc#tag/Poisk-vakansij/Klastery-v-poiske-vakansij
url = 'https://api.hh.ru/vacancies'
# запрос для поиска вакансии
text = 'data scientist'

headers = {}

parametrs = {
    'search_field': 'name',
    'text': text,
    'area': '113',
    'per_page': '10',
    'page': 1,
}

r = requests.get(url, params=parametrs, headers=headers)
vacancies_info = r.json()

df = pd.DataFrame({
    'id':[],
    'name':[],
    'url':[],
    'published_at':[],
    'archived':[],
    'salary':[],
    'company':[],
    'area':[],
    'requirement':[],
    'responsibility': [],
    'working_time_modes':[],
    'experience':[],
    'employment':[]
})

for vac in vacancies_info['items']:
    vac_parser = {
        'id': vac['id'],
        'url': vac['alternate_url'],
        'published_at': vac['published_at'],
        'archived': vac['archived'],
        'name': vac['name'],
        'salary': vac['salary'],
        'company': vac['employer']['name'],
        'area': vac['area']['name'],
        'requirement': vac['snippet']['requirement'],
        'responsibility': vac['snippet']['responsibility'],
        'experience': vac['experience']['name'],
        'working_time_modes': vac['schedule']['name'],
        'employment': vac['employment']['name']
    }
    df.loc[len(df)] = vac_parser

# создание файла
df.to_csv('vacancies.csv', sep=',')

# дописование в существующий файл
#df.to_csv('vacancies.csv', sep=',', mode='a', header= False)