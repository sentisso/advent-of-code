import os
import numpy as np
import timeit


dir_path = os.path.dirname(os.path.realpath(__file__))
stones = np.genfromtxt(os.path.join(dir_path, 'input.txt'), delimiter=' ', dtype=np.str_, comments=None)


def iterate(num: str):
    if len(num) % 2 == 0:
        mid = len(num) // 2
        left = int(num[:mid])
        right = int(num[mid:])

        return [str(left), str(right)]

    if num == '0':
        return ['1']

    return [str(int(num) * 2024)]


mem = {}


def count_nums(num: str, iterations: int):
    if iterations == 0:
        return 1

    key = (num, iterations)
    if key in mem:
        return mem[key]

    nums = iterate(num)

    mem[key] = sum(count_nums(n, iterations - 1) for n in nums)
    return mem[key]


def part_one_two(iterations: int):
    count = sum(count_nums(stone, iterations) for stone in stones)

    print(count)


ms = timeit.timeit(lambda: part_one_two(25), number=1) * 1000
print(f'took {ms:.2f}ms')

ms = timeit.timeit(lambda: part_one_two(75), number=1) * 1000
print(f'took {ms:.2f}ms')
