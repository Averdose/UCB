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
        self.all_states = [(player_value, upcard_value, usable_ace)
                      for player_value in range(12, 21 + 1)
                      for upcard_value in range(1, 10 + 1)
                      for usable_ace in [True, False]]
        self.policy = dict.fromkeys(self.all_states, True)
        for key, _ in self.policy.items():
            self.policy[key] = random()

    def __call__(self, state):
        return self.policy[state] > 0.5 # 'True == HIT'

    def update(self, episode):
        delta = 0.1
        for (state, action, result) in episode:
            if state not in self.all_states:
                continue
            if action == 'HIT':
                self.policy[state] += delta*result
            elif action == 'STAND':
                self.policy[state] -= delta*result

values = policy_update(epsilon_soft(), num_episodes)
plot_expected_returns(values, 'iterative_policy.png')
