from osim.env import ProstheticsEnv
import numpy as np
import ipdb
file ="./subject01_Run_20002_cycle1_states.sto"
f = open(file)

headers =f.readline().split()
print(headers)
# for i in range(len(header)):
    # print(i,header[i])
# ipdb.set_trace()
env =ProstheticsEnv(visualize=False)
env.reset()
state =env.get_state_desc()

body_part =[*state['body_pos'].keys()]
joint_part = [*state['joint_pos'].keys()]

# print(body_part)
# print(joint_part)

# size=env.osim_model.model.getStateVariableNames().getSize()
# vec=[]
# for i in range(size):
#     vec.append(env.osim_model.model.getStateVariableNames().get(i))

# print(vec)

coord=['ground_pelvis/pelvis_tilt/value', 'ground_pelvis/pelvis_tilt/speed', 'ground_pelvis/pelvis_list/value',
       'ground_pelvis/pelvis_list/speed', 'ground_pelvis/pelvis_rotation/value', 'ground_pelvis/pelvis_rotation/speed',
       'ground_pelvis/pelvis_tx/value', 'ground_pelvis/pelvis_tx/speed', 'ground_pelvis/pelvis_ty/value',
       'ground_pelvis/pelvis_ty/speed', 'ground_pelvis/pelvis_tz/value', 'ground_pelvis/pelvis_tz/speed',
       'hip_r/hip_flexion_r/value', 'hip_r/hip_flexion_r/speed', 'hip_r/hip_adduction_r/value',
       'hip_r/hip_adduction_r/speed', 'hip_r/hip_rotation_r/value', 'hip_r/hip_rotation_r/speed',
       'knee_r/knee_angle_r/value', 'knee_r/knee_angle_r/speed', 'ankle_r/ankle_angle_r/value',
       'ankle_r/ankle_angle_r/speed', 'hip_l/hip_flexion_l/value', 'hip_l/hip_flexion_l/speed',
       'hip_l/hip_adduction_l/value', 'hip_l/hip_adduction_l/speed', 'hip_l/hip_rotation_l/value',
       'hip_l/hip_rotation_l/speed', 'knee_l/knee_angle_l/value', 'knee_l/knee_angle_l/speed',
       'ankle_l/ankle_angle_l/value', 'ankle_l/ankle_angle_l/speed', 'back/lumbar_extension/value',
       'back/lumbar_extension/speed', 'abd_r/activation', 'abd_r/fiber_length', 'add_r/activation',
       'add_r/fiber_length', 'hamstrings_r/activation', 'hamstrings_r/fiber_length', 'bifemsh_r/activation',
       'bifemsh_r/fiber_length', 'glut_max_r/activation', 'glut_max_r/fiber_length', 'iliopsoas_r/activation',
       'iliopsoas_r/fiber_length', 'rect_fem_r/activation', 'rect_fem_r/fiber_length', 'vasti_r/activation',
       'vasti_r/fiber_length', 'abd_l/activation', 'abd_l/fiber_length', 'add_l/activation', 'add_l/fiber_length',
       'hamstrings_l/activation', 'hamstrings_l/fiber_length', 'bifemsh_l/activation', 'bifemsh_l/fiber_length',
       'glut_max_l/activation', 'glut_max_l/fiber_length', 'iliopsoas_l/activation', 'iliopsoas_l/fiber_length',
       'rect_fem_l/activation', 'rect_fem_l/fiber_length', 'vasti_l/activation', 'vasti_l/fiber_length',
       'gastroc_l/activation', 'gastroc_l/fiber_length', 'soleus_l/activation', 'soleus_l/fiber_length',
       'tib_ant_l/activation', 'tib_ant_l/fiber_length']

# body_part=['pelvis', 'femur_r', 'pros_tibia_r', 'pros_foot_r', 'femur_l', 'tibia_l', 'talus_l', 'calcn_l', 'toes_l', 'torso', 'head']
# joint_part =['ground_pelvis', 'hip_r', 'knee_r', 'ankle_r', 'hip_l', 'knee_l', 'ankle_l', 'subtalar_l', 'mtp_l', 'back', 'back_0']

