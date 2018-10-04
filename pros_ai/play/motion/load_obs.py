import pickle

with open("./subject01_Run_20002_cycle1_states.obs", "rb") as f:
    observations = pickle.load(f)
    print(observations[25])
