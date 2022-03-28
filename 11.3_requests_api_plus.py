# Ускорьте код из предыдущего задания, добавив в него потоки.
# Сравните результаты. Не забудьте проверить, как работает база данных.
# Не нужно ли добавить для ее работы какой-нибудь примитив синхронизации ?

import requests
import sqlite3
import logging
import threading
import time

URL = 'https://swapi.dev/api/'
lists = []

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
               name TEXT,
               age TEXT,
               gender TEXT);
            """)
conn.commit()

def get_data(url: str, i: int):
    req = requests.get(url=f"{url}people/{i}", timeout=(5, 5))

    if req.status_code != 200:
        raise RuntimeError(f"bad url: {url}people/{i}")

    logger.info(f'#{i} - load data')
    data = req.json()
    name = data['name']
    gender = data['gender']
    age = data['birth_year']

    with sqlite3.connect('db.sqlite', check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(name, age, gender) VALUES (?, ?, ?);", [name, age, gender])
        conn.commit()

    logger.info(f"#{i} {name} added on db")


def table_length(db, name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(f"select * from {name}")
    return len(cursor.fetchall())


def main():
    threads = []

    for i in range(1, 21):
        thread = threading.Thread(target=get_data, args=(URL, i))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    number_of_people = table_length('db.sqlite', 'users')

    while  number_of_people < 20:
        number_of_people += 1
        get_data(URL, number_of_people)
        number_of_people = table_length('db.sqlite', 'users')


if __name__ == '__main__':
    logger.info('start program')
    start = time.time()
    main()
    logger.info('program run in {:.4}'.format(time.time() - start))
