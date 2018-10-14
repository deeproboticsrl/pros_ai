"""Sample expert trajectories based on distances calculated
Using max normalisation and trans misc observations Minimal version - remove toes, talus and pros_foot
Trajectory length = 100

Average trajectory length is 1788.35
Min length is  1060 corresponding to file  subject03_Run_20002_cycle2_states.sto
Max length is  2884 corresponding to file  subject17_Run_50001_cycle3_states.sto
"""

import pickle

import numpy as np
from pros_ai.play import get_pos_trans_misc_minimal

# suppresses scientific notation
np.set_printoptions(suppress=True)

trajectory_length = 100

experts_file_path = "/home/joy/zReinforcementLearning/prosthetic-ai/Data/expertsss.obs"
min_distance_path = "./distances/min_distance_minimal_TM.pkl"
experts_stats_path = "./stats/expert_observations_pos_minimal_TM.stats"
expert_filenames_file_path = "../play/motion/experts_file_names.pkl"

with open(min_distance_path, "rb") as f:
    min_distance_dict = pickle.load(f)

with open(experts_stats_path, "rb") as f:
    expert_stats = pickle.load(f)

with open(experts_file_path, "rb") as f:
    expert_trajectories = pickle.load(f)

with open(expert_filenames_file_path, "rb") as f:
    expert_filenames = pickle.load(f)

"""Sample reference trajectory - Choose the one with minimal distance, both mathematically and visually.
 MAX normalised + translational and misc observations
Choices 
1. At fixed interval
2. Weighted with center at points chosen above 

2 will give points that aren't in actual trajectory but they are "expected" to be more free of noise.

But what is the evaluation metric. Note that reference trajectory affects sampling in all the other expert trajectories.
Also we can use the weighting itself in other trajectories too. Lots of choices here

Choose weighting since otherwise throwing away a lot of data.
To make sure it doesn't distort data too much calculate difference between fixed and weighted value and sum it.
Expected to be close to 0 if assumed symmetric noise (dynamics can be non-linear 
although considering very less time so not a problem. but that's why close to 0 and not exactly 0) 
"""

# Example - If value is 2, then samples chosen for weighing would be t-2, t-1, t, t+1, t+2
weighing_window_half_length = 2
window_length = weighing_window_half_length * 2 + 1
weights = [1 / window_length] * window_length

reference_trajectory_index = np.argmin(min_distance_dict["max"])
reference_trajectory_start_index = int(min_distance_dict["max_ind"][reference_trajectory_index])

reference_trajectory = expert_trajectories[reference_trajectory_index]
reference_trajectory_length = len(reference_trajectory)

observation_length = len(get_pos_trans_misc_minimal(reference_trajectory[0]))
reference_trajectory_skip = int(reference_trajectory_length / trajectory_length)
sampled_reference_trajectory = [get_pos_trans_misc_minimal(reference_trajectory[reference_trajectory_start_index])]
non_weighted_sampled_reference_trajectory = [
    get_pos_trans_misc_minimal(reference_trajectory[reference_trajectory_start_index])]

print(reference_trajectory_index)
print(reference_trajectory_start_index)
print(reference_trajectory_length)
print(reference_trajectory_skip)
print(observation_length)

for t in range(reference_trajectory_start_index + reference_trajectory_skip,
               reference_trajectory_start_index + ((trajectory_length - 1) * reference_trajectory_skip) + 1,
               reference_trajectory_skip):
    sample = np.zeros(shape=(observation_length,1))
    for i in range(-weighing_window_half_length, weighing_window_half_length + 1):
        sample += get_pos_trans_misc_minimal(reference_trajectory[(t + i) % reference_trajectory_length])
    sample /= window_length
    sampled_reference_trajectory.append(sample)
    non_weighted_sampled_reference_trajectory.append(
        get_pos_trans_misc_minimal(reference_trajectory[t % reference_trajectory_length]))

sampled_reference_trajectory = np.array(sampled_reference_trajectory)
non_weighted_sampled_reference_trajectory = np.array(non_weighted_sampled_reference_trajectory)

# print(sampled_reference_trajectory)
# print(non_weighted_sampled_reference_trajectory)
print(sampled_reference_trajectory.shape)
print(non_weighted_sampled_reference_trajectory.shape)
print(non_weighted_sampled_reference_trajectory[0].shape)
print(sampled_reference_trajectory[12] - non_weighted_sampled_reference_trajectory[12])
print(np.linalg.norm(sampled_reference_trajectory - non_weighted_sampled_reference_trajectory))

"""Got distortion 0.007817896441640874 which seems small since summed over all dimensions and trajectory length
Hence using the weighing scheme"""

