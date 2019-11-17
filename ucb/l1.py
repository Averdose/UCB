#!/usr/bin/env python

import numpy as np


class KArmedBandit(object):
    """
    Implementation of k-armed bandit machine, with result pre-computation.

    """

    def __init__(self, arms, arm_means, sigma=1, max_pulls=1001):
        """
        The constructor for KArmedBandit class

        :param arms: number of arms
        :param arm_means: Numpy vector of mean values for each arm
        :param max_pulls: maximum number of bandit moves
        :param sigma: standard deviation of each arm
        """

        if len(arm_means) != arms:
            raise ValueError("Length of arm means does not equal number of arms")

        self.arms = arms
        self.max_pulls = max_pulls
        self.arm_means = arm_means

        # pre-computed results - based on arm mean and standard deviation
        self.results = np.zeros([self.arms, self.max_pulls])
        for arm_index, arm_mean in enumerate(self.arm_means):
            self.results[arm_index] = np.random.normal(arm_mean, sigma, self.max_pulls)
        # vector containing state of each arm (number of times each arm has been selected so far)
        self.arm_state = np.zeros(self.arms, dtype=np.int16)

    def get_result(self, arm_index):
        arm_state = self.arm_state[arm_index]
        self.arm_state[arm_index] = arm_state + 1
        return self.results[arm_index][arm_state]

    def reset(self):
        self.arm_state = np.zeros(self.arms, dtype=np.int16)

    def get_optimal_rewards(self):
        arm_states = np.zeros(self.arms, dtype=np.int16)
        arm_pulls = np.zeros(self.max_pulls, dtype=np.int16)

        reward = 0
        rewards = np.zeros(self.max_pulls)

        for pull_index in range(self.max_pulls):
            best_arm = 0
            best_value = self.results[best_arm][arm_states[best_arm]]

            for arm_index, arm_state in enumerate(arm_states):
                if best_value < self.results[arm_index][arm_state]:
                    best_value = self.results[arm_index][arm_state]
                    best_arm = arm_index

            arm_states[best_arm] = arm_states[best_arm] + 1
            arm_pulls[pull_index] = best_arm

            reward += best_value
            rewards[pull_index] = reward

        return arm_pulls, rewards


def compute_ucb(bandit, ucb_const):
    """

    :param arms:
    :param gen_arm_means:
    :param sigma:
    :param max_pulls:
    :param ucb_const:
    :return:
    """

    def select_next_action(arm_estimates, arm_pulls, pull_index):
        max_ucb_value = -np.inf
        max_ucb_arm = 0

        ln_t = np.log(pull_index + 1)

        for arm_index, arm_estimate in enumerate(arm_estimates):
            if arm_pulls[arm_index] == 0:
                return arm_index
            ucb_value = arm_estimate + ucb_const * np.sqrt(ln_t / arm_pulls[arm_index])
            if ucb_value > max_ucb_value:
                max_ucb_value = ucb_value
                max_ucb_arm = arm_index
        return max_ucb_arm

    estimates = np.zeros(bandit.arms)
    pulls = np.zeros(bandit.arms)
    cum_reward = 0
    rewards = np.zeros(bandit.max_pulls)

    for pull_index in range(bandit.max_pulls):
        arm_index = select_next_action(estimates, pulls, pull_index)
        reward = bandit.get_result(arm_index)

        cum_reward = reward + cum_reward
        rewards[pull_index] = cum_reward

        pulls[arm_index] += 1
        estimates[arm_index] += (reward - estimates[arm_index]) / pulls[arm_index]

    bandit.reset()

    return pulls, rewards


if __name__ == '__main__':
    k = 10
    t = 1000
    mu = 2
    sigma = 1

    means = np.random.normal(mu, sigma, k)

    bandit = KArmedBandit(arms=k, arm_means=means, max_pulls=t, sigma=sigma)
    arm_pulls, arm_rewards = compute_ucb(bandit, ucb_const=2)
    best_pulls, best_rewards = bandit.get_optimal_rewards()

    print("Arm means: {}".format(bandit.arm_means))
    print("UCB pulls: {}".format(arm_pulls))
    print("UCB rewards: {}".format(arm_rewards))
    print("Best pulls: {}".format(best_pulls))
    print("Best rewards: {}".format(best_rewards))
    print(arm_rewards / best_rewards)
