from threading import Thread, Lock
from random import randint
from time import sleep


class Bank(Thread):
    lock = Lock()
    balance = 0

    def __init__(self):
        Thread.__init__(self)

    def deposit(self):
        incr = randint(50, 500)
        self.balance += incr
        if self.balance >= 500 and self.lock.locked():
            self.lock.release()
        print(f'Пополнение: {incr}. Баланс: {self.balance}')
        sleep(0.1)

    def take(self):
        dcr = randint(50, 500)
        print(f"Запрос на {dcr}")
        if dcr <= self.balance:
            self.balance -= dcr
            print(f'Снятие: {dcr}. Баланс: {self.balance}')
        else:
            print('Запрос отклонён, недостаточно средств')
            self.lock.acquire()

    def run_deposit(self):
        for _ in range(100):
            self.deposit()

    def run_take(self):
        for _ in range(100):
            self.take()


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = Thread(target=bk.run_deposit)
th2 = Thread(target=bk.run_take)

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