'''
Body_part
{'pelvis': [0.0, 0.94, 0.0], 'femur_r': [-0.0707, 0.8738999999999999, 0.0835],
'pros_tibia_r': [-0.07519985651753601, 0.47807930355164957, 0.0835],
'pros_foot_r': [-0.07519985651753601, 0.04807930355164958, 0.0835],
'femur_l': [-0.0707, 0.8738999999999999, -0.0835], 'tibia_l': [-0.07519985651753601, 0.47807930355164957, -0.0835],
'talus_l': [-0.07519985651753601, 0.04807930355164958, -0.0835],
'calcn_l': [-0.123969856517536, 0.006129303551649576, -0.09142],
'toes_l': [0.05483014348246398, 0.004129303551649576, -0.0925], 'torso': [-0.1007, 1.0214999999999999, 0.0],
'head': [-0.052764320996907754, 1.5694070821576522, 0.0]}

{'ground_pelvis': [0.0, 0.0, 0.0, 0.0, 0.94, 0.0], 'hip_r': [0.0, 0.0, 0.0], 'knee_r': [0.0], 'ankle_r': [0.0],
'hip_l': [0.0, 0.0, 0.0], 'knee_l': [0.0], 'ankle_l': [0.0], 'subtalar_l': [], 'mtp_l': [], 'back': [-0.0872665],
'back_0': []}

muscles =(['abd_r', 'add_r', 'hamstrings_r', 'bifemsh_r', 'glut_max_r', 'iliopsoas_r',
'rect_fem_r', 'vasti_r', 'abd_l', 'add_l', 'hamstrings_l', 'bifemsh_l', 'glut_max_l',
'iliopsoas_l', 'rect_fem_l', 'vasti_l', 'gastroc_l', 'soleus_l', 'tib_ant_l'])

HEADER


['time', 'pelvis_tilt', 'pelvis_list', 'pelvis_rotation', 'pelvis_tx', 'pelvis_ty', 'pelvis_tz', 'hip_flexion_r',
'hip_adduction_r', 'hip_rotation_r', 'knee_angle_r', 'ankle_angle_r', 'subtalar_angle_r', 'mtp_angle_r', 'hip_flexion_l',
'hip_adduction_l', 'hip_rotation_l', 'knee_angle_l', 'ankle_angle_l', 'subtalar_angle_l', 'mtp_angle_l',
'lumbar_extension', 'lumbar_bending', 'lumbar_rotation', 'arm_flex_r', 'arm_add_r', 'arm_rot_r', 'elbow_flex_r',
'pro_sup_r', 'wrist_flex_r', 'wrist_dev_r', 'arm_flex_l', 'arm_add_l', 'arm_rot_l', 'elbow_flex_l', 'pro_sup_l',
'wrist_flex_l', 'wrist_dev_l', 'pelvis_tilt_u', 'pelvis_list_u', 'pelvis_rotation_u', 'pelvis_tx_u', 'pelvis_ty_u',
'pelvis_tz_u', 'hip_flexion_r_u', 'hip_adduction_r_u', 'hip_rotation_r_u', 'knee_angle_r_u', 'ankle_angle_r_u',
'subtalar_angle_r_u', 'mtp_angle_r_u', 'hip_flexion_l_u', 'hip_adduction_l_u', 'hip_rotation_l_u', 'knee_angle_l_u',
'ankle_angle_l_u', 'subtalar_angle_l_u', 'mtp_angle_l_u', 'lumbar_extension_u', 'lumbar_bending_u', 'lumbar_rotation_u',
'arm_flex_r_u', 'arm_add_r_u', 'arm_rot_r_u', 'elbow_flex_r_u', 'pro_sup_r_u', 'wrist_flex_r_u', 'wrist_dev_r_u',
'arm_flex_l_u', 'arm_add_l_u', 'arm_rot_l_u', 'elbow_flex_l_u', 'pro_sup_l_u', 'wrist_flex_l_u', 'wrist_dev_l_u',
'glut_med1_r.activation', 'glut_med1_r.fiber_length', 'glut_med2_r.activation', 'glut_med2_r.fiber_length',
'glut_med3_r.activation', 'glut_med3_r.fiber_length', 'glut_min1_r.activation', 'glut_min1_r.fiber_length',
'glut_min2_r.activation', 'glut_min2_r.fiber_length', 'glut_min3_r.activation', 'glut_min3_r.fiber_length',
'semimem_r.activation', 'semimem_r.fiber_length', 'semiten_r.activation', 'semiten_r.fiber_length', 'bifemlh_r.activation',
'bifemlh_r.fiber_length', 'bifemsh_r.activation', 'bifemsh_r.fiber_length', 'sar_r.activation', 'sar_r.fiber_length',
'add_long_r.activation', 'add_long_r.fiber_length', 'add_brev_r.activation', 'add_brev_r.fiber_length',
'add_mag1_r.activation', 'add_mag1_r.fiber_length', 'add_mag2_r.activation', 'add_mag2_r.fiber_length',
'add_mag3_r.activation', 'add_mag3_r.fiber_length', 'tfl_r.activation', 'tfl_r.fiber_length', 'pect_r.activation',
'pect_r.fiber_length', 'grac_r.activation', 'grac_r.fiber_length', 'glut_max1_r.activation', 'glut_max1_r.fiber_length',
'glut_max2_r.activation', 'glut_max2_r.fiber_length', 'glut_max3_r.activation', 'glut_max3_r.fiber_length',
'iliacus_r.activation', 'iliacus_r.fiber_length', 'psoas_r.activation', 'psoas_r.fiber_length', 'quad_fem_r.activation',
'quad_fem_r.fiber_length', 'gem_r.activation', 'gem_r.fiber_length', 'peri_r.activation', 'peri_r.fiber_length',
'rect_fem_r.activation', 'rect_fem_r.fiber_length', 'vas_med_r.activation', 'vas_med_r.fiber_length',
'vas_int_r.activation', 'vas_int_r.fiber_length', 'vas_lat_r.activation', 'vas_lat_r.fiber_length',
'med_gas_r.activation', 'med_gas_r.fiber_length', 'lat_gas_r.activation', 'lat_gas_r.fiber_length', 'soleus_r.activation',
'soleus_r.fiber_length', 'tib_post_r.activation', 'tib_post_r.fiber_length', 'flex_dig_r.activation',
 'flex_dig_r.fiber_length', 'flex_hal_r.activation', 'flex_hal_r.fiber_length', 'tib_ant_r.activation',
 'tib_ant_r.fiber_length', 'per_brev_r.activation', 'per_brev_r.fiber_length', 'per_long_r.activation',
 'per_long_r.fiber_length', 'per_tert_r.activation', 'per_tert_r.fiber_length', 'ext_dig_r.activation', 'ext_dig_r.fiber_length',
 'ext_hal_r.activation', 'ext_hal_r.fiber_length', 'glut_med1_l.activation', 'glut_med1_l.fiber_length', 'glut_med2_l.activation',
 'glut_med2_l.fiber_length', 'glut_med3_l.activation', 'glut_med3_l.fiber_length', 'glut_min1_l.activation', 'glut_min1_l.fiber_length',
'glut_min2_l.activation', 'glut_min2_l.fiber_length', 'glut_min3_l.activation', 'glut_min3_l.fiber_length', 'semimem_l.activation',
'semimem_l.fiber_length', 'semiten_l.activation', 'semiten_l.fiber_length', 'bifemlh_l.activation', 'bifemlh_l.fiber_length',
'bifemsh_l.activation', 'bifemsh_l.fiber_length', 'sar_l.activation', 'sar_l.fiber_length', 'add_long_l.activation',
'add_long_l.fiber_length', 'add_brev_l.activation', 'add_brev_l.fiber_length', 'add_mag1_l.activation', 'add_mag1_l.fiber_length',
'add_mag2_l.activation', 'add_mag2_l.fiber_length', 'add_mag3_l.activation', 'add_mag3_l.fiber_length', 'tfl_l.activation',
'tfl_l.fiber_length', 'pect_l.activation', 'pect_l.fiber_length', 'grac_l.activation', 'grac_l.fiber_length', 'glut_max1_l.activation',
'glut_max1_l.fiber_length', 'glut_max2_l.activation', 'glut_max2_l.fiber_length', 'glut_max3_l.activation', 'glut_max3_l.fiber_length',
'iliacus_l.activation', 'iliacus_l.fiber_length', 'psoas_l.activation', 'psoas_l.fiber_length', 'quad_fem_l.activation',
'quad_fem_l.fiber_length', 'gem_l.activation', 'gem_l.fiber_length', 'peri_l.activation', 'peri_l.fiber_length', 'rect_fem_l.activation',
'rect_fem_l.fiber_length', 'vas_med_l.activation', 'vas_med_l.fiber_length', 'vas_int_l.activation', 'vas_int_l.fiber_length',
'vas_lat_l.activation', 'vas_lat_l.fiber_length', 'med_gas_l.activation', 'med_gas_l.fiber_length', 'lat_gas_l.activation',
'lat_gas_l.fiber_length', 'soleus_l.activation', 'soleus_l.fiber_length', 'tib_post_l.activation', 'tib_post_l.fiber_length',
'flex_dig_l.activation', 'flex_dig_l.fiber_length', 'flex_hal_l.activation', 'flex_hal_l.fiber_length', 'tib_ant_l.activation',
'tib_ant_l.fiber_length', 'per_brev_l.activation', 'per_brev_l.fiber_length', 'per_long_l.activation', 'per_long_l.fiber_length',
'per_tert_l.activation', 'per_tert_l.fiber_length', 'ext_dig_l.activation', 'ext_dig_l.fiber_length', 'ext_hal_l.activation',
'ext_hal_l.fiber_length', 'ercspn_r.activation', 'ercspn_r.fiber_length', 'ercspn_l.activation', 'ercspn_l.fiber_length',
'intobl_r.activation', 'intobl_r.fiber_length', 'intobl_l.activation', 'intobl_l.fiber_length', 'extobl_r.activation',
'extobl_r.fiber_length', 'extobl_l.activation', 'extobl_l.fiber_length']



'''

