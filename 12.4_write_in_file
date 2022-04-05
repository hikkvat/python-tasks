# Одна из классических проблем при работе с многопоточными и многопроцессорными программами -- организация записи в файл.

# Реализуйте такую программу, где последовательно, с интервалом в 1 секунду, будет запущенно 10 потоков.

# Каждый из них должен в течение 20 секунд писать лог-сообщение в файл, где будет <имя-процесса/потока>-<дата>. Дату нужно получить с этого сайта https://showcase.api.linx.twenty57.net/UnixTime/fromunix?timestamp=1549892280

# Записи в файле должны быть отсортированы по таймштампу. Записи должны быть отсортированны ДО записи в файл.

import logging.config
import threading
import time
from datetime import datetime
import requests

logging.basicConfig(level=logging.INFO, filename='logfile.log')
logger = logging.getLogger(__name__)

URL = f'https://showcase.api.linx.twenty57.net/UnixTime/fromunix?timestamp='

lock = threading.Lock()


def get_time(url):
    with lock:
        for i in range(20):
            address = f'{url}{int(datetime.now().timestamp())}'
            response = requests.get(url=address).json()
            thread_name = threading.current_thread().name
            logger.info(f'<{thread_name}>-<{response}>')
            time.sleep(1)
            print(f'{thread_name} - load data{i + 1}')


def main():
    threads = []
    for i in range(10):
        time.sleep(1)
        thread = threading.Thread(target=get_time, args=(URL,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    print('program started')
    start = time.time()
    main()
    print('the program ended and worked: {:.4}sec'.format(time.time() - start))
