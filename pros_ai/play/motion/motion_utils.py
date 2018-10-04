import numpy as np


def print_sim_array(array):
    for i in range(array.getSize()):
        print(array.get(i))


def to_radian(angle):
    return angle / 180 * np.pi

