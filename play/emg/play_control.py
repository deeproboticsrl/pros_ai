from osim.env import ProstheticsEnv
import time

env = ProstheticsEnv(visualize=True)
observation = env.reset()

# class CMCEnv(OsimEnv):
# 	time_limit = 300

# 	def __init__(self, visualize = True, integrator_accuracy = 5e-5):
# 		self.model_path = "/home/joy/zReinforcementLearning/prosthetic-ai/RunningSimulation_simTK/FullBodyModel_Hamner2010_v2_0.osim"
# 		super().__init__(visualize = visualize, integrator_accuracy = integrator_accuracy)

# 	def is_done(self):
# 		state_desc = self.get_state_desc()
# 		return state_desc["body_pos"]["pelvis"][1] < 0.6

# 	def reward(self):
# 		state_desc = self.get_state_desc()
# 		prev_state_desc = self.get_prev_state_desc()
# 		if not prev_state_desc:
# 			return 0
# 		return 9.0 - (state_desc["body_vel"]["pelvis"][0] - 3.0)**2

# env= CMCEnv()
# env.reset()

print("MUSCLE SET")
muscleSet = env.osim_model.muscleSet
for i in range(muscleSet.getSize()):
			print(i,":\""+muscleSet.get(i).getName()+"\",")


# print("JOINT SET")
# jointSet = env.osim_model.model.getStateVariableNames()
# for i in range(jointSet.getSize()):
# 			print(i,jointSet.get(i))

# med - medial(towards the middle), lat - lateral(away from the middle)
muscle_dict = {"add_brev_r":1,"bifemsh_r":3,"glut_max1_r":4,"psoas_r":5
,"rect_fem_r":6,"vas_lat_r":7,"add_brev_l":9,"bifemsh_l":11,"glut_max1_l":12,
"psoas_l":13,"rect_fem_l":14,"vas_lat_l":15,"med_gas_l":16,"soleus_l":17,
"tib_ant_l":18}

# header_indices = [10,13,20,24,28,31,53,56,63,67,71,74,75,77,81]
header_indices = [10,13,20,24,28,31,53,56,63,67,71,74,75,77,81]


tr=0.0
with open("subject01_Run_20002_cycle1_controls.sto") as f:
	headers = f.readline().split()
	count = 0
	# for i in range(len(headers)):
	# 	print(i,headers[i])
	for line in f.readlines():
		values = [float(x) for x in line.split()]
		action = env.action_space.sample() * 0
		# for i in range(len(action)):
		# 	## first value is time
		# 	action[i] = values[i+1]
		for header_index in header_indices:
			action[muscle_dict[headers[header_index]]] = values[header_index]*10
		# print(action)
		o,r,e,d = env.step(action)

		tr+=r
		# print(tr)
		if(e):
			break
print(tr)
