import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import sys
from IPython.display import display
import math
from stats_func import calc_stats_txt

# Testcommit 

'''
Call in terminal as: python CSM.py <datafolder>
Test file: /net/s3_dataf/muon/MDT_Endcap_IIC/20261023_EMS1A08_EMS2A08_Zhen/csmMonitor_EMS1A08_CSM0_EMS2A08_CSM1_20261023_225045.csv 
'''

# Folder with datafiles
global_path = r"/net/s3_dataf/muon/MDT_Endcap_IIC/"
# user home folder
home_path = r"/home/svenetia/MDTvalidationIIC/"

# confirm that provided folder exists
folder_path = global_path + sys.argv[1]
if os.path.exists(folder_path) == True:
    print("Reading folder: ", folder_path)

    # locate csmMonitor file
    for file in os.listdir(folder_path):
        if "csmMonitor" in file:
            data_path = folder_path + "/" +file
        else:
            continue

    print("csmMonitor file found: ", data_path)

    skip_stats = True

    # create folder to store output plots
    if os.path.exists(home_path+sys.argv[1]):
        print("Home folder already exists!")
        print("Do you want to re-generate plots for", sys.argv[1], "(y/n)?")
        next_step = input()
        if next_step == "n":
            print("Do you want to re-generate stats?")
            ans = input()
            if ans == "n":
                print("Exiting...")
                exit()
            if ans == "y":
                print("Regenerating stats only...")
                df = pd.read_csv(data_path, delimiter = ',')
                calc_stats_txt(df, sys.argv[1])
                print("Done.")
                exit()
        elif next_step == "y":
            print("Do you want to re-generate stats?")
            ans = input()
            if ans == "n":
                print("Re-generating plots only...")
                skip_stats = True
            elif ans == "y":
                skip_stats = False
                print("Re-generating plots and stats...")
            
    else:
        os.mkdir(home_path+sys.argv[1])
        print("Home folder created!")

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

    num_plots = len(hist_list)
    num_cols = 4

    # determine number of rows for plot png
    num_rows = math.ceil(num_plots/num_cols)

    print("Plotting histograms...")
    df.hist(column=hist_list, bins=30, layout =(num_rows,num_cols), figsize= (35,40), color='skyblue', edgecolor='black', grid=False)
    plt.suptitle(sys.argv[1])
    plt.savefig("/home/svenetia/MDTvalidationIIC"+"/"+sys.argv[1]+"/"+sys.argv[1]+"_hist.png", bbox_inches="tight")
    plt.close()
    print("Histograms plotted.")

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

    fig.savefig("/home/svenetia/MDTvalidationIIC"+"/"+sys.argv[1]+"/"+sys.argv[1]+"_scatter.png")
    plt.close()

    print("Scatters plotted.")


    # print stats information to txt file
    if skip_stats == False:
        print("Calculating stats...")
        calc_stats_txt(df, sys.argv[1])
    else:
        print("Stats skipped.")

    print("All done.")

else:
    print("No folder at path: ", folder_path)
