import os
from typing import List


dir_path = os.path.dirname(os.path.realpath(__file__))


def find_operators(result: int | float, intermediate: int, args: List[int]):
    if len(args) == 0:
        return result == intermediate

    # addition is next
    if find_operators(result, args[0] + intermediate, args[1:]):
        return True

    # multiplication is next
    if find_operators(result, intermediate * args[0], args[1:]):
        return True

    # concat is next
    if find_operators(result, int(str(intermediate) + str(args[0])), args[1:]):
        return True

    return False


with open(os.path.join(dir_path, 'input.txt'), 'r') as f:
    total = 0
    for line in f:
        result, args = line.split(':')
        result = int(result)
        args = [int(x) for x in args.strip().split(' ')]

        if find_operators(result, 0, args):
            total += result

    print(total)