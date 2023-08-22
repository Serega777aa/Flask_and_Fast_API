#  Напишите программу на Python, которая будет находить
# сумму элементов массива из 1000000 целых чисел.
# � Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
# � Массив должен быть заполнен случайными целыми числами
# от 1 до 100.
# � При решении задачи нужно использовать многопоточность,
# многопроцессорность и асинхронность.
# � В каждом решении нужно вывести время выполнения
# вычислений.
import asyncio
from random import randint
import time

LEN_ARR = 1000000
arr = [randint(1, 100) for _ in range(LEN_ARR)]
start_time = time.time()


async def get_sum(start, end, num):
    res = sum(arr[start:end])
    print(f'{num}. Result: {res:_}')
    return res


async def main():
    tasks = []
    for i in range(10):
        start = i * 100000
        end = start + 100000
        task = asyncio.create_task(get_sum(start, end, i + 1))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    print(f'\nSumma = {sum(results):_}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

print(f'Time = {time.time() - start_time:.10f} sec.')
