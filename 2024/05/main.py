import os
from typing import Dict, Set, List

dir_path = os.path.dirname(os.path.realpath(__file__))

# each key's value is a set of numbers that can come after it (map of successors)
succmap: Dict[int, Set[int]] = {}


def update_successors(args: List[int]):
    """
    Update the succmap with the given args (second args comes after the first arg).
    """
    if args[0] not in succmap:
        succmap[args[0]] = set()

    succmap[args[0]].add(args[1])


def validate_updates(updates: List[int]) -> bool:
    """
    Validate the ordering of the given updates according to the map of successors.
    """
    for i, up in enumerate(updates):
        if i == len(updates) - 1:
            continue

        if updates[i + 1] not in succmap.get(up, set()):
            return False

    return True


def fix_updates(updates: List[int]) -> List[int]:
    # updates as a set
    updates_set = set(updates)

    # number of successors for each update in the update set
    successor_counts = []
    for i, up in enumerate(updates):
        # size of intersection of the update map and all the successors of the current update
        successors = len(updates_set.intersection(succmap.get(up, set())))
        successor_counts.append(successors)

    fixed_updates = [-1] * len(updates)
    for i, cnt in enumerate(successor_counts):
        # by knowing the number of successors in the original updates list, we can find the correct index
        new_i = len(updates) - cnt - 1
        fixed_updates[new_i] = updates[i]

    return fixed_updates


with open(os.path.join(dir_path, 'input.txt'), 'r') as f:
    reading_rules = True
    correct_count = 0
    incorrect_count = 0
    for line in f:
        if reading_rules:
            if line == '\n':
                reading_rules = False
                continue

            update_successors([int(x) for x in line.split('|')])
        else:
            updates = [int(x) for x in line.split(',')]

            if validate_updates(updates):
                correct_count += updates[len(updates) // 2]
            else:
                fixed_updates = fix_updates(updates)
                incorrect_count += fixed_updates[len(fixed_updates) // 2]

    print(correct_count)
    print(incorrect_count)
