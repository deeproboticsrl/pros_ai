import numpy as np
import glob


def print_sim_array(array):
    for i in range(array.getSize()):
        print(array.get(i))


def to_radian(angle):
    return angle / 180 * np.pi


def print_state_row_statistics():
    state_data_dir_path = "/home/joy/zReinforcementLearning/prosthetic-ai/Data/state"

    state_files = glob.glob(state_data_dir_path + "/*.sto")

    total_num_rows = 0
    total_files = 0
    min_row_count = 100000
    max_row_count = 0
    min_row_file = ""
    max_row_file = ""
    for state_file_path in state_files:
        with open(state_file_path) as f:
            # ignore first 2 line
            for i in range(2):
                _ = f.readline()
            num_rows = int(f.readline().split('=')[1])
            total_num_rows += num_rows
            total_files += 1
            if num_rows < min_row_count:
                min_row_count = num_rows
                min_row_file = state_file_path
            if num_rows > max_row_count:
                max_row_count = num_rows
                max_row_file = state_file_path

    avg_num_rows = total_num_rows / total_files
    print("Average cycle length is " + str(avg_num_rows) + " rows in " + str(total_files) + " files.")
    print("Min row count is ", min_row_count, "corresponding to file ", min_row_file)
    print("Max row count is ", max_row_count, "corresponding to file ", max_row_file)

