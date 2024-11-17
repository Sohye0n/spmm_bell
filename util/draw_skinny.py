import csv
import os
import pandas as pd
from matplotlib import pyplot as plt
from drawGraph import drawGraph

data = os.path.join(os.getcwd(), "./data")

def draw_skinny(name:str, filepath:str):
    df = pd.read_csv(filepath)

    try:
        num_batch = df.iloc[:,3].nunique() # 총 몇 번 돌려서 평균 냈는지
        num_point = len(df)/num_batch
        xticks = sorted(df.iloc[:,1].unique().astype(int))
        legends = list(df.iloc[:,0].unique().astype(int))
    except:
        print("error")

    #time
    #leftgap 순으로 정렬해야 해서 1,4번째 인덱스 모두 가져옴
    gap_time = df.iloc[:,[1,4]].values.tolist()
    gap_time.sort(key=lambda x:x[0])
    time = [x[0] for x in gap_time]

    #batch개 만큼 존재하는 데이터를 더해서 평균
    avg_time = []
    for i in range(num_point):
        sum = 0.0
        for j in range(num_batch):
            sum+=time[i+j*num_point]
        avg_time[i] = sum/num_batch

    drawGraph(avg_time, xticks, name, filepath, xticks, legends, "gap from left")