motFileHeader_to_stateVariableName_dict = {"pelvis_tx": "ground_pelvis/pelvis_tx/value",
                                           "pelvis_ty": "ground_pelvis/pelvis_ty/value",
                                           "pelvis_tz": "ground_pelvis/pelvis_tz/value",
                                           "pelvis_tilt": "ground_pelvis/pelvis_tilt/value",
                                           "pelvis_list": "ground_pelvis/pelvis_list/value",
                                           "pelvis_rotation": "ground_pelvis/pelvis_rotation/value",
                                           "pelvis_tilt_u":"ground_pelvis/pelvis_tilt/speed",
                                           "pelvis_list_u":"ground_pelvis/pelvis_list/speed",
                                           "pelvis_rotation_u":"ground_pelvis/pelvis_rotation/speed",
                                           "pelvis_tx_u":"ground_pelvis/pelvis_tx/speed",
                                           "pelvis_ty_u":"ground_pelvis/pelvis_ty/speed",
                                           "pelvis_tz_u":"ground_pelvis/pelvis_tz/speed",



                                           "hip_flexion_r": "hip_r/hip_flexion_r/value",
                                           "hip_adduction_r": "hip_r/hip_adduction_r/value",
                                           "hip_rotation_r": "hip_r/hip_rotation_r/value",
                                           "hip_flexion_l": "hip_l/hip_flexion_l/value",
                                           "hip_adduction_l": "hip_l/hip_adduction_l/value",
                                           "hip_rotation_l": "hip_l/hip_rotation_l/value",
                                           "hip_flexion_r_u": "hip_r/hip_flexion_r/speed",
                                           "hip_adduction_r_u": "hip_r/hip_adduction_r/speed",
                                           "hip_rotation_r_u": "hip_r/hip_rotation_r/speed",
                                           "hip_flexion_l_u": "hip_l/hip_flexion_l/speed",
                                           "hip_adduction_l_u": "hip_l/hip_adduction_l/speed",
                                           "hip_rotation_l_u": "hip_l/hip_rotation_l/speed",



                                           "knee_angle_r": "knee_r/knee_angle_r/value",
                                           "ankle_angle_r": "ankle_r/ankle_angle_r/value",
                                           "ankle_angle_r_u": "ankle_r/ankle_angle_r/speed",
                                           "knee_angle_r_u": "knee_r/knee_angle_r/speed",

                                           "knee_angle_l": "knee_l/knee_angle_l/value",
                                           "ankle_angle_l": "ankle_l/ankle_angle_l/value",
                                           "knee_angle_l_u": "knee_l/knee_angle_l/speed",
                                           "ankle_angle_l_u": "ankle_l/ankle_angle_l/speed",


                                           "lumbar_extension": "back/lumbar_extension/value",
                                           "lumbar_extension_u":"back/lumbar_extension/speed",

                                           "bifemsh_r.activation":"bifemsh_r/activation",
                                           "bifemsh_r.fiber_length":"bifemsh_r/fiber_length",


                                           "rect_fem_r.activation":"rect_fem_r/activation",
                                           "rect_fem_r.fiber_length":"rect_fem_r/fiber_length",

                                           "vas_int_r.activation":"vasti_r/activation",
                                           "vas_int_r.fiber_length":"vasti_r/fiber_length",

                                           "bifemsh_l.activation":"bifemsh_l/activation",
                                           "bifemsh_l.fiber_length":"bifemsh_l/fiber_length",

                                           "glut_max1_l.activation":"glut_max_l/activation",
                                           "glut_max1_l.fiber_length":"glut_max_l/fiber_length",

                                           "rect_fem_l.activation":"rect_fem_l/activation",
                                           "rect_fem_l.fiber_length":"rect_fem_l/fiber_length",

                                           "vas_int_l.activation" :"vasti_l/activation",
                                           "vas_int_l.fiber_length":"vasti_l/fiber_length",


                                           "soleus_l.activation":"soleus_l/activation",
                                           "soleus_l.fiber_length":"soleus_l/fiber_length",

                                           "tib_ant_l.activation":"tib_ant_l/activation",
                                           "tib_ant_l.fiber_length":"tib_ant_l/fiber_length"

                                           }
