#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from blackjack.monte_carlo import first_visit_predict
from blackjack.plots import plot_expected_returns

num_episodes = 100000

# policy from https://en.wikipedia.org/wiki/Blackjack#Basic_strategy
def policy(state):
    player_cards_value, upcard_value, usable_ace = state
    if not usable_ace: #hard
        if player_cards_value >= 17:
            return False
        if player_cards_value >= 13:
            return (upcard_value > 6)
        if player_cards_value == 12:
            return (upcard_value < 4 or upcard_value > 6)
        return True
    else:
        if player_cards_value >= 9:
            return False
        if player_cards_value == 8:
            return (upcard_value > 8)
        return True

values = first_visit_predict(policy, num_episodes)
plot_expected_returns(values, 'result_wikipedia_policy.png')
