import time

from osim.env import OsimModel
from pros_ai.play.motion.motion_utils import print_sim_array


class MotionGenEnv(OsimModel):

    def __init__(self, model_path, visualize):
        super().__init__(model_path, visualize)
        self.reset()
        # Dictionary containing mapping from .sto file headers to state variable names of osim env
        self.motFileHeader_to_stateVariableName_dict = {"pelvis_tilt": "ground_pelvis/pelvis_tilt/value",
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
        self.model_display_hints = self.model.updDisplayHints()
        self.is_visualizing = visualize

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

    def get_state_variable_name(self, mot_header):
        return self.motFileHeader_to_stateVariableName_dict[mot_header]

    def set_visualisation(self, visualize):
        self.model_display_hints.set_show_wrap_geometry(visualize)
        self.model_display_hints.set_show_contact_geometry(visualize)
        self.model_display_hints.set_show_path_geometry(visualize)
        self.model_display_hints.set_show_path_points(visualize)
        self.model_display_hints.set_show_markers(visualize)
        self.model_display_hints.set_show_forces(visualize)
        self.model_display_hints.set_show_frames(visualize)
        self.model_display_hints.set_show_labels(visualize)
        self.model_display_hints.set_show_debug_geometry(visualize)

    def sleep(self, visualize, sleep_time=2):
        if (self.is_visualizing and not visualize) or (not self.is_visualizing and visualize):
            # transition in visualisation
            print(f"Visualisation transition. {self.is_visualizing} -> {visualize} Sleeping for {sleep_time} seconds")
            time.sleep(sleep_time)