def ValuetoKey(value):
      keys =[*motFileHeader_to_stateVariableName_dict.keys()]
      key  = keys[[*motFileHeader_to_stateVariableName_dict.values()].index(value)]

      return key


model = env.osim_model.model
# ipdb.set_trace()

num =model.getStateVariableNames().getSize()

state_variable_names =[]   ## coordinates in terms of opensim
for i in range(num):
      state_variable_names.append(model.getStateVariableNames().get(i))
# print(model_parameters)
# print (state_variable_names)
# ipdb.set_trace()
# sto_parameter =[]
# for i in ((model_parameters)):
      # print(i)
      # sto_parameter.append(modelVariableName(i))
index_list=[]
header_dict_values = [*motFileHeader_to_stateVariableName_dict.values()]

for i in coord:
      if i not in header_dict_values:
            print (i)
            continue
      key = ValuetoKey(i)  #find name of the statevariablename in header

      index_list.append(headers.index(key))   #find position in header

print (index_list)
print(len(index_list))




# printSimArray(model.getStateVariableNames([0]*patameters))


# ipdb.set_trace()

# def reorder (arr,index_list):



count=0

for line in f.readlines():
      print(line)
      count+=1
      value =[float(x) for x in line.split()]
      time = value[0]
      data = value[1:]
      for i in range(len(data)):
            data_order= data[:]
            for index in range(len(index_list)):
                  data_order[index] = data[i]


            env.osim_model.model.setStateVariableValue(state, data_order[i],headers[i])


print(count)

# def toRadian(angle):
#       return 3.14 * angle/180



