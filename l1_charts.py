#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from l1 import KArmedBandit, compute_ucb


def create_chart(arms, means, sigma, max_pulls, ucb_consts):
    bandit = KArmedBandit(arms, means, sigma, max_pulls)
    best_pulls, best_rewards = bandit.get_optimal_rewards()

    steps = np.arange(1, max_pulls)
    rewards = pd.DataFrame({'t': steps})
    rewards['greedy'] = best_rewards[1:] / steps
    plt.plot('t', 'greedy', data=rewards, color='red', linewidth=4)

    cmap = plt.get_cmap('viridis')
    colors = cmap(np.linspace(0, 1, len(ucb_consts)))

    for ucb_index, ucb_const in enumerate(ucb_consts):
        arm_pulls, arm_rewards = compute_ucb(bandit, ucb_const)
        column_name = "c = {}".format(ucb_const)
        rewards[column_name] = arm_rewards[1:] / steps

    for ucb_index, ucb_const in enumerate(ucb_consts):
        column_name = "c = {}".format(ucb_const)
        plt.plot('t', column_name, data=rewards, color=colors[ucb_index], linewidth=2)

    plt.legend()
    plt.show()


if __name__ == '__main__':
    k = 10
    mu = 2
    sigma = 1
    t = 501
    eps = 0.001

    means = np.random.normal(mu, sigma, k)
    c = np.arange(-6, 6 + eps, 2)

    create_chart(k, means, sigma, t, c)
