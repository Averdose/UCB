#!/usr/bin/env python

import numpy as np

class bandits(object):
    def __init__(self, k, mu = 0, sigma = 1, t = 1001):
        # FIXME
        self.hand = np.random.normal(mu, sigma, k)
        # precompute
        self.results = np.zeros([k, t])
        for hi, h in enumerate(self.hand):
            self.results[hi] = np.random.normal(h, sigma, t)
        self.results_iter = np.zeros(k, dtype=np.int16)

    def getPrecomputedResult(self, i):
        it = self.results_iter[i]
        self.results_iter[i] = it + 1
        return self.results[i][it]

    def getResult(self, i):
        return np.random.normal(self.hand[i], 1)

def getUCB(Q, N, t, c = 2):
    max_val = float('-Inf')
    max_a = 0
    lg_t = np.log(t)
    for a, q in enumerate(Q):
        if N[a] == 0:
            return a
        val = q + c*np.sqrt(lg_t / N[a])
        if val > max_val:
            max_val = val
            max_a = a
    return max_a

k = 10
bandit = bandits(k)
Q = np.zeros(k)
N = np.zeros(k)

for i in range(1, 1000):
    A = getUCB(Q, N, i)
    R = bandit.getPrecomputedResult(A)
    N[A] = N[A] + 1
    Q[A] = Q[A] + (1/N[A])*(R-Q[A])

print(bandit.hand)
print(N)
print(Q)
