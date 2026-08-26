import os
import json


class FileWork:
    """Класс предназначен для работы с файловой системой, в том числе обработкой, хранением и передачей информации."""

    @staticmethod
    def get_response_data(name_file: str) -> list:
        """Получение сохраненных данных из hh.ru и вывод списка вакансий."""

        file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_api_hh = os.path.join(file_path, "data", f"{name_file}")
        with open(file_api_hh, "r", encoding="utf-8") as file:
            data = json.load(file)
            list_vacancies = data["items"]
            return list_vacancies

    @staticmethod
    def save_response_data(data: json) -> None:
        """Сохранение полученных сведений api в формате json."""

        if data is not None:
            file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_api_hh = os.path.join(file_path, "data", "api_hh.json")
            with open(file_api_hh, "w", encoding="utf-8") as file:
                json.dump(data, file)
        else:
            print('Невозможно сохранить пустые данны api.')
        return None
