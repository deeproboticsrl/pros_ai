"""Goal is to find a state among given experts that best resembles the
initial state of ProstheticsEnv
Only use positional observations for distance
"""
import pickle

from osim.env import ProstheticsEnv
from pros_ai.play import MotionGenEnv, get_relative_observations, observation_to_array
from pros_ai.play import get_positional_observations_array

model_path = "../gait14dof22musc_pros_20180507.osim"
experts_file_path = "/home/joy/zReinforcementLearning/prosthetic-ai/Data/expertsss.obs"
experts_stats_path = "./expert_observations.stats"

prosthetic_env = ProstheticsEnv(visualize=False)
motion_env = MotionGenEnv(model_path=model_path, visualize=False)

prosthetic_env.reset()
pros_init_obs_dict = get_relative_observations(prosthetic_env.get_state_desc())
pros_init_obs_array = observation_to_array(pros_init_obs_dict)
pros_init_positional_obs = get_positional_observations_array(pros_init_obs_dict)
# print(pros_init_obs_dict)
# print(pros_init_obs_array)
# print(pros_init_positional_obs)
# print(len(pros_init_obs_dict))
# print(len(pros_init_obs_array))
# print(len(pros_init_positional_obs))

# Load expert stats
with open(experts_stats_path, "rb") as f:
    expert_stats = pickle.load(f)
print(expert_stats)


# Load experts
with open(experts_file_path, "rb") as f:
    expert_trajectories = pickle.load(f)
    # print(len(expert_trajectories))


min_distance_experts = []
min_distance_index_experts = []
