import copy
import glob

import numpy as np


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


def get_relative_observations(observation):
    body_observations = {}
    pelvis_observation = {}

    body_keys = ["body_pos", "body_vel", "body_acc", "body_pos_rot", "body_vel_rot", "body_acc_rot"]
    for key in body_keys:
        pelvis_observation[key] = copy.deepcopy(observation[key]["pelvis"])

    for key in body_keys:
        body_observations[key] = {}
        for body_part in ["pelvis", "head", "torso", "toes_l", "tibia_l", "talus_l", "pros_tibia_r", "pros_foot_r",
                          "femur_l", "femur_r", "calcn_l"]:
            body_observations[key][body_part] = [0.0] * 3
            for i in range(3):
                body_observations[key][body_part][i] = observation[key][body_part][i] - pelvis_observation[key][i]

    body_observations["misc"] = copy.deepcopy(observation["misc"])
    return body_observations


def observation_to_array(observation):
    observation_array = []
    body_keys = ["body_pos", "body_vel", "body_acc", "body_pos_rot", "body_vel_rot", "body_acc_rot"]

    for body_key in body_keys:
        for body_part in ["pelvis", "head", "torso", "toes_l", "tibia_l", "talus_l", "pros_tibia_r", "pros_foot_r",
                          "femur_l", "femur_r", "calcn_l"]:
            for i in range(3):
                observation_array.append(observation[body_key][body_part][i])

    for misc_key in ['mass_center_pos', 'mass_center_vel', 'mass_center_acc']:
        for i in range(3):
            observation_array.append(observation["misc"][misc_key][i])
    return np.array(observation_array).reshape((-1, 1))


def get_positional_observations_array(observation):
    observation_array = []
    body_keys = ["body_pos", "body_pos_rot"]

    for body_key in body_keys:
        for body_part in ["pelvis", "head", "torso", "toes_l", "tibia_l", "talus_l", "pros_tibia_r", "pros_foot_r",
                          "femur_l", "femur_r", "calcn_l"]:
            for i in range(3):
                observation_array.append(observation[body_key][body_part][i])

    for i in range(3):
        observation_array.append(observation["misc"]['mass_center_pos'][i])
    return np.array(observation_array).reshape((-1, 1))


def get_pos_trans_misc_minimal(observation):
    """ No toes_l, talus_l and pros_foot_r
    """
    observation_array = []
    body_keys = ["body_pos"]

    for body_key in body_keys:
        for body_part in ["pelvis", "head", "torso", "tibia_l", "pros_tibia_r",
                          "femur_l", "femur_r", "calcn_l"]:
            for i in range(3):
                observation_array.append(observation[body_key][body_part][i])

    for misc_key in ['mass_center_pos', 'mass_center_vel', 'mass_center_acc']:
        for i in range(3):
            observation_array.append(observation["misc"][misc_key][i])
    return np.array(observation_array).reshape((-1, 1))


def get_expert_observation(observation):
    return get_pos_trans_misc_minimal(observation)


def get_policy_observation(observation):
    return get_pos_trans_misc_minimal(observation)