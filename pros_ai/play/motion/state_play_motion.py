import pickle
from pros_ai.play.motion.motion_gen_env import MotionGenEnv
import glob

model_path = "./gait14dof22musc_pros_20180507.osim"
visualize = True


# Dictionary containing mapping from .sto file headers to state variable names of osim env
motFileHeader_to_stateVariableName_dict = {"pelvis_tilt": "ground_pelvis/pelvis_tilt/value",
                                           "pelvis_list": "ground_pelvis/pelvis_list/value",
                                           "pelvis_rotation": "ground_pelvis/pelvis_rotation/value",
                                           "pelvis_tx": "ground_pelvis/pelvis_tx/value",
                                           "pelvis_ty": "ground_pelvis/pelvis_ty/value",
                                           "pelvis_tz": "ground_pelvis/pelvis_tz/value",
                                           "hip_flexion_r": "hip_r/hip_flexion_r/value",
                                           "hip_adduction_r": "hip_r/hip_adduction_r/value",
                                           "hip_rotation_r": "hip_r/hip_rotation_r/value",
                                           "knee_angle_r": "knee_r/knee_angle_r/value",
                                           "ankle_angle_r": "ankle_r/ankle_angle_r/value",
                                           "hip_flexion_l": "hip_l/hip_flexion_l/value",
                                           "hip_adduction_l": "hip_l/hip_adduction_l/value",
                                           "hip_rotation_l": "hip_l/hip_rotation_l/value",
                                           "knee_angle_l": "knee_l/knee_angle_l/value",
                                           "ankle_angle_l": "ankle_l/ankle_angle_l/value",
                                           "lumbar_extension": "back/lumbar_extension/value",
                                           "pelvis_tilt_u": "ground_pelvis/pelvis_tilt/speed",
                                           "pelvis_list_u": "ground_pelvis/pelvis_list/speed",
                                           "pelvis_rotation_u": "ground_pelvis/pelvis_rotation/speed",
                                           "pelvis_tx_u": "ground_pelvis/pelvis_tx/speed",
                                           "pelvis_ty_u": "ground_pelvis/pelvis_ty/speed",
                                           "pelvis_tz_u": "ground_pelvis/pelvis_tz/speed",
                                           "hip_flexion_r_u": "hip_r/hip_flexion_r/speed",
                                           "hip_adduction_r_u": "hip_r/hip_adduction_r/speed",
                                           "hip_rotation_r_u": "hip_r/hip_rotation_r/speed",
                                           "knee_angle_r_u": "knee_r/knee_angle_r/speed",
                                           "ankle_angle_r_u": "ankle_r/ankle_angle_r/speed",
                                           "hip_flexion_l_u": "hip_l/hip_flexion_l/speed",
                                           "hip_adduction_l_u": "hip_l/hip_adduction_l/speed",
                                           "hip_rotation_l_u": "hip_l/hip_rotation_l/speed",
                                           "knee_angle_l_u": "knee_l/knee_angle_l/speed",
                                           "ankle_angle_l_u": "ankle_l/ankle_angle_l/speed",
                                           "lumbar_extension_u": "back/lumbar_extension/speed",
                                           }


def get_state_variable_name(mot_header):
    return motFileHeader_to_stateVariableName_dict[mot_header]


"""
Average cycle length is 1788.35 rows in 120 files.
Min row count is  1060 corresponding to file  subject03_Run_20002_cycle2_states.sto
Max row count is  2884 corresponding to file  subject17_Run_50001_cycle3_states.sto
"""

# don't force pelvis translational co-ordinates as gonna do relative to it and also since they cause problems initially
motHeader_indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 21, 38, 39, 40, 41, 42, 43, 44,
                     45, 46, 47, 48, 51, 52, 53, 54, 55, 58]

state_data_dir_path = "/home/joy/zReinforcementLearning/prosthetic-ai/Data/state"

motion_file_path = state_data_dir_path + "/subject01_Run_20002_cycle1_states.sto"
min_rows_motion_file_path = state_data_dir_path + "/subject03_Run_20002_cycle2_states.sto"
max_rows_motion_file_path = state_data_dir_path + "/subject17_Run_50001_cycle3_states.sto"

motion_file_path = min_rows_motion_file_path
####################################################################################
#
# state_data_dir_path = "/home/joy/zReinforcementLearning/prosthetic-ai/Data/state"
#
# state_files = glob.glob(state_data_dir_path + "/*.sto")

# for motion_file_path in state_files:
    # Simulate values from the sto file .. angles are in radians
env = MotionGenEnv(model_path=model_path, visualize=visualize)

with open(motion_file_path) as f:
    # ignore header lines (first 6)
    for i in range(6):
        _ = f.readline()

    headers = f.readline().split()
    observations = []

    # read first line separately to get start time
    line = f.readline()
    # convert strings to floats
    values = [float(x) for x in line.split()]
    start_time = values[0]
    for motHeader_index in motHeader_indices:
        env.model.setStateVariableValue(env.state, get_state_variable_name(headers[motHeader_index]),
                                        values[motHeader_index])

    env.model.assemble(env.state)
    env.integrate(endtime=values[0] - start_time)
    observation = env.get_relative_observations()
    observations.append(observation)

    count = 1
    for line in f.readlines():

        # convert strings to floats
        values = [float(x) for x in line.split()]
        for motHeader_index in motHeader_indices:
            env.model.setStateVariableValue(env.state, get_state_variable_name(headers[motHeader_index]),
                                            values[motHeader_index])

        env.model.assemble(env.state)
        env.integrate(endtime=(values[0]-start_time))
        observation = env.get_relative_observations()
        observations.append(observation)
        count += 1
print(observations[25])
        #
        # with open("./obs/"+motion_file_path.split('/')[-1].split('.')[0]+".obs", 'wb') as f:
        #     print(len(observations))
        #     pickle.dump(observations, f)

####################################################################################

# t(discrimator_reward) +(1-t) (reinforce_reward) ...we can change t
# ignore toe --- talus rotation -- prosthetic foor rotaion

# observation for turning -- relative difference  pelvis direction -- goal direction



