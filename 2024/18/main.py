import os
import re
import heapq
import numpy as np
from typing import List, Dict, Set, Tuple


dir_path = os.path.dirname(os.path.realpath(__file__))

blocks = np.genfromtxt(os.path.join(dir_path, 'input.txt'), delimiter=',', dtype=np.int64, comments=None)


def is_pos_valid(pos: Tuple, grid_size: int) -> bool:
    return 0 <= pos[0] < grid_size and 0 <= pos[1] < grid_size


class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, u: tuple, v: tuple):
        if u not in self.edges:
            self.edges[u] = set()

        if v not in self.edges:
            self.edges[v] = set()

        self.edges[u].add(v)
        self.edges[v].add(u)

    def get_neighbors(self, u: tuple) -> Set[tuple]:
        return self.edges.get(u, set())

    def a_star(self, s: tuple, e: tuple):
        # priority queue of opened nodes
        open = []
        # set of closed nodes
        closed = set()
        # g scores (current best path costs)
        g = dict()
        # f scores (path cost estimates to the goal)
        f = dict()
        # map of parents
        parent = dict()

        g[s] = 0
        f[s] = 0
        parent[s] = None
        heapq.heappush(open, (f[s], s))

        while open:
            _, u = heapq.heappop(open)

            # found the path
            if u == e:
                return self.reconstruct_path(parent, e)

            closed.add(u)

            for v in self.get_neighbors(u):
                if v in closed:
                    continue

                g_new = g.get(u, np.inf) + 1  # weight is same for all edges
                f_new = g_new + np.linalg.norm(np.array(u) - np.array(e))  # Euclidean distance

                # if g_new is less than the current g(v), push to queue
                if v not in g or g_new < g.get(v, np.inf):
                    g[v] = g_new
                    f[v] = f_new
                    parent[v] = u
                    heapq.heappush(open, (f_new, v))

        return []

    def reconstruct_path(self, parent: Dict[tuple, tuple], current: tuple) -> List[tuple]:
        path = []
        while current:
            path.append(current)
            current = parent[current]
        return path[::-1]


# optimization idea: keep a global graph and just remove/add the blocked nodes as needed
def load_grid_to_graph(grid_size: int, n_blocks: int) -> Graph:
    graph = Graph()
    block_set = {tuple(x) for x in blocks[:n_blocks]}

    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) in block_set:
                continue

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                ni, nj = i + dx, j + dy

                if is_pos_valid((ni, nj), grid_size) and (ni, nj) not in block_set:
                    graph.add_edge((i, j), (ni, nj))

    return graph


def part_one(grid_size: int, n_blocks: int):
    graph = load_grid_to_graph(grid_size, n_blocks=n_blocks)
    path = graph.a_star((0, 0), (grid_size - 1, grid_size - 1))

    # minus 1 to get the number of steps
    print(len(path) - 1)


def part_two(grid_size: int):
    bs, be = 0, blocks.shape[0]

    # binary search the first block that blocks the path
    while True:
        mid = (bs + be) // 2

        graph = load_grid_to_graph(grid_size, n_blocks=mid)
        path = graph.a_star((0, 0), (grid_size - 1, grid_size - 1))

        # path is not blocked, move to right half
        if len(path) > 0:
            bs = mid + 1
            continue

        # binary search found the block
        if be - bs == 1:
            break

        # path is blocked and binary search continues, move to left half
        be = mid

    print(mid, blocks[mid - 1])


part_one(grid_size=71, n_blocks=1024)
part_two(grid_size=71)
