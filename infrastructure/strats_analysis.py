import enum
from infrastructure import *
from RPM import RPMBernoulli
from TS import ThompsonSamplingBernoulli
import matplotlib.pyplot as plt
import dill
import bz2
import numpy as np


files = ['ts_n100_T5000.bz2', 'rpm_n100_T5000.bz2', 'gbb_n100_T5000.bz2']
names = ['Thompson sampling', 'Randomised probability matching', 'Greedy Bayesian']
colors = ['red', 'black', 'green']
strats = []
for file in files:
    with bz2.open(file, 'rb') as handle:
        strats.append(dill.load(handle))


n = 100     # no of simulations
T = 5000    # horizon

# [strat1_hist_regrets, strat2...]
hist_regret_arrs = [np.array([game.historical_regret for game in games]) for games in strats]
confidences = [95, 70, 50]


# [[strat1_interval_1, strat1_interval_2,...],[strat2_...],...]
# strat1_interval_1 = (u, b) where u is the upper array to be plotted
def get_u_b(hist_regrets, confidence):
    return [np.percentile(hist_regrets, 50 + confidence/2, axis=0),
            np.percentile(hist_regrets, 50 - confidence/2, axis=0),
            ]


strat_u_b = [[get_u_b(arrs, conf) for conf in confidences] for arrs in hist_regret_arrs]
mean_arrs = [np.mean(arr, axis=0) for arr in hist_regret_arrs]

for n, strat in enumerate(strat_u_b):
    ax = plt.subplot(2, 2, n+1)
    ax.plot(range(T+1), mean_arrs[n])
    for confidence in strat:
        u, b = confidence
        ax.fill_between(range(T+1), b, u, alpha=0.5)
    ax.legend(['mean']+[f"{conf}% CI" for conf in confidences])
    ax.set_xlabel("Horizon")
    ax.set_ylabel("Cumulative regret")
    ax.set_title(names[n])

plt.tight_layout()
plt.show()