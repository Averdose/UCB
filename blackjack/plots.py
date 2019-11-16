import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # for 3D plotting


def plot_expected_returns(values):
    def get_figure(ax, usable_ace):
        player_cards_values = np.arange(12, 22)
        upcard_values = np.arange(1, 11)

        X, Y = np.meshgrid(player_cards_values, upcard_values)
        Z = np.reshape(np.array([
            values[player_cards_value, upcard_value, usable_ace]
            for player_cards_value in player_cards_values
            for upcard_value in upcard_values
        ]), X.shape)

        ax.plot_surface(
            X, Y, Z,
            rstride=1, cstride=1,
            cmap=plt.cm.seismic,
            vmin=-1.0, vmax=1.0
        )

        ax.set_xlabel('Wartość kart gracza')
        ax.set_ylabel('Wartość widocznej karty krupiera')
        ax.set_zlabel('Oczekiwana nagroda')

        ax.view_init(ax.elev, -120)

    fig = plt.figure(figsize=(15, 15))

    ax = fig.add_subplot(211, projection='3d')
    ax.set_title('Z używalnym asem')
    get_figure(ax, usable_ace=True)

    ax = fig.add_subplot(212, projection='3d')
    ax.set_title('Bez używalnego asa')
    get_figure(ax, usable_ace=False)

    plt.show()
