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

'''
Call in terminal as: python CSM.py <datafolder>
Test file: /net/s3_dataf/muon/MDT_Endcap_IIC/20261023_EMS1A08_EMS2A08_Zhen/csmMonitor_EMS1A08_CSM0_EMS2A08_CSM1_20261023_225045.csv 
'''
# Folder with datafiles

# Arg parser for various flag options
arguments = argparse.ArgumentParser()
arguments.add_argument('--A', '--analyze-all-files', action='store_true')
arguments.add_argument('--S', '--analyze-specified-files', action='store_true')
arguments.add_argument('--files', '--list-of-files', nargs="*") # Accept min 0 files
arguments.add_argument('--local', '--use-folder-struct-local', action='store_true')
args = arguments.parse_args()

if args.local:
    global_path = "C:/Users/svene/OneDrive/Documents/Tufts/1. Research/8. MDT Electronics Comissioning/Raw_output_offline/"
    home_path = "C:/Users/svene/OneDrive/Documents/Tufts/1. Research/8. MDT Electronics Comissioning/"
else:
    global_path = r"/net/s3_dataf/muon/MDT_Endcap_IIC/"
    home_path = r"/home/svenetia/MDTvalidationIIC/"

# print(os.path.exists(global_path))
# print(os.path.exists(home_path))

folders = []
if args.S and not args.A:
    folders = args.files
elif args.A and not args.S:
    for i in os.listdir(global_path):
        list_files = os.listdir(r"/net/s3_dataf/muon/MDT_Endcap_IIC/"+i)
        if any("csmMonitor" in elem for elem in list_files):
            folders.append(i)
elif args.S and args.A:
    print("These commands contradict eachother. Please select only -A or -S.")
    exit()
else:
    print("Please use flags to choose all files (--A) or selection (--S)")
    exit()

# print(folders)

