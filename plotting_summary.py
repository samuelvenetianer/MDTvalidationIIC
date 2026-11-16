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

# Create list of folders

path = r"/home/svenetia/MDTvalidationIIC/"
only_folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f)) and ("pycache") not in f and "git" not in f]
# print(only_folders)

# Start an empty bar chart (matplotlib.pyplot.bar(x, height, width=0.8, bottom=None, *, align='center', data=None, **kwargs))

fix, ax = plt.subplots()

# Loop thru folders and grab stats file

for folder in only_folders:
    files = os.listdir(path+folder)
    # print(files)
    for file in files:
        if "CSM_stats" in file:
            # print("here is the file we want: ", file)
            
            # Import txt to dataframe, set headers
            cols = ["param", "min", "max", "mean", "stddev", "datatype"]
            df = pd.read_csv(path+folder+"/"+file, skiprows=3, header = None, sep=r'\s+')
            df.columns = cols
            # display(df)

            # Grab data from one column and plot to bar chart
            ax.bar(folder, df.loc[0, "min"])
            if "voltage" in df["param"][0]:
                ax.set_ylabel("Voltage")
            else:
                ax.set_ylabel("Temperature")
            ax.set_title(df["param"][0])
            ax.tick_params(axis='x', labelrotation=90)
        else:
            continue

# Save out figure
plt.savefig(r'/home/svenetia/MDTvalidationIIC/test.png', bbox_inches="tight")
plt.close()