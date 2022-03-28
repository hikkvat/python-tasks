# Добавим еще одного персонажа -- главный директор с печатным станком.

# По условию, как только количество проданных билетов приближается к такому,
# что каждый из продавцов сможет продать не более одного,
# то в этот момент директор должен добавить в общее число доступных билетов еще сколько-то.

# Например, это выглядит так:

# всего билетов осталось 4, директор добавляет 6, всего билетов 10.
# Пусть директор может так делать, пока общее число билетов не превысило общее число посадочных мест.
# Пока директор пополняет билеты, продавцы не могут продавать билеты.

import logging
import random
import threading
import time

TOTAL_TICKETS = 10
AVAILABLE_TICKETS = 5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore):
        super(Director, self).__init__()
        self.lock = semaphore
        logger.info('Director started work')

    def run(self):
        global TOTAL_TICKETS, AVAILABLE_TICKETS
        while TOTAL_TICKETS:
            if AVAILABLE_TICKETS < 4:
                with self.lock:
                    tickets_to_print = 5 - (AVAILABLE_TICKETS % 5)
                    if tickets_to_print > TOTAL_TICKETS:
                        tickets_to_print = TOTAL_TICKETS
                    AVAILABLE_TICKETS += tickets_to_print
                    logger.info(f'Director put {tickets_to_print} new tickets')
        logger.info('Director stops work, not more tickets left')


class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore):
        super().__init__()
        self.sem = semaphore
        self.tickets_sold = 0
        logger.info(f'{self.getName()} Seller started work')

    def run(self):
        global TOTAL_TICKETS, AVAILABLE_TICKETS
        is_running = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                AVAILABLE_TICKETS -= 1
                logger.info(f'{self.getName()} sold one;  {TOTAL_TICKETS} left')
        logger.info(f'Seller {self.getName()} sold {self.tickets_sold} tickets')

    def random_sleep(self):
        time.sleep(random.randint(0, 1))


def main():
    semaphore = threading.Semaphore()
    director = Director(semaphore=semaphore)
    director.start()
    sellers = [director]
    for _ in range(4):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()


if __name__ == '__main__':
    main()
