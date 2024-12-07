import os
import numpy as np


dir_path = os.path.dirname(os.path.realpath(__file__))
grid = np.genfromtxt(os.path.join(dir_path, 'input.txt'), delimiter=1, dtype=np.str_, comments=None)

OBSTACLE = '#'
DIRECTIONS = ['^', '>', 'v', '<']


# TODO totally different O(n^2) approach


def find_guard() -> (str, np.array):
    pos = np.array(np.where(np.isin(grid, DIRECTIONS)))
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
    Run the guard through the grid until it reaches the end or a loop is detected.
    """
    unique_visits = set()
    pos_visits = set()
    while True:
        next_pos = curr_pos + curr_vec
        next_val = get_grid_val(next_pos)

        # if end of grid
        if next_val is None:
            break

        if next_val == OBSTACLE:
            curr_vec = rotate_vec(curr_vec)
            continue

        # if loop detected
        curr_pos_key = tuple(next_pos) + tuple(curr_vec)
        if curr_pos_key in unique_visits:
            return None

        unique_visits.add(curr_pos_key)
        pos_visits.add(tuple(curr_pos))
        curr_pos = next_pos

    return pos_visits


def part_one_two():
    guard, curr_pos = find_guard()
    curr_vec = direction_to_vec(guard)

    visits = simulate_guard(curr_pos, curr_vec)
    print('unique visits:', len(visits) + 1)  # one for the end

    loops = 0
    for visit in visits:
        # place block
        before = grid[visit]
        grid[visit] = OBSTACLE

        if simulate_guard(curr_pos, curr_vec) is None:
            loops += 1

        # revert the block
        grid[visit] = before

    print('possible loops:', loops)


part_one_two()
