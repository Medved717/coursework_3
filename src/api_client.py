import json

import requests
import os

from src.db_manager import result


class ApiClient:
    """Класс написан как теоритический и в курсовой используется
    только как пример ввиду невозможности подключиться к API hh.ru."""

    def __init__(self) -> None:
        """Задаются автоматические параметры при запросе API
        в адрес hh.ru для автоматизации процесса возвращения данных."""

        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "MySuperApp/1.0 (my-super-examplel@mail.ru)"}
        self.params = {"text": "Python", "area": 113, "per_page": 20, "page": 0}

    def get_response_save(self, url: str, headers: dict, params: dict) -> dict|None:
        """Получение ответа API запроса на hh.ru и сохранение сведений в формате json."""

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            for vacancy in data["items"]:
                print(f"{vacancy['name']} — {vacancy['employer']['name']}")
        else:
            print(f"Ошибка: {response.status_code}")
            data = None
        return data