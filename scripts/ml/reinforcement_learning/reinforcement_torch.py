import time
from collections import deque, namedtuple

import PIL.Image
import gym
import torch
import torch.nn as nn
import torch.optim as optim
from pyvirtualdisplay import Display
import numpy as np

import utils_torch

Display(visible=0, size=(840, 480)).start()

torch.manual_seed(utils_torch.SEED)

MEMORY_SIZE = 100_000
GAMMA = 0.995
ALPHA = 1e-3
NUM_STEPS_FOR_UPDATE = 4

env = gym.make("LunarLander-v2")

env.reset()
PIL.Image.fromarray(env.render(mode="rgb_array"))

state_size = env.observation_space.shape[0]
num_actions = env.action_space.n

print("State Shape:", state_size)
print("Number of actions:", num_actions)

current_state = env.reset()

action = 0

next_state, reward, done, _ = env.step(action)

utils_torch.display_table(current_state, action, next_state, reward, done)

current_state = next_state


class QNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


q_network = QNetwork(state_size, num_actions)
target_q_network = QNetwork(state_size, num_actions)
optimizer = optim.Adam(q_network.parameters(), lr=ALPHA)

from public_tests import *

test_network(q_network)
test_network(target_q_network)
test_optimizer(optimizer, ALPHA)

experience = namedtuple(
    "Experience", field_names=["state", "action", "reward", "next_state", "done"]
)


def compute_loss(experiences, gamma, q_network, target_q_network):
    states, actions, rewards, next_states, done_vals = experiences

    states = torch.tensor(states, dtype=torch.float32)
    actions = torch.tensor(actions, dtype=torch.long)
    rewards = torch.tensor(rewards, dtype=torch.float32)
    next_states = torch.tensor(next_states, dtype=torch.float32)
    done_vals = torch.tensor(done_vals, dtype=torch.float32)

    max_qsa = target_q_network(next_states).max(dim=1)[0]
    y_targets = rewards + gamma * max_qsa * (1 - done_vals)

    q_values = q_network(states)
    q_values = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)

    loss = nn.MSELoss()(q_values, y_targets)
    return loss


test_compute_loss(compute_loss)


def agent_learn(experiences, gamma):
    optimizer.zero_grad()
    loss = compute_loss(experiences, gamma, q_network, target_q_network)
    loss.backward()
    optimizer.step()
    utils_torch.update_target_network(q_network, target_q_network)


start = time.time()

num_episodes = 2000
max_num_timesteps = 1000

total_point_history = []

num_p_av = 100
epsilon = 1.0

memory_buffer = deque(maxlen=MEMORY_SIZE)

target_q_network.load_state_dict(q_network.state_dict())

for i in range(num_episodes):
    state = env.reset()
    total_points = 0

    for t in range(max_num_timesteps):
        state_qn = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        q_values = q_network(state_qn)
        action = utils_torch.get_action(q_values, epsilon)

        next_state, reward, done, _ = env.step(action)

        memory_buffer.append(experience(state, action, reward, next_state, done))

        update = utils_torch.check_update_conditions(
            t, NUM_STEPS_FOR_UPDATE, memory_buffer
        )

        if update:
            experiences = utils_torch.get_experiences(memory_buffer)
            agent_learn(experiences, GAMMA)

        state = next_state.copy()
        total_points += reward

        if done:
            break

    total_point_history.append(total_points)
    av_latest_points = np.mean(total_point_history[-num_p_av:])

    epsilon = utils_torch.get_new_eps(epsilon)

    print(
        f"\rEpisode {i + 1} | Total point average of the last {num_p_av} episodes: {av_latest_points:.2f}",
        end="",
    )

    if (i + 1) % num_p_av == 0:
        print(
            f"\rEpisode {i + 1} | Total point average of the last {num_p_av} episodes: {av_latest_points:.2f}"
        )

    if av_latest_points >= 200.0:
        print(f"\n\nEnvironment solved in {i + 1} episodes!")
        torch.save(q_network.state_dict(), "lunar_lander_model.pth")
        break

tot_time = time.time() - start

print(f"\nTotal Runtime: {tot_time:.2f} s ({(tot_time / 60):.2f} min)")

utils_torch.plot_history(total_point_history)

import logging

logging.getLogger().setLevel(logging.ERROR)

filename = "./videos/lunar_lander.mp4"

utils_torch.create_video(filename, env, q_network)
utils_torch.embed_mp4(filename)
