import pickle

from pros_ai.play import MotionGenEnv, get_relative_observations

model_path = "/home/joy/zReinforcementLearning/prosthetic-ai/pros_ai/pros_ai/gait14dof22musc_pros_20180507.osim"
visualize = True

"""
Average cycle length is 1788.35 rows in 120 files.
Min row count is  1060 corresponding to file  subject03_Run_20002_cycle2_states.sto
Max row count is  2884 corresponding to file  subject17_Run_50001_cycle3_states.sto
"""

motHeader_indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 21, 38, 39, 40, 41, 42, 43, 44,
                     45, 46, 47, 48, 51, 52, 53, 54, 55, 58]


def play_motion(expert_file_path, indices=None, sleeping_vis=False, sleep_time=2):
    env = MotionGenEnv(model_path=model_path, visualize=visualize)

    # assume indices sorted

    with open(expert_file_path) as f:
        lines = f.readlines()
        num_rows = int(lines[2].split('=')[1])

        # first 6 lines are headers. Start from 7th
        headers = lines[6].split()
        observations = []

        if indices is None:
            indices = range(num_rows)

        # NOTE - indices aren't played in order passed in the array
        visualize_list = [False] * num_rows
        for index in indices:
            visualize_list[index] = True

        # read first line separately to get start time so that can use relative time
        line = lines[7]
        # convert strings to floats
        values = [float(x) for x in line.split()]
        start_time = values[0]
        env.set_visualisation(visualize=visualize_list[0])
        for motHeader_index in motHeader_indices:
            env.model.setStateVariableValue(env.state, env.get_state_variable_name(headers[motHeader_index]),
                                            values[motHeader_index])

        env.model.assemble(env.state)
        env.integrate(endtime=values[0] - start_time)
        if sleeping_vis:
            env.sleep(visualize_list[0], sleep_time=sleep_time)
        env.is_visualizing = visualize_list[0]
        observation = get_relative_observations(env.get_state_desc())
        observations.append(observation)

        file_count = 1
        for line in lines[8:]:
            env.set_visualisation(visualize=visualize_list[file_count])

            # convert strings to floats
            values = [float(x) for x in line.split()]
            for motHeader_index in motHeader_indices:
                env.model.setStateVariableValue(env.state, env.get_state_variable_name(headers[motHeader_index]),
                                                values[motHeader_index])

            env.model.assemble(env.state)
            env.integrate(endtime=(values[0] - start_time))
            if sleeping_vis:
                env.sleep(visualize_list[file_count], sleep_time=sleep_time)
            env.is_visualizing = visualize_list[file_count]
            observation = get_relative_observations(env.get_state_desc())
            observations.append(observation)
            file_count += 1
    observation = observations[25]
    # print(observation)
    # print(len(observation_to_array(observation)))

    file_count = 1
    with open("./obs/" + motion_file_path.split('/')[-1].split('.')[0] + ".obs", 'wb') as f:
        print(len(observations), motion_file_path, file_count)
        # the first observation is bad. it is same as pros env init
        pickle.dump(observations[1:], f)
        file_count += 1


####################################################################################

# t(discrimator_reward) +(1-t) (reinforce_reward) ...we can change t
# ignore toe --- talus rotation -- prosthetic foor rotaion

# observation for turning -- relative difference  pelvis direction -- goal direction


state_data_dir_path = "/home/joy/zReinforcementLearning/prosthetic-ai/Data/state"

motion_file_path = state_data_dir_path + "/./subject01_Run_20002_cycle1_states.sto"
min_rows_motion_file_path = state_data_dir_path + "/subject03_Run_20002_cycle2_states.sto"
max_rows_motion_file_path = state_data_dir_path + "/subject17_Run_50001_cycle3_states.sto"

# motion_file_path = min_rows_motion_file_path
####################################################################################
#
# state_data_dir_path = "/home/joy/zReinforcementLearning/prosthetic-ai/Data/state"
#
# state_files = glob.glob(state_data_dir_path + "/*.sto")
#
# for motion_file_path in state_files:
#
#     # Simulate values from the sto file .. angles are in radians
#
#
#     # play_motion(expert_file_path=motion_file_path, indices=range(234, 280))
#     # play_motion(expert_file_path=motion_file_path, indices=[234, 278, 456, 567], sleeping_vis=True)
#     play_motion(expert_file_path=motion_file_path)
# play_motion(expert_file_path=motion_file_path)
