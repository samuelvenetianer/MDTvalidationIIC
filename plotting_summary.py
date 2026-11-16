import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import sys
from IPython.display import display
import math
from stats_func import calc_stats_txt, check_files
from time import sleep
from tqdm import tqdm
from plotting_func import plot_hist, plot_scatter, produce_good_cols_list
import argparse

# Start an empty bar chart
# matplotlib.pyplot.bar(x, height, width=0.8, bottom=None, *, align='center', data=None, **kwargs)[source]

fix, ax = plt.subplots()

# Import txt to dataframe, set headers
cols = ["param", "min", "max", "mean", "stddev", "datatype"]
df = pd.read_csv(r'/home/svenetia/MDTvalidationIIC/20261006_EMS4C10_Ed/20261006_EMS4C10_Ed_CSM_stats.txt', skiprows=3, header = None, delim_whitespace = True)
df.columns = cols
display(df)

# Grab data from one column and plot to bar chart
ax.bar("20261006_EMS4C10_Ed_min", df.loc[0, "min"])
# ax.bar("20261006_EMS4C10_Ed_max", df.loc[0, "max"])
if "voltage" in df["param"][0]:
    ax.set_ylabel("Voltage")
else:
    ax.set_ylabel("Temperature")
ax.set_title(df["param"][0])

# Save out figure
plt.savefig(r'/home/svenetia/MDTvalidationIIC/test.png', bbox_inches="tight")
plt.close()