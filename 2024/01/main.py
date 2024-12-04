import numpy as np
import pandas as pd
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

data = np.genfromtxt(os.path.join(dir_path, 'input.txt'), delimiter='   ', dtype=np.int64)


def part_one():
    sorted = np.sort(data, axis=0)
    distances = np.abs(sorted[:, 0] - sorted[:, 1])
    distance = np.sum(distances)
    print(distance)


def part_two():
    S1 = np.unique_values(data[:, 0])

    D2 = data[:, 1]
    D2 = D2[np.isin(D2, S1)]  # filter second list by values in first list
    D2_counts = np.unique_counts(D2)

    similarity_score = np.sum(D2_counts.values * D2_counts.counts)
    print(similarity_score)

part_one()
part_two()