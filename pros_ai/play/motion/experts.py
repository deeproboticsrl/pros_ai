"""Creates one pickle file containing all experts from separated expert files"""

import glob
import pickle

expert_dir_path = "/home/joy/zReinforcementLearning/prosthetic-ai/Data/"
expert_obs_dir_path = expert_dir_path + "obs/"
expert_state_dir_path = expert_dir_path + "state/"

expert_obs_files = glob.glob(expert_obs_dir_path + "*.obs")

experts_file_path = "./expertsss.obs"
experts_filenames_file_path = "./experts_file_names.pkl"
expert_trajectories = []
expert_file_names = []
for expert_file in expert_obs_files:
    with open(expert_file, "rb") as f:
        expert_trajectory = pickle.load(f)
        expert_trajectories.append(expert_trajectory)
        expert_file_name = expert_file.split('/')[-1].split('.')[0]
        expert_file_names.append(expert_state_dir_path + expert_file_name + '.sto')
        print(len(expert_trajectory))

print(len(expert_trajectories))

with open(experts_file_path, "wb") as f:
    pickle.dump(expert_trajectories, f)

with open(experts_filenames_file_path, "wb") as f:
    pickle.dump(expert_file_names, f)
