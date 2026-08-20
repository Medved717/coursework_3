import json

import requests
import os

class ApiClient:

    def __init__(self, url, headers, params):
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {'User-Agent': 'MySuperApp/1.0 (my-super-examplel@mail.ru)'}
        self.params = {
        "text": "Python",
        "area": 113,
        "per_page": 20,
        "page": 0
    }


    def get_response_save(self, url, headers, params):
        '''Получаине ответа API запроса на hh.ru и сохранение сведений в формате json.'''

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            for vacancy in data['items']:
                print(f"{vacancy['name']} — {vacancy['employer']['name']}")

            file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_api_hh = os.path.join(file_path, 'data', 'api_hh.json')
            with open(file_api_hh, 'w', encoding='utf-8') as file:
                json.dump(data, file)
        else:
            print(f"Ошибка: {response.status_code}")

    @classmethod
    def get_response_data(cls, name_file):
        '''Получение сохраненных данных из hh.ru и вывод списка вакансий.'''

        file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_api_hh = os.path.join(file_path, 'data', f"{name_file}")
        with open(file_api_hh, 'r', encoding='utf-8') as file:
            data = json.load(file)
            list_vacancies = data['items']
            return list_vacancies