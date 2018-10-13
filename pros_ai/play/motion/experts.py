"""Creates one pickle file containing all experts from separated expert files"""

import glob
import pickle

expert_dir_path = "/home/joy/zReinforcementLearning/prosthetic-ai/Data/obs/"

expert_obs_files = glob.glob(expert_dir_path + "*.obs")

experts_file_path = "./expertsss.obs"
expert_trajectories = []
for expert_file in expert_obs_files:
    with open(expert_file, "rb") as f:
        expert_trajectoy = pickle.load(f)
        expert_trajectories.append(expert_trajectoy)
        print(len(expert_trajectoy))

print(len(expert_trajectories))

with open(experts_file_path, "wb") as f:
    pickle.dump(expert_trajectories, f)