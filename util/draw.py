import csv
import os
import pandas as pd
from matplotlib import pyplot as plt
import re
import dataframe_image as dfi

data = os.path.join(os.getcwd(), "./data")
excution_time = {}

def drawAcc(filename: str):
    num_pannel_thickness = len(excution_time['rr'])
    num_blocks_per_pannel = len(excution_time['rr'][0])
 
    increase_rr = [[0 for _ in range(2,num_blocks_per_pannel)] for _ in range(num_pannel_thickness)]
    for i in range(num_pannel_thickness):
        for j in range(2,num_blocks_per_pannel):
            increase_rr[i][j-2] = (excution_time['rr'][i][j] / excution_time['rr'][i][1])

    increase_rc = [[0 for _ in range(2,num_blocks_per_pannel)] for _ in range(num_pannel_thickness)]
    for i in range(num_pannel_thickness):
        for j in range(2,num_blocks_per_pannel):
            increase_rc[i][j-2] = (excution_time['rc'][i][j] / excution_time['rc'][i][1])

    data = [increase_rr[0], increase_rc[0],
            increase_rr[1], increase_rc[1],
            increase_rr[2], increase_rc[2],
            increase_rr[3], increase_rc[3],
            increase_rr[4], increase_rc[4],
            increase_rr[5], increase_rc[5],
            increase_rr[6], increase_rc[6],
            increase_rr[7], increase_rc[7],
            increase_rr[8], increase_rc[8]
            ]
    index_names = ["row_10%", "col_10%", "row_20%", "col_20%", 
                   "row_30%", "col_30%", "row_40%", "col_40%",
                   "row_50%", "col_50%", "row_60%", "col_60%",
                   "row_70%", "col_70%", "row_80%", "col_80%",
                   "row_90%", "col_90%"]
    
    labels = list(range(20,100,10))
    df = pd.DataFrame(data, index=index_names, columns=labels)
    df.columns = pd.MultiIndex.from_product([['% of non-zero blocks per pannel'], df.columns])
    df.index = pd.MultiIndex.from_product([["% of non-zero pannels"], df.index])
    styled_df = df.style.set_table_styles(
        [{"selector": "th.col_level", "props": "text-align: center;"},
        {"selector": "th.row_level", "props": "text-align: center;"},
        ], axis="columns"
    )
    dfi.export(df, filename+"_increase_rate.png")


def drawGraph(y: list, x: list, name: str, filepath: str, xticks: list, legends: list):
    plt.figure() 
    for lbl,arr in zip(legends,y):
        if(name[:6]=="simple") : plt.plot(x,arr,marker="o", linestyle="-", label=lbl) 
        else: plt.plot(x,arr,marker="|", linestyle="-",label=lbl)

    plt.xticks(xticks)
    legendTitle=name[7:10]
    plt.legend(title="# of non-zero " + legendTitle + " pannels")
    plt.xlabel("# of non-zero blocks per pannel")
    plt.ylabel("elapsed tilme (ms) ")
    plt.title(name)
    plt.savefig(name)


