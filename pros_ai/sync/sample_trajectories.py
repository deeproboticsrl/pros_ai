"""Sample expert trajectories based on distances calculated
Using max normalisation and trans misc observations
Trajectory length = 100

Average trajectory length is 1788.35
Min length is  1060 corresponding to file  subject03_Run_20002_cycle2_states.sto
Max length is  2884 corresponding to file  subject17_Run_50001_cycle3_states.sto
"""

import pickle
from pros_ai.play import get_pos_trans_misc

trajectory_length = 100

experts_file_path = "/home/joy/zReinforcementLearning/prosthetic-ai/Data/expertsss.obs"
min_distance_path = "./distances/min_distance_trans_misc.pkl"
experts_stats_path = "./stats/expert_observations_pos_trans_misc.stats"
expert_filenames_file_path = "../play/motion/experts_file_names.pkl"

with open(min_distance_path, "rb") as f:
    min_distances = pickle.load(f)

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
"""
