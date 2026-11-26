import pandas as pd
import os

def calc_stats_txt(dataframe_full, ignore, include, cols, foldername, filename):

    hist_list = []
    if ignore == True:
        for all_cols in list(dataframe_full):
            if any(elem in all_cols for elem in cols):
                continue
            else:
                hist_list.append(all_cols)
    elif include == True:
        for all_cols in list(dataframe_full):
            if any(elem in all_cols for elem in cols):
                hist_list.append(all_cols)
            else:
                continue

    dataframe=dataframe_full[hist_list].copy()
    
    # find stats for only alive tubes
    mins=dataframe.min().to_frame()
    mins.columns=["Min"]
    maxes=dataframe.max().to_frame()
    maxes.columns=["Max"]
    means=dataframe.mean().to_frame()
    means.columns=["Mean"]
    stds=dataframe.std().to_frame()
    stds.columns=["Standard dev"]
    datatypes=dataframe.dtypes.to_frame()
    datatypes.columns=["Data type"]
    summary=pd.concat([mins,maxes,means,stds, datatypes],axis=1)
    # summary=summary.drop(labels=["scan", "time_s"], axis=0, inplace=False)
    # max_time_s = dataframe["time_s"].max()
    # max_time_hr = max_time_s/3600
    
    # save_path = "/home/svenetia/MDTvalidationIIC"+"/"+foldername+"/"+foldername+"_"+filename+".txt"
    save_path = "C:/Users/svene/OneDrive/Documents/Tufts/1. Research/8. MDT Electronics Comissioning/"+foldername+"_stats.txt"
    # save_path = "C:/Users/svene/OneDrive/Documents/Tufts/1. Research/8. MDT Electronics Comissioning/"+foldername+"/"+foldername+"_"+filename+".txt"

    with open(save_path, 'w') as f:
        f.write("Dataset: ")
        f.write(foldername)
        f.write("\n")
        # f.write("Length of run: ")
        # f.write(str(round(max_time_hr,2)))
        # f.write(" hour(s)")
        # f.write("\n")
        f.write("Statistics:\n")
        df_string = summary.to_string(header=True, index=True)
        f.write(df_string + '\n')

    return

def check_files(folder):
    all_files = os.listdir(folder)
    num_csv = 0
    for file in all_files:
        if ".csv" in file:
            num_csv += 1
            print(file)




