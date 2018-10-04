from osim.env import OsimModel
from pros_ai.play.motion.motion_utils import print_sim_array
import copy


class MotionGenEnv(OsimModel):

    def __init__(self, model_path, visualize):
        super().__init__(model_path, visualize)
        self.reset()

    def integrate(self, endtime=None):
        # Define the new endtime of the simulation
        self.istep = self.istep + 1
        # Integrate till the new endtime
        try:
            if endtime is None:
                endtime = self.stepsize * self.istep
            self.state = self.manager.integrate(endtime)
        except Exception as e:
            print(e)

    def print_state_variables(self):
        # Print all state variables in the model

        print("STATE VARIABLES")
        print_sim_array(self.model.getStateVariableNames())

        print("STATE VARIABLE VALUES Length -- ", self.model.getNumStateVariables())
        print(self.model.getStateVariableValues(self.state))

    def get_relative_observations(self):
        body_observations = {}
        observation = self.get_state_desc()
        pelvis_observation = {}

        body_keys = ["body_pos", "body_vel", "body_acc", "body_pos_rot", "body_vel_rot", "body_acc_rot"]
        for key in body_keys:
            pelvis_observation[key] = copy.deepcopy(observation[key]["pelvis"])

        for key in body_keys:
            body_observations[key] = {}
            for body_part in ["pelvis", "head", "torso", "toes_l", "tibia_l", "talus_l", "pros_tibia_r", "pros_foot_r",
                              "femur_l", "femur_r", "calcn_l"]:
                body_observations[key][body_part] = [0.0]*3
                for i in range(2):
                    body_observations[key][body_part][i] = observation[key][body_part][i] - pelvis_observation[key][i]

        body_observations["misc"] = copy.deepcopy(observation["misc"])
        return body_observations
