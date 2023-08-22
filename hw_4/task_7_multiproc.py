#  Напишите программу на Python, которая будет находить
# сумму элементов массива из 1000000 целых чисел.
# � Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
# � Массив должен быть заполнен случайными целыми числами
# от 1 до 100.
# � При решении задачи нужно использовать многопоточность,
# многопроцессорность и асинхронность.
# � В каждом решении нужно вывести время выполнения
# вычислений.
import multiprocessing
import time
from random import randint

LEN_ARR = 1000000
arr = [randint(1, 100) for _ in range(LEN_ARR)]


def get_sum(start, end, num):
    start_time = time.time()
    result = 0
    for i in range(start, end):
        result += arr[i]
    print(f'{num}. Result = {result:_} Time = {time.time() - start_time}')


if __name__ == '__main__':
    processes = []
    start_time = time.time()
    for j in range(10):
        start = j * 100000
        end = start + 100000
        p = multiprocessing.Process(target=get_sum, args=[start, end, j + 1])
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
