from .blackjack import play_episode


def first_visit_predict(policy, num_episodes, gamma=1):
    all_states = [(player_value, upcard_value, usable_ace)
                  for player_value in range(12, 21 + 1)
                  for upcard_value in range(1, 10 + 1)
                  for usable_ace in [True, False]]

    returns = dict.fromkeys(all_states, 0)
    counts = dict.fromkeys(all_states, 0.0)
    values = dict.fromkeys(all_states, 0.0)

    for episode_index in range(num_episodes):
        episode = play_episode(policy)
        first_state_occurrences = {}

        for task_index, task in enumerate(episode):
            state = task[0]

            if state in all_states and state not in first_state_occurrences:
                first_state_occurrences[state] = task_index

                returns[state] += sum([
                    reward * gamma ** i
                    for i, (_, _, reward)
                    in enumerate(episode[task_index:])]
                )
                counts[state] += 1.0
                values[state] = returns[state] / counts[state]

    return values

def policy_update(policy, num_episodes, gamma=1):
    all_states = [(player_value, upcard_value, usable_ace)
                  for player_value in range(12, 21 + 1)
                  for upcard_value in range(1, 10 + 1)
                  for usable_ace in [True, False]]

    returns = dict.fromkeys(all_states, 0)
    counts = dict.fromkeys(all_states, 0.0)
    values = dict.fromkeys(all_states, 0.0)

    for episode_index in range(num_episodes):
        episode = play_episode(policy)
        first_state_occurrences = {}

        for task_index, task in enumerate(episode):
            state = task[0]

            if state in all_states and state not in first_state_occurrences:
                first_state_occurrences[state] = task_index

                returns[state] += sum([
                    reward * gamma ** i
                    for i, (_, _, reward)
                    in enumerate(episode[task_index:])]
                )
                counts[state] += 1.0
                values[state] = returns[state] / counts[state]
        policy.update(episode, values)

    return values
