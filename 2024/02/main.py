import numpy as np
import pandas as pd
import os
import math

dir_path = os.path.dirname(os.path.realpath(__file__))

data = []
with open(os.path.join(dir_path, 'input.txt'), 'r') as f:
    for line in f:
        data.append([int(x) for x in line.split()])


def check_row(row):
    asc = False
    prev = None
    is_correct = False
    for j, val in enumerate(row):
        if j == 1:
            asc = prev < val

        if j > 0:
            diff = prev - val
            if 0 < abs(diff) < 4 and (asc is (diff < 0)):
                is_correct = True
            else:
                is_correct = False
                break

        prev = val

    return is_correct


def part_one():
    correct = 0
    for i, row in enumerate(data):
        if check_row(row):
            correct += 1
            continue

        for j in range(0, len(row)):
            if check_row(row[0:j] + row[j+1:]):
                correct += 1
                break

    print(correct)

part_one()