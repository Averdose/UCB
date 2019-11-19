#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from blackjack.monte_carlo import first_visit_predict
from blackjack.plots import plot_expected_returns

num_episodes = 100000

policy = lambda state: True if state[0] < 20 else False

values = first_visit_predict(policy, num_episodes)
plot_expected_returns(values, 'result_get_if_below_20.png')
