import matplotlib.pyplot as plt


import pandas as pd
dates = ['2015-12-20','2018-09-12']
PM_25 = [80, 55]
dates = [pd.to_datetime(d) for d in dates]

plt.scatter(dates, PM_25, s =100, c = 'red')
plt.show()
