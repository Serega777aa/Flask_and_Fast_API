#  Напишите программу на Python, которая будет находить
# сумму элементов массива из 1000000 целых чисел.
# � Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
# � Массив должен быть заполнен случайными целыми числами
# от 1 до 100.
# � При решении задачи нужно использовать многопоточность,
# многопроцессорность и асинхронность.
# � В каждом решении нужно вывести время выполнения
# вычислений.
import threading
import time
from random import randint

LEN_ARR = 1000000
arr = [randint(1, 100) for _ in range(LEN_ARR)]
result = 0


def get_sum(start, end, num):
    start_time = time.time()
    global result
    for i in range(start, end):
        result += arr[i]
    print(f'{num}. Result = {result:_} Time = {time.time() - start_time:.10f}')


threads = []
start_time = time.time()
for j in range(10):
    start = j * 100000
    end = start + 100000
    t = threading.Thread(target=get_sum, args=[start, end, j + 1])
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f'Summa = {result}\nTime = {time.time() - start_time:.10f}')
