import os
import numpy as np
from collections import deque
from typing import List, Dict, Set, Tuple
import timeit


dir_path = os.path.dirname(os.path.realpath(__file__))
grid = np.genfromtxt(os.path.join(dir_path, 'input.txt'), delimiter=1, dtype=np.str_, comments=None)


def get_neighbors(pos: Tuple):
    neighbors = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
    val = grid[pos]

    same = []
    next = []
    out = []
    for n in neighbors:
        if not (0 <= n[0] < grid.shape[0] and 0 <= n[1] < grid.shape[1]):
            out.append(n)
        elif grid[n] == val:
            same.append(n)
        else:
            next.append(n)

    return same, next, out


def pos_diff(pos1: Tuple, pos2: Tuple):
    return pos1[0] - pos2[0], pos1[1] - pos2[1]


def is_same_side(side_visits: Set, pos: Tuple, inneighbors: List[Tuple], outneighbor: Tuple):
    """
    Is same side if there's an existing inneighbor with the same orientation.
    """
    orientation = pos_diff(outneighbor, pos)

    for inneighbor in inneighbors:
        nside_key = inneighbor + orientation
        if nside_key in side_visits:
            return True

    return False


directions = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])


def part_one_two():
    total_perimeter_cost = 0
    total_side_cost = 0

    # queue for same region plants
    Qin = deque[Tuple]()
    # queue for neighboring region plants
    Qout = deque[Tuple]()

    s = (0, 0)
    visited_out = {s}
    visited_in = set()
    Qout.append(s)

    while Qout:
        pos = Qout.popleft()
        region = grid[pos]

        if pos in visited_in:
            continue

        # set of edge nodes with the direction to "out" (pos, (orientation))
        edge_nodes = set()
        visited_in.add(pos)
        Qin.append(pos)

        perimeter = 0
        area = 0
        while Qin:
            pos = Qin.popleft()
            same, next, out = get_neighbors(pos)

            area += 1
            perimeter += len(next) + len(out)

            for s in same:
                if s in visited_in:
                    continue

                visited_in.add(s)
                Qin.append(s)

            for n in next:
                if n in visited_out:
                    continue

                visited_out.add(n)
                Qout.append(n)

            # if this is an edge node, add it with each out direction
            for n in next + out:
                edge_nodes.add((pos, pos_diff(n, pos)))

        sides = 0
        while len(edge_nodes) > 0:
            edge_node = edge_nodes.pop()
            sides += 1

            # try to find all possible same edge neighbors by iterating each direction
            for direction in directions:
                curr_pos = np.array(edge_node[0])
                while True:
                    curr_pos = curr_pos + direction
                    pos_key = (tuple(curr_pos), tuple(edge_node[1]))

                    # no more same side neighbors
                    if pos_key not in edge_nodes:
                        break

                    # remove each same side neighbor so they are counted as one side
                    edge_nodes.remove(pos_key)

        total_perimeter_cost += area * perimeter
        total_side_cost += area * sides

    print('total side cost:', total_side_cost)
    print('total perimeter cost:', total_perimeter_cost)


part_one_two()
