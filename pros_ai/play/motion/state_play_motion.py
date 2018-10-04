from pros_ai.play.motion.motion_gen_env import MotionGenEnv

model_path = "./gait14dof22musc_pros_20180507.osim"
visualize = True

env = MotionGenEnv(model_path=model_path, visualize=visualize)

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


# don't force pelvis translational co-ordinates as gonna do relative to it and also since they cause problems initially
motHeader_indices = [4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 21, 38, 39, 40, 41, 42, 43, 44,
                     45, 46, 47, 48, 51, 52, 53, 54, 55, 58]

motion_file_path = "../../data/motion//state/subject01_Run_20002_cycle3_states.sto"
####################################################################################

# Simulate values from the sto file .. angles are in radians
with open(motion_file_path) as f:
    # ignore header lines (first 6)
    for i in range(6):
        _ = f.readline()

    headers = f.readline().split()

    count = 0

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

    for line in f.readlines():
        # convert strings to floats
        values = [float(x) for x in line.split()]
        for motHeader_index in motHeader_indices:
            env.model.setStateVariableValue(env.state, get_state_variable_name(headers[motHeader_index]),
                                            values[motHeader_index])

        env.model.assemble(env.state)
        env.integrate(endtime=values[0]-start_time)

####################################################################################
