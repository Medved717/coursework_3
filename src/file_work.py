import os
import json

class FileWork:

    @staticmethod
    def get_response_data(name_file):
        """Получение сохраненных данных из hh.ru и вывод списка вакансий."""

        file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_api_hh = os.path.join(file_path, "data", f"{name_file}")
        with open(file_api_hh, "r", encoding="utf-8") as file:
            data = json.load(file)
            list_vacancies = data["items"]
            return list_vacancies