# confirm that provided folder exists
for i in folders:
    folder_path = global_path + i
    if os.path.exists(folder_path) == True:
        check_files(folder_path)
        print("Folder exists. Do you want to continue(y/n)?")
        move_on = input()
        if move_on == "y":
            for file in os.listdir(folder_path):
                if "csmMonitor" in file:
                    data_path_csm = folder_path + "/" +file
                    split = True
                if "mezzMonitor" in file:
                    data_path_mezz = folder_path + "/" +file
                    split = True
                elif "monitor" in file:
                    print("Joined filetype")
                    data_path_all = folder_path + "/" +file
                    split = False
                else:
                    # check run folders for monitor files
                    run_folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f)) and "run" in f]
                    # print(run_folders)
                    monitor_paths = []
                    notable_runs = []
                    for j in run_folders:
                        # print(j)
                        for k in os.listdir(folder_path+"/"+j):
                            if "monitor" in k:
                                monitor_paths.append(folder_path+"/"+j+"/"+k)
                                notable_runs.append(j)
                    # print(monitor_paths)
                    # print(notable_runs)
                    split = False

            skip_stats = True

    if os.path.exists(home_path+i):
        print(home_path + i + " already exists")
    else:
        os.mkdir(home_path+i)
        print(home_path + i + " created!")

            # create folder to store output plots
            # for home_path in monitor_paths:
            #     if os.path.exists(home_path+i):
            #         print("Home folder already exists!")
            #         print("Do you want to re-generate plots for", i, "(y/n)?")
            #         next_step = input()
            #         if next_step == "n":
            #             print("Do you want to re-generate stats for", i, "(y/n)?")
            #             ans = input()
            #             if ans == "n":
            #                 # print("Exiting...")
            #                 continue
            #                 # exit()
            #             if ans == "y":
            #                 print("Regenerating stats only...")
            #                 if split == True:
            #                     df_csm = pd.read_csv(data_path_csm, delimiter=',')
            #                     cols_to_ignore = ["scan", "time_s"]
            #                     df_mezz = pd.read_csv(data_path_mezz, delimiter=',')
            #                     cols_to_include = ["AVDD_display", "DVDD_display", "Temp_display"]
            #                     calc_stats_txt(df_csm, True, False, cols_to_ignore, i, "CSM_stats")
            #                     calc_stats_txt(df_mezz, False, True, cols_to_include, i, "Mezz_stats")
            #                     print("Done.")
            #                     continue
            #                     # exit()
            #                 if split == False:
            #                     df_all = pd.read_csv(data_path_all, delimiter=',')
            #                     cols_to_ignore = ["raw", "scan", "timestamp"]
            #                     calc_stats_txt(df_all, True, False, cols_to_ignore, i, "all_stats")
            #         elif next_step == "y":
            #             print("Do you want to re-generate stats?")
            #             ans = input()
            #             if ans == "n":
            #                 print("Re-generating plots only...")
            #                 skip_stats = True
            #             elif ans == "y":
            #                 skip_stats = False
            #                 print("Re-generating plots and stats...")
                    
            #     else:
            #         os.mkdir(home_path+i)
            #         print("Home folder created for: ", i)
            #         skip_stats = False

            # CSM Analysis
            # if split == True:
            #     df_csm = pd.read_csv(data_path_csm, delimiter=',')
            #     cols_to_ignore = ["scan", "time_s"]
            #     good_df_csm = produce_good_cols_list(df_csm, True, False, cols_to_ignore)
            #     time_data = df_csm["time_s"]
            #     plot_hist(i, good_df_csm, 4, 30, 45, 60, "csm_hist")
            #     plot_scatter(i, good_df_csm, 4, 30, time_data, 30, 45, "csm_scatter")
            #     print("CSM data analyzed.")

            #     # Mezz Analysis
            #     df_mezz = pd.read_csv(data_path_mezz, delimiter=',')
            #     cols_to_include = ["AVDD_display", "DVDD_display", "Temp_display"]
            #     good_df_mezz = produce_good_cols_list(df_mezz, False, True, cols_to_include)
            #     scan_data = df_mezz["scan"]
            #     plot_hist(i, good_df_mezz, 3, 30, 30, 150, "mezz_hist")
            #     plot_scatter(i, good_df_mezz, 3, 30, scan_data, 30, 150, "mezz_scatter")
            #     print("Mezz data analyzed.")

                # print stats information to txt file
                # if skip_stats == False:
                #     print("Calculating stats...")
                #     calc_stats_txt(df_csm, True, False, cols_to_ignore, i, "CSM_stats")
                #     calc_stats_txt(df_mezz, False, True, cols_to_include, i, "Mezz_stats")
                # else:
                #     print("Stats skipped.")

                # print("All done.")
            
    if split == False:
        run_folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f)) and "run" in f]
        for j in run_folders:
            for k in os.listdir(folder_path+"/"+j):
                if "monitor" in k:
                    # monitor_paths.append(folder_path+"/"+j+"/"+k)
                    # notable_runs.append(j)
                    df_all = pd.read_csv(folder_path+"/"+j+"/"+k, delimiter=',')
                    cols_to_ignore = ["raw", "scan", "timestamp"]
                    scan_data = df_all["scan"]
                    good_df = produce_good_cols_list(df_all, True, False, cols_to_ignore)
                    # print(len(good_df))
                    print("plotting hists")
                    plot_hist(i+"/"+j, good_df, 4, 30, 30, 45, "all_hist")
                    print("plotting scatters")
                    plot_scatter(i+"/"+j, good_df, 4, 30, scan_data, 30, 150, "all_scatter")
                    print("calculating stats")
                    calc_stats_txt(df_all, True, False, cols_to_ignore, i+"/"+j, "all_stats")
                else:
                    continue

        # print(monitor_paths)
        # print(notable_runs)
        # split = False

        
        # print("stopping")
        # for data_path_all in monitor_paths:
        #     df_all = pd.read_csv(data_path_all, delimiter=',')
        #     cols_to_ignore = ["raw", "scan", "timestamp"]
        #     scan_data = df_all["scan"]
        #     good_df = produce_good_cols_list(df_all, True, False, cols_to_ignore)
        #     # print(len(good_df))
        #     print("plotting hists")
        #     plot_hist(i, good_df, 4, 30, 30, 45, "all_hist")
        #     print("plotting scatters")
        #     plot_scatter(i, good_df, 4, 30, scan_data, 30, 150, "all_scatter")

        #     print("working on stats")
        #     if skip_stats == False:
        #         print("Calculating stats...")
        #         calc_stats_txt(df_all, True, False, cols_to_ignore, i, "all_stats")
        #     else:
        #         print("Stats skipped.")

        #     print("All done.")

    else:
        print("No folder at path: ", folder_path)
