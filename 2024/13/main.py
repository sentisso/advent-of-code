import os
import re
import numpy as np
from scipy import linalg
from typing import List, Dict, Set, Tuple


dir_path = os.path.dirname(os.path.realpath(__file__))


def parse_coordinates(s: str):
    pattern = r'X.(\d+), Y.(\d+)'
    match = re.search(pattern, s)
    if match:
        x = int(match.group(1))
        y = int(match.group(2))
        return np.array([[x], [y]], dtype=np.int64)
    return None


def load_equations():
    equations = []
    with open(os.path.join(dir_path, 'input.txt'), 'r') as f:
        equation = np.array([[], []], dtype=np.int64)
        for line in f:
            if line.startswith('Button'):
                equation = np.hstack([equation, parse_coordinates(line)])
                continue

            if line.startswith('Prize'):
                equation = np.hstack([equation, parse_coordinates(line)])
                equations.append(equation)
                equation = np.array([[], []], dtype=np.int64)
                continue

    return equations


def solve_equation(equation: np.array):
    A = equation[:, :-1]
    b = equation[:, -1]

    return linalg.solve(A, b)


def is_valid_solution(eq: np.ndarray, x: np.array, upper_limit):
    """
    Valid solution is when all coefficients are natural numbers in range [0, upper_limit].
    """
    x = np.round(x)
    are_natural_numbers = np.all(eq[:, :-1] @ x == eq[:, -1])

    if upper_limit is not None:
        all_in_range = np.all(0 <= x) and np.all(x <= upper_limit)
    else:
        all_in_range = np.all(0 <= x)

    return all_in_range and are_natural_numbers


def get_token_cost(x: np.array):
    return x[0] * 3 + x[1]


def part_one():
    equations = load_equations()
    total_cost = 0

    for eq in equations:
        solution = solve_equation(eq)
        if not is_valid_solution(eq, solution, 100):
            continue

        cost = get_token_cost(solution)
        if cost != np.inf:
            total_cost += cost

    print(total_cost)


def part_two():
    equations = load_equations()
    total_cost = 0

    for eq in equations:
        eq[:, -1] = eq[:, -1] + 10000000000000

        solution = solve_equation(eq)
        if not is_valid_solution(eq, solution, None):
            continue

        cost = get_token_cost(solution)
        if cost != np.inf:
            total_cost += cost

    print(total_cost)


part_one()
part_two()