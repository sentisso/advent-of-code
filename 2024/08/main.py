import os
import numpy as np
from typing import List, Dict, Set


dir_path = os.path.dirname(os.path.realpath(__file__))
grid = np.genfromtxt(os.path.join(dir_path, 'input.txt'), delimiter=1, dtype=np.str_, comments=None)

EMPTY = '.'


def group_antennas() -> Dict[str, Set[tuple]]:
    """
    Group antenna positions by antenna frequency.
    :return:
    """
    groups = dict()
    antennas = np.array(np.where(grid != EMPTY)).T

    for pos in antennas:
        val = grid[tuple(pos)]
        if val not in groups:
            groups[val] = set()

        groups[val].add(tuple(pos))

    return groups


def is_valid_pos(pos: np.array):
    return 0 <= pos[0] < grid.shape[0] and 0 <= pos[1] < grid.shape[1]


def part_one():
    groups = group_antennas()
    antinodes = set()

    for freq in groups:
        for ant1 in groups[freq]:
            ant1_pos = np.array(ant1)
            for ant2 in groups[freq]:
                if ant1 == ant2:
                    continue

                ant2_pos = np.array(ant2)
                pos_diff = ant2_pos - ant1_pos
                antinode = ant2_pos + pos_diff

                if is_valid_pos(antinode):
                    antinodes.add(tuple(antinode))

    print('unique antinodes:', len(antinodes))


def part_two():
    groups = group_antennas()
    antinodes = set()

    for freq in groups:
        for ant1 in groups[freq]:
            ant1_pos = np.array(ant1)

            for ant2 in groups[freq]:
                if ant1 == ant2:
                    continue

                ant2_pos = np.array(ant2)
                pos_diff = ant2_pos - ant1_pos

                # repeat frequency
                antinode = ant2_pos - pos_diff
                while is_valid_pos(antinode):
                    antinodes.add(tuple(antinode))
                    antinode = antinode - pos_diff

    print('unique antinodes:', len(antinodes))


part_one()
part_two()

