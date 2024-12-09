import os
import numpy as np
from typing import List, Dict, Set


dir_path = os.path.dirname(os.path.realpath(__file__))
disk = np.genfromtxt(os.path.join(dir_path, 'input.txt'), delimiter=1, dtype=np.int64, comments=None)


def sum_arithmetic_series(n: int, a1: int, a2: int) -> int:
    return n * (a1 + a2) // 2


def part_one():
    """
    O(n) solution, where n is the raw input length (not the actual expanded input).
    """
    checksum = 0
    occupied_segments = disk[::2].copy()
    empty_segments = disk[1::2].copy()

    # virtual address of the last occupied segment
    last_occupied_i = len(occupied_segments) - 1
    # current physical address
    pa = 0

    for i, empty in enumerate(empty_segments):
        # first is an occupied segment

        size = occupied_segments[i]
        checksum += i * sum_arithmetic_series(n=size, a1=pa, a2=pa + size - 1)
        pa += size

        # followed by an empty segment
        while empty > 0 and i < last_occupied_i:
            last_occupied_size = occupied_segments[last_occupied_i]
            to_transfer = min(empty, last_occupied_size)

            # begin "transferring" data...
            occupied_segments[last_occupied_i] -= to_transfer
            checksum += last_occupied_i * sum_arithmetic_series(n=to_transfer, a1=pa, a2=pa + to_transfer - 1)

            # decrement transferred indices
            if occupied_segments[last_occupied_i] == 0:
                last_occupied_i -= 1

            pa += to_transfer
            empty -= to_transfer

        # no more occupied segments
        if i == last_occupied_i:
            break

    print('checksum:', checksum)


def part_two():
    checksum = 0

    # shifted cumulative sum gives the physical addresses of each segment
    segments_pa = np.cumsum(np.insert(disk, [0], [0]))

    occupied_segments, occupied_segments_pa = disk[::2].copy(), segments_pa[::2]
    empty_segments, empty_segments_pa = disk[1::2].copy(), segments_pa[1::2]

    for fi in reversed(range(len(occupied_segments))):
        size = occupied_segments[fi]

        too_big = True
        for i in range(fi):
            empty = empty_segments[i]
            if empty < size:
                continue

            pa = empty_segments_pa[i]
            cs = fi * sum_arithmetic_series(n=size, a1=pa, a2=pa + size - 1)
            checksum += cs

            empty_segments[i] -= size
            empty_segments_pa[i] += size
            too_big = False
            break

        if not too_big:
            continue

        # no empty segment is big enough
        pa = occupied_segments_pa[fi]
        checksum += fi * sum_arithmetic_series(n=size, a1=pa, a2=pa + size - 1)

    print('checksum (entire files):', checksum)


part_one()
part_two()
