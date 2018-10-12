import robo_rl.common.utils.nn_utils as nn_utils
import torch
import torch.nn.functional as torchfunc
from osim.env import ProstheticsEnv
from robo_rl.common.networks.linear_network import LinearNetwork

env = ProstheticsEnv(visualize=False)
observation = env.reset()

print("MUSCLE SET")
muscleSet = env.osim_model.muscleSet
for i in range(muscleSet.getSize()):
    print(i, ":\"" + muscleSet.get(i).getName() + "\",")

# med - medial(towards the middle), lat - lateral(away from the middle)
muscle_dict = {"add_brev_r": 1, "bifemsh_r": 3, "glut_max1_r": 4, "psoas_r": 5,
               "rect_fem_r": 6, "vas_lat_r": 7, "add_brev_l": 9, "bifemsh_l": 11, "glut_max1_l": 12,
               "psoas_l": 13, "rect_fem_l": 14, "vas_lat_l": 15, "med_gas_l": 16, "soleus_l": 17,
               "tib_ant_l": 18}

# semimem - one of hamstring
muscle_dict_2 = {"semimem_r": 2, "bflh_r": 3, "glmax1_r": 4,
                 "recfem_r": 6, "vaslat_r": 7, "semimem_l": 10, "bflh_l": 11, "glmax1_l": 12,
                 "recfem_l": 14, "vaslat_l": 15, "gasmed_l": 16, "soleus_l": 17,
                 "tibant_l": 18}

header_indices = [10, 13, 20, 24, 28, 31, 53, 56, 63, 67, 71, 74, 75, 77, 81]
header_indices_right = [1, 4, 10, 11]
header_indices_left = [1, 4, 10, 11, 13, 14, 15]

right_leg = open("../../data/Run_20002_EMG_RAW_right.sto")
left_leg = open("../../data/Run_20002_EMG_RAW_left.sto")

right_leg_headers = right_leg.readline().split()
left_leg_headers = left_leg.readline().split()

right_leg_values = []
left_leg_values = []

# for i in range(len(headers)):
# 	print(i,headers[i])

for line in right_leg.readlines():
    values = [float(x) for x in line.split()]
    right_leg_values.append(values)

for line in left_leg.readlines():
    values = [float(x) for x in line.split()]
    left_leg_values.append(values)

data_length = len(right_leg_values)

linear_network = LinearNetwork(layers_size=[1, 100, 10, 1, 10, 100, 1], is_dropout=True)
linear_network.apply(nn_utils.xavier_initialisation)


def no_activation(x):
    x = torch.abs(x)
    return x/(1+x)


def excitation_transformation(x, i, train=False):
    action = linear_network(torch.Tensor([x]), final_layer_function=no_activation,
                            activation_function=torch.exp)
    if train:
        linear_network.actions[i].append(action)
    return action.item()


initial_phase = 2000
cycle_delay = int(data_length / 2)


def train(num_iterations):
    linear_network.train()

    best_tr = -100000

    for j in range(num_iterations):
        linear_network.actions = []
        linear_network.rewards = []
        linear_network.zero_grad()

        tr = 0.0
        env.reset()
        for i in range(data_length):
            linear_network.actions.append([])
            action = [0] * 19

            right_leg_index = (i + initial_phase) % data_length
            left_leg_index = (right_leg_index + cycle_delay) % data_length

            for header_index in header_indices_right:
                action[muscle_dict_2[right_leg_headers[header_index]]] = \
                    excitation_transformation(right_leg_values[right_leg_index][header_index], i, True)

            for header_index in header_indices_left:
                action[muscle_dict_2[left_leg_headers[header_index]]] = \
                    excitation_transformation(left_leg_values[left_leg_index][header_index], i, True)

            # print(action)
            o, r, e, d = env.step(action)
            linear_network.rewards.append(r)
            tr += r

            # print(tr)
            if e:
                break
        discount_factor = 0.9
        back_reward = linear_network.rewards[-1]
        episode_len = len(linear_network.rewards)
        discounted_rewards = [0] * episode_len

        if tr > best_tr:
            torch.save(linear_network.state_dict(), 'transform_net_best')
            best_tr = tr

        print(j, tr, episode_len, best_tr)

        for i in range(episode_len - 1):
            discounted_rewards[-i] = back_reward
            back_reward = back_reward * discount_factor + linear_network.rewards[-i - 1]
        discounted_rewards[0] = back_reward

        for i in range(episode_len):
            for action in linear_network.actions[i]:
                r = action * torch.Tensor([discounted_rewards[i]])
                # print(r, action)
                r.backward()
                torch.nn.utils.clip_grad_norm_(linear_network.parameters(), 100)
                # print(linear_network.linear_layers[0].weight.grad.data)
                for param in linear_network.parameters():
                    param.data.add_(0.00001 * param.grad.data)

    torch.save(linear_network.state_dict(), 'transform_net')


def test():
    linear_network.load_state_dict(torch.load('transform_net_best'))
    linear_network.eval()

    tr = 0.0
    for i in range(data_length):
        action = [0] * 19

        right_leg_index = (i + initial_phase) % data_length
        left_leg_index = (right_leg_index + cycle_delay) % data_length

        for header_index in header_indices_right:
            action[muscle_dict_2[right_leg_headers[header_index]]] = \
                excitation_transformation(right_leg_values[right_leg_index][header_index], i)

        for header_index in header_indices_left:
            action[muscle_dict_2[left_leg_headers[header_index]]] = \
                excitation_transformation(left_leg_values[left_leg_index][header_index], i)

        # print(action)
        o, r, e, d = env.step(action)
        tr += r

        # print(tr)
        if e:
            break
    print(tr)


train(1000)
# test()
