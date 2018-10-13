"""Goal is to find a state among given experts that best resembles the
initial state of ProstheticsEnv
"""
from osim.env import ProstheticsEnv
from pros_ai.play import MotionGenEnv, get_relative_observations, observation_to_array

model_path = "../gait14dof22musc_pros_20180507.osim"

prosthetic_env = ProstheticsEnv(visualize=False)
motion_env = MotionGenEnv(model_path=model_path, visualize=False)

prosthetic_env.reset()
pros_init_obs = get_relative_observations(prosthetic_env.get_state_desc())
print(pros_init_obs)
print(observation_to_array(pros_init_obs))
