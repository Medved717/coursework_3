from src.db_data import DbSave
from src.db_manager import DbManager


if __name__ == '__main__':

    print('''Здравствуй, пользователь! Добро пожаловать в программу по анализу размещенных вакансий на сайте hh.ru.''')

    print('Какую базу данных Вы хотите использовать?')
    input_name_bd = input('Пользователь: введите наименование базы данных: ').lower()
    input_table_company = None
    db_name_exists = DbSave.exists_db(input_name_bd)
    if db_name_exists == 0:
        while True:
            print(f'Базы данных {input_name_bd} не существует. Желаете инициализировать новую базу данных?')
            input_answer = input('Пользователь: да/нет: ').lower()
            if input_answer == 'да':
                DbSave.create_data_base(input_name_bd)
                print(f'База данных {input_name_bd} успешно создана.')
                answer = 'да'
                break
            elif input_answer == 'нет':
                print('Попробуйте заново внести наименование используемой базы данных и повторите операцию.')
                break

        print('Создать новые таблицы по учету компаний и вакансий?')
        while True:
            input_world = input('Пользователь: (Да или нет)? ').lower()
            if input_world == 'да':

                DbSave.create_table_vacancy(input_name_bd)
                print('Таблица вакансий - company успешно создана.')
                DbSave.create_table_company(input_name_bd)
                print(f'Таблица вакансий - vacancy успешно создана.')
                break
            elif input_world == 'нет':
                print('Таблицы не созданы. Данные отсутствуют.')

    elif db_name_exists == 1:
        print(f'База данных {input_name_bd} успешно выбрана.')
        input_table_company = 'company'
        input_table_vacancy = 'vacancy'

    print('''Выберите одну из представленных возможностей ознакомления со сведениями вакансий:
    1. Представить компании и количество вакансий в каждой компании;
    2. Представить список всех вакансий с указанием названия компании, 
    названия вакансии, зарплаты и ссылки на вакансию.
    3. Представить среднюю зарплату по вакансиям;
    4. Представить список всех вакансий, у которых зарплата выше средней по всем вакансиям;
    5. Осуществить поиск вакансий по введенному слову.''')

    input_word = str(input('Пользователь: ')).lower()
    while True:
        if input_word == '1':
            result = DbManager.get_companies_and_vacancies_count(input_name_bd)
            print(result)
            break

    while True:
        if input_word == '2':
            result = DbManager.get_all_vacancies(input_name_bd)
            print(result)
            break

    while True:
        if input_word == '3':
            result = DbManager.get_avg_salary(input_name_bd)
            print(result)
            break

    while True:
        if input_word == '4':
            result = DbManager.get_vacancies_with_higher_salary(input_name_bd)
            print(result)
            break

    while True:
        if input_word == '5':
            print('Введите искомое слово.')
            search_word = input('Пользователь: ').lower()
            result = DbManager.get_vacancies_with_keyword(input_name_bd, search_word)
            print(result)
            break


# # Пробники
# coursework_33
# vacancy
# company







