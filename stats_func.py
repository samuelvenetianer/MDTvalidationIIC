import pandas as pd

def calc_stats_txt(dataframe, foldername):

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
    summary=summary.drop(labels=["scan", "time_s"], axis=0, inplace=False)
    max_time_s = dataframe["time_s"].max()
    max_time_hr = max_time_s/3600
    
    with open("CSM_stats.txt", 'w') as f:
        f.write("Dataset: ")
        f.write(foldername)
        f.write("\n")
        f.write("Length of run: ")
        f.write(str(round(max_time_hr,2)))
        f.write(" hour(s)")
        f.write("\n")
        f.write("Statistics:\n")
        df_string = summary.to_string(header=True, index=True)
        f.write(df_string + '\n')

    return

def calc_rms(data, parameter:str, output_folder:str):
    """
    Function calculates root mean square of provided array
    
    Parameters:
        data: values of interest
        parameter: label of interest for printing result
 
    """
    squared=np.square(data)
    rms=np.sqrt(np.sum(squared)/len(data))
    # print("Root Mean Squared of", parameter, "is: ", rms)
    
    with open(output_folder+"/"+"stats.txt", 'a') as f:
        f.write("Root Mean Squared of "+ parameter+ " is: "+ str(rms)+"\n")

    return rms

def calc_stddev(data, parameter:str, output_folder:str):

    """
    Function calculates standard deviation of provided array
    
    Parameters:
        data: values of interest
        parameter: label of interest for printing result

    """
    std_dev=np.std(data)
    #print("Standard Deviation of", parameter, "is: ", std_dev)
    
    with open(output_folder+"/"+"stats.txt", 'a') as f:
        f.write("Standard Deviation of "+ parameter+ " is: "+ str(std_dev)+ "\n")

    return std_dev


