import logging
import sqlite3
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
import time
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL = 'https://swapi.dev/api/people/'
conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
               name TEXT,
               age TEXT,
               gender TEXT);
            """)
conn.commit()


def get_data(i: int):
    req = requests.get(url=f"{URL}{i}", timeout=(5, 5))

    if req.status_code != 200:
        return

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
    pool = ThreadPool(processes=cpu_count() * 2)
    pool.map(get_data, list(range(1, 21)))
    pool.close()
    pool.join()

    number_of_people = table_length('db.sqlite', 'users')

    while  number_of_people < 20:
        number_of_people += 1
        get_data(number_of_people)
        number_of_people = table_length('db.sqlite', 'users')



if __name__ == '__main__':
    logger.info('start program')
    start = time.time()
    main()
    logger.info('the program ended and worked: {:.4}sec'.format(time.time() - start))
