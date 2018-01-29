import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple


n_groups = 5

means_men = (20, 35, 30, 35, 27)
std_men = (2, 3, 4, 1, 2)

means_women = (25, 32, 34, 20, 25)
std_women = (3, 5, 2, 3, 3)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = ax.barh(index, means_men, bar_width,
                 alpha=opacity, color='b',
                 label='Men')

rects2 = ax.barh(index + bar_width, means_women, bar_width,
                 alpha=opacity, color='r',
                 label='Women')

ax.set_ylabel('Group')
ax.set_xlabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_yticks(index + bar_width / 2)
ax.set_yticklabels(('A', 'B', 'C', 'D', 'E'))
ax.legend()

fig.tight_layout()
plt.show()
