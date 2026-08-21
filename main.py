from src.db_data import DbSave


if __name__ == '__main__':

    print('''Здравствуй, пользователь! Добро пожаловать в программу по анализу размещенных вакансий на сайте hh.ru.''')

    print('Какую базу данных Вы хотите использовать?')
    input_name_bd = input('Пользователь: введите наименование базы данных: ').lower()
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

        print('Введите наименование таблицы вакансий')
        input_table_vacancy = input('Пользователь: ').lower()
        DbSave.create_table_vacancy(input_name_bd, input_table_vacancy)
        print(f'Таблица вакансий - {input_table_vacancy} успешно создана.')
        print('Введите наименование таблицы компаний')
        input_table_company = input('Пользователь: ').lower()
        DbSave.create_table_company(input_name_bd, input_table_vacancy, input_table_company)
        print(f'Таблица вакансий - {input_table_company} успешно создана.')

    elif db_name_exists == 1:
        print(f'База данных {input_name_bd} успешно выбрана.')


# # Пробники
# coursework_33
# vacancy
# company







