#!/usr/bin/env python

import numpy as np

class bandits(object):
    def __init__(self, k, mu = 2, sigma = 1, t = 1001):
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

    def getOptimalRewards(self):
        loc_results_iter = np.zeros(len(self.results), dtype=np.int16)
        loc_results = np.zeros(len(self.results[0]))
        for i in range(1, len(self.results[0])):
            best_val = self.results[0][loc_results_iter[0]]
            best = 0
            for pos, val in enumerate(loc_results_iter):
                if best_val <= self.results[pos][val]:
                    best_val = self.results[pos][val]
                    best = pos
            loc_results_iter[best] = loc_results_iter[best] + 1
            loc_results[i] = best_val + loc_results[i-1]
        return loc_results

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
t = 101
bandit = bandits(k, t=t)
Q = np.zeros(k)
N = np.zeros(k)
CR = np.zeros(t)

for i in range(1, t):
    A = getUCB(Q, N, i)
    R = bandit.getPrecomputedResult(A)
    CR[i] = R + CR[i-1]
    N[A] = N[A] + 1
    Q[A] = Q[A] + (1/N[A])*(R-Q[A])

print(bandit.hand)
print(N)
print(Q)
print(CR[1:]/bandit.getOptimalRewards()[1:])
