import pickle

import numpy as np
from pros_ai.play import play_motion

with open("./distances/min_distance.pkl", "rb") as f:
    min_distance_dict = pickle.load(f)

print(min_distance_dict)

# find min among all experts
min_no_norm = np.min(min_distance_dict["no_norm"])
min_max_norm = np.min(min_distance_dict["max"])
min_gaussian_norm = np.min(min_distance_dict["gaussian"])
min_ind_no_norm = np.argmin(min_distance_dict["no_norm"])
min_ind_max_norm = np.argmin(min_distance_dict["max"])
min_ind_gaussian_norm = np.argmin(min_distance_dict["gaussian"])

print(min_no_norm)
print(min_max_norm)
print(min_gaussian_norm)
print(min_ind_no_norm)
print(min_ind_max_norm)
print(min_ind_gaussian_norm)

expert_filenames_file_path = "../play/motion/experts_file_names.pkl"
with open(expert_filenames_file_path, "rb") as f:
    expert_filenames = pickle.load(f)

no_norm_min_file = expert_filenames[min_ind_no_norm]
max_norm_min_file = expert_filenames[min_ind_max_norm]
gaussian_norm_min_file = expert_filenames[min_ind_gaussian_norm]

# index in the trajectory of expert selected by indices found above using argmin
no_norm_index = int(min_distance_dict["no_norm_ind"][min_ind_no_norm])
max_norm_index = int(min_distance_dict["max_ind"][min_ind_max_norm])
gaussian_norm_index = int(min_distance_dict["gaussian_ind"][min_ind_gaussian_norm])

# print file names with min distances
print(no_norm_min_file, no_norm_index)
print(max_norm_min_file, max_norm_index)
print(gaussian_norm_min_file, gaussian_norm_index)

sleep_time = 5
# visualise no norm
# play_motion(expert_file_path=no_norm_min_file, indices=[no_norm_index], sleeping_vis=True, sleep_time=sleep_time)

# visualise max norm
# play_motion(expert_file_path=max_norm_min_file, indices=[max_norm_index], sleeping_vis=True, sleep_time=sleep_time)

# visualise no norm
play_motion(expert_file_path=gaussian_norm_min_file, indices=[gaussian_norm_index], sleeping_vis=True,
            sleep_time=sleep_time)
