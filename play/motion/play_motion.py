import numpy as np
import opensim

integrator_accuracy = 3e-3
stepsize = 0.017
model = opensim.Model('../models/gait14dof22musc_pros_20180507.osim')

# initialise model's simbody System object. System is a computational representation of the Model
model.initSystem()
# initialise the ModelVisualizer object
model.setUseVisualizer(True)

'''
Defines controller for controlling actuators. A controller computes and sets the values of the controls for the actuators under its control
PrescribedController specifies functions that prescribe the control values of its actuators as a function of time. 
So we will explicitly provide these functions.
'''
brain = opensim.PrescribedController()

##################################################################
# Print all components of the model

muscleSet = model.getMuscles()
forceSet = model.getForceSet()
bodySet = model.getBodySet()
jointSet = model.getJointSet()
markerSet = model.getMarkerSet()
contactGeometrySet = model.getContactGeometrySet()

print("JOINTS")
for i in range(jointSet.getSize()):
    print(i, jointSet.get(i).getName())
print("\nBODIES")
for i in range(bodySet.getSize()):
    print(i, bodySet.get(i).getName())
print("\nMUSCLES")
for i in range(muscleSet.getSize()):
    print(i, muscleSet.get(i).getName())
print("\nFORCES")
for i in range(forceSet.getSize()):
    print(i, forceSet.get(i).getName())

##################################################################

### set constant control on all muscles        
for j in range(muscleSet.getSize()):
    func = opensim.Constant(1.0)
    brain.addActuator(muscleSet.get(j))
    brain.prescribeControlForActuator(j, func)

model.addController(brain)
model.initSystem()

########### System initialised
# time.sleep(3)

initial_state = model.initializeState()
initial_state.setTime(0)
istep = 0
manager = opensim.Manager(model)
state = initial_state


def reset_manager():
    manager.setIntegratorAccuracy(integrator_accuracy)
    manager.initialize(initial_state)


def reset():
    istep = 0
    reset_manager()


reset()


def integrate(endtime=None):
    global istep, state
    # Define the new endtime of the simulation
    istep = istep + 1

    # Integrate till the new endtime
    try:
        if (endtime == None):
            endtime = stepsize * istep
        state = manager.integrate(endtime)
    except Exception as e:
        print(e)


def actuate(action):
    if np.any(np.isnan(action)):
        raise ValueError("NaN passed in the activation vector. Values in [0,1] interval are required.")

    brain = opensim.PrescribedController.safeDownCast(model.getControllerSet().get(0))
    functionSet = brain.get_ControlFunctions()

    for j in range(functionSet.getSize()):
        func = opensim.Constant.safeDownCast(functionSet.get(j))
        func.setValue(float(action[j]))


# action = [1.0] * muscleSet.getSize()
# actuate(action)
# for i in range(1):
# 	model.setStateVariableValue(state,"ground_pelvis/pelvis_tx/value",0.2*i)
# 	model.assemble(state)
# 	integrate()
# 	print(model.getStateVariableValue(state,"ground_pelvis/pelvis_tx/value"))
# time.sleep(1)
# time.sleep(3)

def printSimArray(array):
    for i in range(array.getSize()):
        print(array.get(i))

    #### Print all state variables in the model


print("STATE VARIABLES")
printSimArray(model.getStateVariableNames())

print("STATE VARIABLE VALUES... Length -- ", model.getNumStateVariables())
print(model.getStateVariableValues(state))

####################################################################################

## Dictionary containing mapping from .mot file headers to state variable names of osim
motFileHeader_to_stateVariableName_dict = {"pelvis_tx": "ground_pelvis/pelvis_tx/value",
                                           "pelvis_ty": "ground_pelvis/pelvis_ty/value",
                                           "pelvis_tz": "ground_pelvis/pelvis_tz/value",
                                           "pelvis_tilt": "ground_pelvis/pelvis_tilt/value",
                                           "pelvis_list": "ground_pelvis/pelvis_list/value",
                                           "pelvis_rotation": "ground_pelvis/pelvis_rotation/value",
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
                                           "lumbar_extension": "back/lumbar_extension/value"}


def getStateVariableName(motHeader):
    return motFileHeader_to_stateVariableName_dict[motHeader]


motHeader_distance_indices = [1, 2, 3]
motHeader_angle_indices = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]


def toRadian(angle):
    return angle / 180 * 3.14


####################################################################################

## Simulate values from the mot file
with open("subject02_running_arms_ik.mot") as f:
    headers = f.readline().split()
    count = 0
    for line in f.readlines():
        # convert strings to floats
        values = [float(x) for x in line.split()]
        for motHeader_index in motHeader_distance_indices:
            model.setStateVariableValue(state, getStateVariableName(headers[motHeader_index]), values[motHeader_index])
        for motHeader_index in motHeader_angle_indices:
            model.setStateVariableValue(state, getStateVariableName(headers[motHeader_index]),
                                        toRadian(values[motHeader_index]))
        model.assemble(state)
        integrate(values[0])

####################################################################################
