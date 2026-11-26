import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import sys
from IPython.display import display
import math
from time import sleep
from tqdm import tqdm

def produce_good_cols_list(dataframe, ignore, include, cols):
    hist_list = []

    if ignore == True:
        for all_cols in list(dataframe):
            if any(elem in all_cols for elem in cols):
                continue
            else:
                hist_list.append(all_cols)
    elif include == True:
        for all_cols in list(dataframe):
            if any(elem in all_cols for elem in cols):
                hist_list.append(all_cols)
            else:
                continue
    
    new_df = dataframe[hist_list].copy()
               
    return new_df

def plot_hist(foldername, new_df, number_of_cols, number_of_bins, fig_sizex, fig_sizey, png_title):
    '''
    dataframe: pd dataframe
    ignore: bool
    include: bool
    cols: array of str
    bins: int
    fig_sizex: int
    fig_sizey: int
    '''

    num_plots = len(new_df.columns)
    num_cols = number_of_cols
    num_rows = math.ceil(num_plots/num_cols)

    new_df.hist(column=new_df.columns, bins=number_of_bins, layout =(num_rows,num_cols), figsize= (fig_sizex,fig_sizey), color='skyblue', edgecolor='black', grid=False)
    plt.suptitle(foldername)
    # save_path = "/home/svenetia/MDTvalidationIIC"+"/"+foldername+"/"+foldername+"_"+png_title+".png"
    save_path = "C:/Users/svene/OneDrive/Documents/Tufts/1. Research/8. MDT Electronics Comissioning/"+foldername+"_hist.png"
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()

def plot_scatter(foldername, new_df, number_of_cols, number_of_bins, xaxis_data, fig_sizex, fig_sizey, png_title):

    num_plots = len(new_df.columns)
    num_cols = number_of_cols
    num_rows = math.ceil(num_plots/num_cols)

    row_counter = 0
    col_counter = 0

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(fig_sizex, fig_sizey))
    for i in range(0, num_plots):
        if col_counter < num_cols:
            axs[row_counter, col_counter].scatter(xaxis_data, new_df[new_df.columns[i]])
            axs[row_counter, col_counter].set_title(new_df.columns[i])
            col_counter+=1
        else:
            col_counter = 0
            row_counter += 1
            axs[row_counter, col_counter].scatter(xaxis_data, new_df[new_df.columns[i]])
            axs[row_counter, col_counter].set_title(new_df.columns[i])
            col_counter+=1

    # save_path = "/home/svenetia/MDTvalidationIIC"+"/"+foldername+"/"+foldername+"_"+png_title+".png"
    # save_path = "C:/Users/svene/OneDrive/Documents/Tufts/1. Research/8. MDT Electronics Comissioning/"+foldername+"/"+foldername+"_"+png_title+".png"
    save_path = "C:/Users/svene/OneDrive/Documents/Tufts/1. Research/8. MDT Electronics Comissioning/"+foldername+"_scatter.png"

    # print(save_path)
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()