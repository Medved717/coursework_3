from src.api_client import APICLIENT


class DBMANAGER:

    def __init__(self, list_vacanccies=None):
        if list_vacanccies == None:
            list_vacanccies = APICLIENT.get_response_data('hh_vacancies.json')
        else:
            self.list_vacanccies=list_vacanccies


    def get_companies_and_vacancies_count(self):
        '''Получает список всех компаний и количество вакансий у каждой компании.'''

        # Получаем список всех компаний.
        dict_company = {}
        for vacancy in self.list_vacanccies:
            company_name = vacancy.get('employer', {}).get('name', {})
            if company_name not in dict_company:
                dict_company[company_name] = 1
            else:
                dict_company[company_name] += 1
        return dict_company



obj_1 = DBMANAGER(APICLIENT.get_response_data('hh_vacancies.json'))
result = obj_1.get_companies_and_vacancies_count()
print(result)