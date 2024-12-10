import os
import numpy as np
from collections import deque
from typing import List, Dict, Set, Tuple


dir_path = os.path.dirname(os.path.realpath(__file__))
grid = np.genfromtxt(os.path.join(dir_path, 'input.txt'), delimiter=1, dtype=np.int64, comments=None)


def get_valid_neighbors(pos: Tuple):
    """
    Valid neighbors are the ones that (a) are in the grid and (b) are greater by 1.
    """
    neighbors = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]

    val = grid[pos]
    return list(
        filter(
            lambda x: 0 <= x[0] < grid.shape[0] and 0 <= x[1] < grid.shape[1] and grid[x] == val + 1,
            neighbors
        )
    )


def part_one_two(ignore_visited=False):
    trailheads = np.array(np.where(grid == 0)).T

    # queue of positions
    Q = deque[Tuple]()
    scores = 0

    for th in trailheads:
        score = 0
        Q.clear()

        visited = {tuple(th)}
        Q.append(tuple(th))

        while Q:
            pos = Q.popleft()

            if grid[tuple(pos)] == 9:
                score += 1
                continue

            for neighbor in get_valid_neighbors(pos):
                if ignore_visited or neighbor not in visited:
                    visited.add(neighbor)
                    Q.append(neighbor)

        scores += score

    print(scores)


part_one_two()
part_one_two(ignore_visited=True)  # easy pt2 lol :D
