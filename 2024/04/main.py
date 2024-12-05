import os

dir_path = os.path.dirname(os.path.realpath(__file__))

grid = []
with open(os.path.join(dir_path, 'input.txt'), 'r') as f:
    for line in f:
        grid.append(line.replace('\n', ''))


def count_occurrences(word: str, i, j):
    count = 0

    # left to right
    if word == grid[i][j:j + len(word)]:
        count += 1

    # right to left
    if word == grid[i][max(j - len(word) + 1, 0):j + 1][::-1]:
        count += 1

    def count_vertical(invert=1):
        match = ''
        for wi in range(len(word)):
            gi = i + (wi * invert)
            if 0 <= gi < len(grid):
                match += grid[gi][j]
            else:
                break

        return word == match

    # bottom to top
    if count_vertical(invert=-1):
        count += 1

    # top to bottom
    if count_vertical(invert=1):
        count += 1

    def count_diagonal(inverti=1, invertj=1):
        match = ''
        for wi in range(len(word)):
            di, dj = i + (wi * inverti), j + (wi * invertj)
            if 0 <= di < len(grid) and 0 <= dj < len(grid[0]):
                match += grid[di][dj]
            else:
                break

        return word == match

    # to bottom right
    if count_diagonal(inverti=1, invertj=1):
        count += 1

    # to bottom left
    if count_diagonal(inverti=1, invertj=-1):
        count += 1

    # to top right
    if count_diagonal(inverti=-1, invertj=1):
        count += 1

    # to top left
    if count_diagonal(inverti=-1, invertj=-1):
        count += 1

    return count


def part_one():
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            total += count_occurrences('XMAS', i, j)

    print(total)


def part_two():
    total = 0
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            A = grid[i][j] == 'A'
            tlM = grid[i - 1][j - 1] == 'M'
            tlS = grid[i - 1][j - 1] == 'S'

            blM = grid[i + 1][j - 1] == 'M'
            blS = grid[i + 1][j - 1] == 'S'

            trM = grid[i - 1][j + 1] == 'M'
            trS = grid[i - 1][j + 1] == 'S'

            brM = grid[i + 1][j + 1] == 'M'
            brS = grid[i + 1][j + 1] == 'S'

            if A and (tlM and brS or tlS and brM) and (trM and blS or trS and blM):
                total += 1

    print(total)


part_one()
part_two()