import os
import numpy as np
from typing import Dict, List, Tuple

# TODO no time to finish, but should be "theoretically" fast

dir_path = os.path.dirname(os.path.realpath(__file__))
grid = np.genfromtxt(os.path.join(dir_path, 'input.txt'), delimiter=1, dtype=np.str_, comments=None)

OBSTACLE = '#'
GRID_DIRECTIONS = ['^', '>', 'v', '<']

# row_to_block[idx] = list of obstacles at row idx, sorted by col idx (position, row idx in col_to_block)
row_to_block: Dict[int, np.ndarray] = dict()
# col_to_block[idx] = list of obstacles at col idx, sorted by row idx (position, col idx in row_to_block)
col_to_block: Dict[int, np.ndarray] = dict()


def build_block_map():
    # find obstacle by row, then col (row-col sort)
    obstacles = np.array(np.where(grid == OBSTACLE))

    for obs_pos in obstacles.T:
        row, col = obs_pos

        if row not in row_to_block:
            row_to_block[row] = np.array([])

        # append obstacle to row sorted by col
        row_to_block[row] = np.append(row_to_block[row], col)

    # by transposing the grid we can find obstacles by col, then row (col-row sort)
    obstacles = np.array(np.where(grid.T == OBSTACLE))
    for obs_pos in obstacles.T:
        col, row = obs_pos

        if col not in col_to_block:
            col_to_block[col] = np.array([])

        # append obstacle to col sorted by row
        col_to_block[col] = np.append(col_to_block[col], row)


def random_insert_block(obs_pos: tuple):
    """
    Random insert block position to the row/col block maps.
    Respects the ordering.
    :returns: (row, col) indices in the row/col maps.
    """
    row, col = obs_pos

    if row not in row_to_block:
        row_to_block[row] = np.array([col])
        colidx = 0
    else:
        # insert col value at sorted index
        colidx = np.searchsorted(row_to_block[row], col)
        row_to_block[row] = np.insert(row_to_block[row], [colidx], col)

    if col not in col_to_block:
        col_to_block[col] = np.array([row])
        rowidx = 0
    else:
        # insert row value at sorted index
        rowidx = np.searchsorted(col_to_block[col], row)
        col_to_block[col] = np.insert(col_to_block[col], [rowidx], row)

    return (rowidx, colidx)


def random_remove_block(obs_pos: tuple, obs_idx: tuple):
    """
    Remove a block from the row/col maps at given indices.
    """
    row, col = obs_pos
    rowidx, colidx = obs_idx

    row_to_block[row] = np.delete(row_to_block[row], [colidx])
    col_to_block[col] = np.delete(col_to_block[col], [rowidx])


def find_guard() -> (str, np.array):
    pos = np.array(np.where(np.isin(grid, GRID_DIRECTIONS)))
    pos = pos[:, 0]  # 2d index of the first occurrence
    return grid[tuple(pos)], pos


def direction_to_vec(guard: str):
    if guard == '^':
        return [-1, 0]
    elif guard == '>':
        return [0, 1]
    elif guard == 'v':
        return [1, 0]
    elif guard == '<':
        return [0, -1]
    else:
        raise ValueError(f'Invalid guard: {guard}')


def rotate_vec(vec):
    # clockwise rotation matrix
    M = np.array([[0, 1], [-1, 0]])

    return M @ vec


def get_grid_val(pos: np.array):
    if 0 <= pos[0] < grid.shape[0] and 0 <= pos[1] < grid.shape[1]:
        return grid[tuple(pos)]

    return None


def simulate_guard(curr_pos, curr_vec):
    """
    Run the guard through the grid until it reaches the end.
    :returns: Set of visited positions
    """
    # (position) -> (rotation vector)
    visits: Dict[Tuple, np.ndarray] = dict()
    while True:
        next_pos = curr_pos + curr_vec
        next_val = get_grid_val(next_pos)

        # if end of grid
        if next_val is None:
            break

        if next_val == OBSTACLE:
            curr_vec = rotate_vec(curr_vec)
            continue

        # keep only the first pass-through
        if tuple(curr_pos) not in visits:
            visits[tuple(curr_pos)] = curr_vec

        curr_pos = next_pos

    return visits


def find_next_obstacle(curr_pos, curr_vec):
    row, col = curr_pos

    if up:
        rowidx = np.searchsorted(col_to_block[col], [row], side='left')
        if rowidx == 0:
            return None

        return col_to_block[col][rowidx - 1], col

    if right:
        colidx = np.searchsorted(row_to_block[row], [col], side='right')
        if colidx == len(row_to_block[row]):
            return None

        return row_to_block[row][colidx]

    if down:
        # TODO

    if left:
        # TODO


def detect_loop(curr_pos, curr_vec):
    while True:
        next_obs


def part_one_two():
    guard, curr_pos = find_guard()
    curr_vec = direction_to_vec(guard)

    visits = simulate_guard(curr_pos, curr_vec)
    print('unique visits:', len(visits) + 1)  # one for the end

    loops = 0
    for visit in visits:
        obs_pos = visit

        # place block
        obs_idx = random_insert_block(obs_pos)

        if detect_loop(curr_pos, curr_vec):
            loops += 1

        # revert the block
        random_remove_block(obs_pos, obs_idx)

    print('possible loops:', loops)



part_one_two()
