import csv
import os
import pandas as pd
from matplotlib import pyplot as plt
import re

data = os.path.join(os.getcwd(), "./data")


def drawGraph(y: list, x: list, name: str, filepath: str, xticks: list, legends: list):
    plt.figure() 
    for lbl,arr in zip(legends,y):
        if(name[:6]=="simple") : plt.plot(x,arr, 'o', label=lbl) 
        else: plt.plot(x,arr, label=lbl)
    plt.xticks(xticks)
    legendTitle=name[7:10]
    plt.legend(title=legendTitle+" pannel thickness")
    plt.xlabel("none zero tiles per pannel")
    plt.ylabel("elapsed tilme")
    plt.title(name)
    plt.savefig(name)

    
    
def processRandom(name: str, filepath: str):

    # open file
    df = pd.read_csv(filepath, header=None)

    idx=1
    if(name[:10]=="simple_col"): idx=2
    
    try:
        num_batch = df.iloc[:,3].nunique()
        num_set = df.iloc[:,idx].nunique()
        num_point = len(df) // (num_batch * num_set)
        xticks = sorted(df.iloc[:,3-idx].unique())
        legends = sorted(df.iloc[:,idx].unique().astype(int))
        print(legends)
        #print("num_batch : ",num_batch, "num_set : ",num_set, "num_point : ",num_point)
    except:
        print("error")

    # pannel_thickness 기준으로 group
    grouped = df.groupby(df.iloc[:,idx])

    # time만 가져옴
    averages = []
    if(idx==1): group_list = [group.iloc[:,[2,3,4]].values.tolist() for _,group in grouped]
    else: group_list = [group.iloc[:,[1,3,4]].values.tolist() for _,group in grouped]
    for i,group in enumerate(group_list):
        group.sort(key=lambda x: (x[0],x[1]))  # group 자체를 정렬
        group_y = [x[2] for x in group]
        group_x =sorted(list(set(x[0] for x in group)))

        batch_averages = []
        
        for i in range(num_point):
            batch_data = group_y[i * num_batch : (i+1) * num_batch]
            batch_averages.append(sum(batch_data) / len(batch_data))
            #if(name=="random_col_10240_5120" and i==1): print(batch_data)

        
        
        averages.append(batch_averages)
    
    print(len(averages))
    print(group_x)
    drawGraph(averages, group_x, name, filepath, xticks, legends)



def main():
    subfolders=[]
    arr=[]

    for subdir in os.listdir(data):
        if os.path.isdir(os.path.join(data, subdir)):
            subfolders.append("./data/"+subdir+"/")


    for subdir in subfolders:
        csv_files = []

        # collect all csv files in dir
        for file in os.listdir(subdir):
            if file.endswith('.csv'):
                csv_files.append(file)

        # draw graph for each file
        for file in csv_files:
            #print(file[:-4]+"_"+subdir[7:-1])
            processRandom(file[:-4]+"_"+subdir[7:-1], subdir+file)
            # if(file == "random_row.csv"):
            #     draw(file, subdir+file)
            # elif(file == "random_col.csv"):
            #     pass
            #     #drawRandomCol()
            # elif(file == "smiple_col.csv"):
            #     pass
            #     #drawSimpleCol()
            # elif(file == "simple_row.csv"):
            #     pass
            #     #drawSimpleRow()
        print("------------------------------------")

if __name__=="__main__":
    main()