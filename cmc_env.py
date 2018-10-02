from osim.env import OsimEnv


class CMCEnv(OsimEnv):
    time_limit = 300

    def __init__(self, visualize=True, integrator_accuracy=5e-5):
        self.model_path = "/home/joy/zReinforcementLearning/prosthetic-ai/RunningSimulation_simTK/FullBodyModel_Hamner2010_v2_0.osim"
        super().__init__(visualize=visualize, integrator_accuracy=integrator_accuracy)

    def is_done(self):
        state_desc = self.get_state_desc()
        return state_desc["body_pos"]["pelvis"][1] < 0.6

    def reward(self):
        state_desc = self.get_state_desc()
        prev_state_desc = self.get_prev_state_desc()
        if not prev_state_desc:
            return 0
        return 9.0 - (state_desc["body_vel"]["pelvis"][0] - 3.0) ** 2


env = CMCEnv()
env.reset()
