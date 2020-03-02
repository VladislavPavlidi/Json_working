import requests
import json
import os.path
import sys
import time

# Количество запросов от всех пользователей

requests_list = [i for i in range(200)]

# Обозначения в текстовом файле

text_mission_t = 'Завершенные задачи: '
text_mission_f = 'Оставшиеся задачи: '

# Текущая директория

path = sys.path[0]

# Путь от скрипта до папки, которую в будущем создадим

path_to_dir = r'\tasks'


# Создаем папку tasks

def create_directory():
    """Создает папку 'tasks', если этого не произошло раньше"""
    if os.path.exists(path + r'\tasks'):
        print('this derictory already exist')

    else:
        os.mkdir('tasks')


create_directory()

# Подключаемся к JSON

response_users = requests.get('https://json.medrating.org/users')
print(response_users.status_code)
response_todos = requests.get('https://json.medrating.org/todos')
print(response_todos.status_code)


def missions(list1, list2, from_num, to_num):
    """Добавляет задания в список, в зависимости от их статуса"""

    # Для пользователя

    person_requests = requests_list[from_num: to_num]
    for i in person_requests:
        user_status = []
        try:
            text = response_todos.json()[i]['completed']
            user_status.append(text)
            title = list(response_todos.json()[i]['title'])
            t = [True]
            f = [False]
            if len(title) > 50:
                while len(title) > 50:
                    title.pop()
                title.append('...')
                if user_status == t:
                    list1.append(''.join(title))
                if user_status == f:
                    list2.append(''.join(title))
            else:
                if user_status == t:
                    list1.append(''.join(title))
                elif user_status == f:
                    list2.append(''.join(title))
        except UnboundLocalError:
            print('Ошибка в использовании переменной')
        except KeyError:
            print('У пользователя нет задач')


def writter_creator(number_id, from_num, to_num):
    """Создает txt файл и вписывает в него все необходимое"""
    # Название файла для частных случаев

    username = (response_users.json()[number_id]['username'])
    # Путь к папке:

    real_path = (path + path_to_dir + '\\' + username)

    name = (response_users.json()[number_id]['name'])
    email = (response_users.json()[number_id]['email'])
    company = (response_users.json()[number_id]['company'])

    # Список, которых хранит выполненные задачи

    passed_missions = []

    # Список, которых хранит невыполненные задачи

    lost_missions = []

    # Разбиваем задачи на выполненные и невыполненные

    missions(passed_missions, lost_missions, from_num, to_num)

    psd_miss = '\n'.join(passed_missions)

    lst_miss = '\n'.join(lost_missions)

    # Дата

    now_time = time.strftime("%d.%m.%y %H:%M")

    # В windows нельзя использовать символ ":" в названии файла
    # Поэтому, использовал точку
    file_time = time.strftime("%Y-%m-%dT%H.%M")

    # Текст в файле

    all_about_person = (name + ' ' + '<' + email + '>'
                        ' ' + now_time, '\n' +
                        company['name'], '\n', '\n' +
                        text_mission_t, '\n' +
                        psd_miss, '\n', '\n' +
                        text_mission_f, '\n' +
                        lst_miss)

    # Переводим в строку

    all_about_person_str = ''.join(all_about_person)
    try:
        if os.path.exists(real_path + '.txt'):
            os.rename(real_path + '.txt', real_path + '_' +
                      file_time + '.txt')
            with open(real_path + '.txt', 'x') as f:
                f.write(all_about_person_str)
        else:
            with open(real_path + '.txt', 'x') as f:
                f.write(all_about_person_str)
    except FileNotFoundError:
        print('Не удалось найти нужный файл в указаном пути!')


writter_creator(0, 0, 20)
writter_creator(1, 20, 40)
writter_creator(2, 40, 60)
writter_creator(3, 60, 80)
writter_creator(4, 80, 100)
writter_creator(5, 100, 120)
writter_creator(6, 120, 140)
writter_creator(7, 140, 160)
writter_creator(8, 160, 180)
writter_creator(9, 180, 200)
