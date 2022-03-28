# Потренируйтесь с новым модулем requests. С сайта - базы данных о звездных войнах https://swapi.dev/ скачайте 20 персонажей и сохраните их имена, возраст, пол в БД (sqlite3). Чтобы получить результат запроса -- обратитесь к методу json() объекта Response.

import logging
import time
import requests
import sqlite3


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    url = 'https://swapi.dev/api/'
    lists = []
    i = 1
    count = 21

    while i != count:
        req = requests.get(url=f"{url}people/{i}", timeout=(5, 5))
        logger.info(f'#{i} {req.status_code}')
        if req.status_code == 200:
            logger.info('OK')
            data = req.json()

            name = data['name']
            gender = data['gender']
            age = data['birth_year']
            lists.append(
                [name, age, gender]
            )
        else:
            logger.error('Error')
            count += 1
        i += 1

    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
        name TEXT,
        age TEXT,
        gender TEXT
        );
        """
    )
    conn.commit()

    for i in lists:
        cur.execute("INSERT INTO users(name, age, gender) VALUES (?, ?, ?);", i)
    conn.commit()


if __name__ == "__main__":
    start = time.time()
    logger.info('start program')
    main()
    logger.info('program run in {:.4}'.format(time.time() - start))
