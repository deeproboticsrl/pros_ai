"""Goal is to find a state among given experts that best resembles the
initial state of ProstheticsEnv
Only use positional observations for distance
"""
import copy
import pickle

import numpy as np
from osim.env import ProstheticsEnv
from pros_ai.play import MotionGenEnv, get_relative_observations, observation_to_array
from pros_ai.play import get_positional_observations_array

# suppresses scientific notation
np.set_printoptions(suppress=True)

model_path = "../gait14dof22musc_pros_20180507.osim"
experts_file_path = "/home/joy/zReinforcementLearning/prosthetic-ai/Data/expertsss.obs"
experts_stats_path = "./stats/expert_observations.stats"
experts_pos_stats_path = "./stats/expert_observations_pos.stats"

prosthetic_env = ProstheticsEnv(visualize=False)
motion_env = MotionGenEnv(model_path=model_path, visualize=False)

# Load expert stats
# with open(experts_stats_path, "rb") as f:
#     expert_stats = pickle.load(f)
# print(expert_stats)
with open(experts_pos_stats_path, "rb") as f:
    expert_pos_stats = pickle.load(f)
# print(expert_pos_stats)

prosthetic_env.reset()
pros_init_obs_dict = get_relative_observations(prosthetic_env.get_state_desc())
pros_init_obs_array = observation_to_array(pros_init_obs_dict)
pros_init_positional_obs = get_positional_observations_array(pros_init_obs_dict)

max_normalised_pros_init_obs = np.empty(shape=(len(pros_init_positional_obs), 1))
gaussian_normalised_pros_init_obs = copy.deepcopy(pros_init_positional_obs - expert_pos_stats["mean"])

for i in range(len(pros_init_positional_obs)):
    if expert_pos_stats["max"][i]:
        max_normalised_pros_init_obs[i] = pros_init_positional_obs[i] / expert_pos_stats["max"][i]
    if expert_pos_stats["std"][i]:
        gaussian_normalised_pros_init_obs[i] = gaussian_normalised_pros_init_obs[i] / expert_pos_stats["std"][i]

# print(pros_init_obs_dict)
# print(pros_init_obs_array)
# print(pros_init_positional_obs)
# print(len(pros_init_obs_dict))
# print(pros_init_obs_array.shape)
# print(pros_init_positional_obs.shape)
# print(gaussian_normalised_pros_init_obs)
# print(max_normalised_pros_init_obs)

# Load experts
with open(experts_file_path, "rb") as f:
    expert_trajectories = pickle.load(f)
    # print(len(expert_trajectories))

num_experts = len(expert_trajectories)
min_distance_experts_no_norm = np.full(shape=(num_experts, 1), fill_value=np.inf)
min_distance_experts_max_norm = np.full(shape=(num_experts, 1), fill_value=np.inf)
min_distance_experts_gaussian_norm = np.full(shape=(num_experts, 1), fill_value=np.inf)
min_distance_index_experts_no_norm = np.zeros(shape=(num_experts, 1))
min_distance_index_experts_max_norm = np.zeros(shape=(num_experts, 1))
min_distance_index_experts_gaussian_norm = np.zeros(shape=(num_experts, 1))

# normalise observations
for i in range(len(expert_trajectories)):
    expert_trajectory = expert_trajectories[i]
    for j in range(len(expert_trajectory)):
        observation = expert_trajectory[j]
        # convert observation to array
        pos_observation_array = get_positional_observations_array(observation)
        max_normalised_pos_obs_array = np.empty(shape=(len(pos_observation_array), 1))
        gaussian_normalised_pos_obs_array = copy.deepcopy(pos_observation_array - expert_pos_stats["mean"])

        for k in range(len(pos_observation_array)):
            if expert_pos_stats["max"][k]:
                max_normalised_pos_obs_array[k] = pos_observation_array[k] / expert_pos_stats["max"][k]
            if expert_pos_stats["std"][k]:
                gaussian_normalised_pos_obs_array[k] = gaussian_normalised_pos_obs_array[k] / expert_pos_stats["std"][k]

        # calculate distance
        no_norm_pos_distance = np.sum(abs(pos_observation_array - pros_init_positional_obs))
        max_normalised_pos_distance = np.sum((max_normalised_pos_obs_array - max_normalised_pros_init_obs) ** 2)
        gaussian_normalised_pos_distance = np.sum(
            (gaussian_normalised_pos_obs_array - gaussian_normalised_pros_init_obs) ** 2)

        # update minima
        if no_norm_pos_distance < min_distance_experts_no_norm[i]:
            min_distance_experts_no_norm[i] = no_norm_pos_distance
            min_distance_index_experts_no_norm[i] = j

        if max_normalised_pos_distance < min_distance_experts_max_norm[i]:
            min_distance_experts_max_norm[i] = max_normalised_pos_distance
            min_distance_index_experts_max_norm[i] = j

        if gaussian_normalised_pos_distance < min_distance_experts_gaussian_norm[i]:
            min_distance_experts_gaussian_norm[i] = gaussian_normalised_pos_distance
            min_distance_index_experts_gaussian_norm[i] = j

min_distance_dict = {"max": min_distance_experts_max_norm, "gaussian": min_distance_experts_gaussian_norm,
                     "no_norm": min_distance_experts_no_norm, "max_ind": min_distance_index_experts_max_norm,
                     "gaussian_ind": min_distance_index_experts_gaussian_norm,
                     "no_norm_ind": min_distance_index_experts_no_norm}

with open("./distances/min_distance.pkl", "wb") as f:
    pickle.dump(min_distance_dict, f)

print(min_distance_dict)
