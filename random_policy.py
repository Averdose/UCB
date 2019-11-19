#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from random import random
from blackjack.monte_carlo import policy_update
from blackjack.plots import plot_expected_returns
from blackjack.policies import BasePolicy

num_episodes = 100000

class epsilon_soft(BasePolicy):
    def __init__(self):
        all_states = [(player_value, upcard_value, usable_ace)
                      for player_value in range(12, 21 + 1)
                      for upcard_value in range(1, 10 + 1)
                      for usable_ace in [True, False]]
        self.policy = dict.fromkeys(all_states, True)
        for key, _ in self.policy.items():
            if random() < 0.5:
                self.policy[key] = False

    def __call__(self, state):
        return self.policy[state]

    def update(self, episode, values):
        pass

values = policy_update(epsilon_soft(), num_episodes)
plot_expected_returns(values, 'random.png')
