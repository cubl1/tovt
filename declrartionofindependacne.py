import threading
from time import sleep
import random

lock = threading.Lock()

class Bank:
    def __init__(self):
        self.balance = int(0)
        self.deposit_limit = 100
        self.take_limit = 100
    def deposit(self):
        while True:
            sleep(0.001)
            a = random.choice(range(50, 501))
            self.deposit_limit -= 1
            if self.deposit_limit != -1:
                self.balance += a
                if self.balance >= 500 and lock.locked():
                    lock.release()
                print(f"Пополнение: {a}. Баланс: {self.balance}")
            else:
                break
    def take(self):
        while True:
            sleep(0.001)
            a = random.choice(range(50, 501))
            print(f"Запрос на {a}")
            self.take_limit -= 1
            if self.take_limit < 0:
                break
            if a > self.balance:
                print(f'Запрос отклонён, недостаточно средств')
                lock.acquire()
            else:
                self.balance -= a
                print(f"Снятие: {a}. Баланс: {self.balance}")

bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')



