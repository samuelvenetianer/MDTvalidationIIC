import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import sys
from IPython.display import display

'''
Call in terminal as: python CSM.py <datafolder>
Test file: /net/s3_dataf/muon/MDT_Endcap_IIC/20261023_EMS1A08_EMS2A08_Zhen/csmMonitor_EMS1A08_CSM0_EMS2A08_CSM1_20261023_225045.csv 
'''

# Folder with datafiles
global_path = r"/net/s3_dataf/muon/MDT_Endcap_IIC/"

# confirm that provided folder exists
folder_path = global_path + "/"+ sys.argv[1]
if os.path.exists(folder_path) == True:
    print("Reading folder: ", folder_path)

    # locate csmMonitor file
    for file in os.listdir(folder_path):
        if "csmMonitor" in file:
            data_path = folder_path + "/" +file
        else:
            continue

    print("csmMonitor file found: ", data_path)

    # Read CSV to dataframe and assign headers
    print("Converting to dataframe...")
    df = pd.read_csv(data_path, delimiter=',')
    # print("Headers: ", list(df))
    print("Number of headers: ", len(list(df)))
    # display(df)

    hist_list = []
    for cols in list(df):
        if (cols == "scan") or (cols == "time_s"):
            continue
        else:
            hist_list.append(cols)

    print("Plotting histograms...")
    df.hist(column=hist_list, bins=30, layout =(11,4), figsize= (35,40), color='skyblue', edgecolor='black', grid=False)
    plt.suptitle(sys.argv[1])
    plt.savefig("/home/svenetia/MDT_voltage_temp_validation"+"/"+sys.argv[1]+"_hist.png", bbox_inches="tight")
    plt.close()
    print("Histograms plotted.")

    num_plots = len(hist_list)
    num_rows = 11
    num_cols = 4

    row_counter = 0
    col_counter = 0

    print("Plotting time evolution...")
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(45, 60))
    for i in range(0, num_plots):
        if col_counter < num_cols:
            axs[row_counter, col_counter].scatter(df['time_s'], df[hist_list[i]])
            axs[row_counter, col_counter].set_title(hist_list[i])
            col_counter+=1
        else:
            col_counter = 0
            row_counter += 1
            axs[row_counter, col_counter].scatter(df['time_s'], df[hist_list[i]])
            axs[row_counter, col_counter].set_title(hist_list[i])
            col_counter+=1

    fig.savefig(sys.argv[1]+"_scatter.png")
    plt.close()

    # # Generate individual scatter plots
    # for cols in list(df):
    #     fig = plt.figure()
    #     plt.scatter(df['time_s'], df[cols])
    #     plt.xlabel('Time (s)')
    #     plt.ylabel(cols)
    #     fig.savefig(cols+".png")
    #     plt.close()

    print("Scatters plotted.")
    print("All done.")

else:
    print("No folder at path: ", folder_path)
