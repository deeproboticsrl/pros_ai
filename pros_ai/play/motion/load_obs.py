import pickle
from pros_ai.play import observation_to_array

with open("./subject01_Run_20002_cycle1_states.obs", "rb") as f:
    observations = pickle.load(f)
    observation = observations[25]
    print(observation)
    print(len(observation_to_array(observation)))
