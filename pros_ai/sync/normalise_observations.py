"""Find weights to normalise observations from data
1. Divide by max
2. Subtract mean, divide by std. "Normal"ise
"""
import pickle

import numpy as np
from pros_ai.play import observation_to_array, get_positional_observations_array
from robo_rl.common.utils import print_heading

experts_file_path = "/home/joy/zReinforcementLearning/prosthetic-ai/Data/expertsss.obs"

# Load experts
with open(experts_file_path, "rb") as f:
    expert_trajectories = pickle.load(f)

# observation_length = len(observation_to_array(expert_trajectories[0][0]))
observation_length = len(get_positional_observations_array((expert_trajectories[0][0])))
observations_max = np.full(shape=(observation_length, 1), fill_value=-np.inf)
observations_sum = np.zeros(shape=(observation_length, 1))
observations_square_sum = np.zeros(shape=(observation_length, 1))
total_observations = 0

for expert_trajectory in expert_trajectories:
    for observation in expert_trajectory:
        # convert observation to array
        observation_array = get_positional_observations_array(observation)
        # find statistics over these
        for i in range(observation_length):
            observations_max[i][0] = max(observations_max[i], abs(observation_array[i]))
            observations_sum[i][0] += observation_array[i]
            observations_square_sum[i][0] += observation_array[i] ** 2
        total_observations += 1

observations_mean = observations_sum / total_observations
observations_std = np.sqrt(
    abs(observations_square_sum - total_observations * (observations_mean ** 2)) / (total_observations - 1))
print_heading("Observations Max")
print(observations_max)
print_heading("Observations Sum")
print(observations_sum)
print_heading("Observations Square Sum")
print(observations_square_sum)
print_heading("Observations Mean")
print(observations_mean)
print_heading("Observations std")
print(observations_std)
print_heading("Total Observations")
print(total_observations)

# store stats
observation_stats = {"max": observations_max, "mean": observations_mean, "std": observations_std,
                     "total": total_observations}
with open("./stats/expert_observations_pos.stats", "wb") as f:
    pickle.dump(observation_stats, f)
