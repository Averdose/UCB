import random

_SPOTS_ = [str(n) for n in range(2, 11)]
_FACES_ = ['J', 'Q', 'K']
_ACE_ = 'A'

_CARDS_ = _SPOTS_ + _FACES_ + [_ACE_]


def play_episode(policy, seed=None):
    if seed:
        random.seed(seed)

    episode = []

    # initialize cards
    player_cards = random.choices(_CARDS_, k=2)
    dealer_cards = random.choices(_CARDS_, k=2)

    player_cards_value = _get_cards_value(player_cards)
    dealer_cards_value = _get_cards_value(dealer_cards)

    # check for blackjack (natural)
    if player_cards_value == 21:
        return episode

    # check for draw from first cards
    if player_cards_value > 21 and dealer_cards_value > 21:
        return episode

    player_state = _get_player_state(player_cards, dealer_cards)
    player_turn = 1

    while player_turn:
        if player_cards_value < 12 or policy(player_state):
            new_card = random.choice(_CARDS_)
            player_cards.append(new_card)

            player_cards_value = _get_cards_value(player_cards)
            if player_cards_value <= 21:
                episode.append((player_state, 'HIT', 0))
                player_state = _get_player_state(player_cards, dealer_cards)
            else:
                player_turn = 0

        else:
            player_turn = 0

    if player_cards_value > 21:
        episode.append((player_state, 'HIT', -1))
        return episode

    while dealer_cards_value < 17:
        new_card = random.choice(_CARDS_)
        dealer_cards.append(new_card)
        dealer_cards_value = _get_cards_value(dealer_cards)

    if dealer_cards_value > 21 or dealer_cards_value < player_cards_value:
        episode.append((player_state, 'STAND', 1))
    elif dealer_cards_value == player_cards_value:
        episode.append((player_state, 'STAND', 0))
    else:
        episode.append((player_state, 'STAND', -1))
    return episode


def _get_cards_value(cards):
    cards_value = sum([_get_card_value(card) for card in cards])
    if _ACE_ in cards and cards_value < 12:
        cards_value += 10
    return cards_value


def _get_card_value(card):
    if card == _ACE_:
        return 1
    if card in _FACES_:
        return 10
    return int(card)


def _get_player_state(player_cards, dealer_cards):
    player_cards_value = sum([_get_card_value(card) for card in player_cards])
    upcard_value = _get_card_value(dealer_cards[0])
    usable_ace = False

    if _ACE_ in player_cards and player_cards_value < 12:
        player_cards_value, usable_ace = player_cards_value + 10, True
    return player_cards_value, upcard_value, usable_ace

