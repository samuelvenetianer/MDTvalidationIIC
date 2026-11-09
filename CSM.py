import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import sys
from IPython.display import display
import math
from stats_func import calc_stats_txt
from time import sleep
from tqdm import tqdm
from plotting_func import plot_hist, plot_scatter, produce_good_cols_list

'''
Call in terminal as: python CSM.py <datafolder>
Test file: /net/s3_dataf/muon/MDT_Endcap_IIC/20261023_EMS1A08_EMS2A08_Zhen/csmMonitor_EMS1A08_CSM0_EMS2A08_CSM1_20261023_225045.csv 
'''

# Folder with datafiles
global_path = r"/net/s3_dataf/muon/MDT_Endcap_IIC/"
# user home folder
home_path = r"/home/svenetia/MDTvalidationIIC/"

# confirm that provided folder exists
for i in range(1,len(sys.argv)):
    folder_path = global_path + sys.argv[1]
    if os.path.exists(folder_path) == True:
        for file in os.listdir(folder_path):
            if "csmMonitor" in file:
                data_path_csm = folder_path + "/" +file
            if "mezzMonitor" in file:
                data_path_mezz = folder_path + "/" +file
            else:
                continue

        skip_stats = True

        # create folder to store output plots
        if os.path.exists(home_path+sys.argv[1]):
            print("Home folder already exists!")
            print("Do you want to re-generate plots for", sys.argv[1], "(y/n)?")
            next_step = input()
            if next_step == "n":
                print("Do you want to re-generate stats for", sys.argv[1], "(y/n)?")
                ans = input()
                if ans == "n":
                    print("Exiting...")
                    exit()
                if ans == "y":
                    print("Regenerating stats only...")
                    df_csm = pd.read_csv(data_path_csm, delimiter=',')
                    cols_to_ignore = ["scan", "time_s"]
                    df_mezz = pd.read_csv(data_path_mezz, delimiter=',')
                    cols_to_include = ["AVDD_display", "DVDD_display", "Temp_display"]
                    calc_stats_txt(df_csm, True, False, cols_to_ignore, sys.argv[1], "CSM_stats.txt")
                    calc_stats_txt(df_mezz, False, True, cols_to_include, sys.argv[1], "Mezz_stats.txt")
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
            skip_stats = False

        # CSM Analysis
        df_csm = pd.read_csv(data_path_csm, delimiter=',')
        cols_to_ignore = ["scan", "time_s"]
        good_df_csm = produce_good_cols_list(df_csm, True, False, cols_to_ignore)
        time_data = df_csm["time_s"]
        plot_hist(sys.argv[1], good_df_csm, 4, 30, 30, 45, "csm_hist")
        plot_scatter(sys.argv[1], good_df_csm, 4, 30, time_data, 30, 45, "csm_scatter")
        print("CSM data analyzed.")

        # Mezz Analysis
        df_mezz = pd.read_csv(data_path_mezz, delimiter=',')
        cols_to_include = ["AVDD_display", "DVDD_display", "Temp_display"]
        good_df_mezz = produce_good_cols_list(df_mezz, False, True, cols_to_include)
        scan_data = df_mezz["scan"]
        plot_hist(sys.argv[1], good_df_mezz, 3, 30, 30, 150, "mezz_hist")
        plot_scatter(sys.argv[1], good_df_mezz, 3, 30, scan_data, 30, 150, "mezz_scatter")
        print("Mezz data analyzed.")

        # print stats information to txt file
        if skip_stats == False:
            print("Calculating stats...")
            calc_stats_txt(df_csm, True, False, cols_to_ignore, sys.argv[1], "CSM_stats.txt")
            calc_stats_txt(df_mezz, False, True, cols_to_include, sys.argv[1], "Mezz_stats.txt")
        else:
            print("Stats skipped.")

        print("All done.")

    else:
        print("No folder at path: ", folder_path)
