from osim.env import OsimModel
from pros_ai.play.motion.motion_utils import print_sim_array


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