def speedup(filename: str):
    num_pannel_thickness = len(excution_time['rr'])
    num_blocks_per_pannel = len(excution_time['rr'][0])
 
    diff = [[0 for _ in range(num_blocks_per_pannel)] for _ in range(num_pannel_thickness)]
    for i in range(num_pannel_thickness):
        for j in range(num_blocks_per_pannel):
            diff[i][j] = (excution_time['rr'][i][j] / excution_time['rc'][i][j])

    data = [excution_time['rr'][0], excution_time['rc'][0], diff[0], 
            excution_time['rr'][1], excution_time['rc'][1], diff[1],
            excution_time['rr'][2], excution_time['rc'][2], diff[2],
            excution_time['rr'][3], excution_time['rc'][3], diff[3],
            excution_time['rr'][4], excution_time['rc'][4], diff[4],
            excution_time['rr'][5], excution_time['rc'][5], diff[5],
            excution_time['rr'][6], excution_time['rc'][6], diff[6],
            excution_time['rr'][7], excution_time['rc'][7], diff[7],
            excution_time['rr'][8], excution_time['rc'][8], diff[8],
            ]

    index_names = ["row_10%", "col_10%", "speedup (row time / col time)", "row_20%", "col_20%", "speedup (row time / col time)",
                "row_30%", "col_30%", "speedup (row time / col time)", "row_40%", "col_40%", "speedup (row time / col time)",
                "row_50%", "col_50%", "speedup (row time / col time)", "row_60%", "col_60%", "speedup (row time / col time)",
                "row_70%", "col_70%", "speedup (row time / col time)", "row_80%", "col_80%", "speedup (row time / col time)",
                "row_90%", "col_90%", "speedup (row time / col time)"]

    # DataFrame 생성 (N x M 형태)
    labels = list(range(0,100,10))
    labels[0] = 1

    df = pd.DataFrame(data, index=index_names, columns=labels)
    df.columns = pd.MultiIndex.from_product([['% of non-zero blocks per pannel'], df.columns])
    df.index = pd.MultiIndex.from_product([["% of non-zero pannels"], df.index])
    styled_df = df.style.set_table_styles(
        [{"selector": "th.col_level", "props": "text-align: center;"},
        {"selector": "th.row_level", "props": "text-align: center;"},
        ], axis="columns"
    )
    dfi.export(df, filename+"_time_compare.png")

def processSimple(name: str, filepath: str):
    # open file
    df = pd.read_csv(filepath, header=None)

    idx=1
    if(name[:10]=="simple_col"): idx=2

    try:
        xticks = sorted(df.iloc[:,idx].unique())
        legends = list(df.iloc[:,3-idx].unique().astype(int))
    except:
        print("error")

    # pannel_thickness 기준으로 group
    grouped = df.groupby(df.iloc[:,idx])

    # time만 가져옴
    averages = []
    if(idx==1): group_list = [group.iloc[:,[1,3,4]].values.tolist() for _,group in grouped]
    else:group_list = [group.iloc[:,[2,3,4]].values.tolist() for _,group in grouped]

    batch_averages = []
    for i,group in enumerate(group_list):
        group.sort(key=lambda x: (x[0],x[1]))  # group 자체를 정렬
        time = [x[2] for x in group] # time 값만 모은 그룹

        batch_averages.append(sum(time) / len(time))
    averages.append(batch_averages)
    drawGraph(averages, xticks, name, filepath, xticks, legends)


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
    except:
        print("error")

    # pannel_thickness 기준으로 group
    grouped = df.groupby(df.iloc[:,idx])

    # time만 가져옴
    averages = []
    if(idx==1): group_list = [group.iloc[:,[2,3,4]].values.tolist() for _,group in grouped]
    else:group_list = [group.iloc[:,[1,3,4]].values.tolist() for _,group in grouped]

    for i,group in enumerate(group_list):
        group.sort(key=lambda x: (x[0],x[1]))  # group 자체를 정렬
        group_y = [x[2] for x in group]
        group_x =sorted(list(set(x[0] for x in group)))

        batch_averages = []
        
        for i in range(num_point):
            batch_data = group_y[i * num_batch : (i+1) * num_batch]
            batch_averages.append(sum(batch_data) / len(batch_data))

        averages.append(batch_averages)
    
    drawGraph(averages, group_x, name, filepath, xticks, legends)
    if(name[:10]=="random_row"): excution_time['rr'] = averages
    if(name[:10]=="random_col"): excution_time['rc'] = averages


def main():
    subfolders=[]
    randoms=[]

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
            subdir_name = os.path.basename(os.path.normpath(subdir))

            if(file[:-8]=="random"): processRandom(file[:-4]+"_"+subdir_name, subdir+file)
            elif(file[:-8]=="simple"): processSimple(file[:-4]+"_"+subdir_name, subdir+file)
            # random 끼리 실행 시간을 비교하기 위해
            if(file[:-4]=="random_row" or file[:-4]=="random_col"):
                randoms.append(subdir+file)

        print("------------------------------------")
        # draw graph to compare random_row and random_col
        if(len(randoms)==2) :
            speedup(subdir_name)
            drawAcc(subdir_name)
            randoms = []

if __name__=="__main__":
    main()