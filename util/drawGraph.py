import csv
import os
import pandas as pd
from matplotlib import pyplot as plt
import re

def drawGraph(y: list, x: list, name: str, filepath: str, xticks: list, legends: list, xlabel: str, ylabel:str = "elapsed time (ms)", fsize:tuple=(20,10), multiples: list = None):
    plt.figure(figsize=fsize) 
    plt.plot(x,y,marker="o", linestyle="-")

    if multiples:
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta']  # 색상 목록
        for i, m in enumerate(multiples):
            color = colors[i % len(colors)]  # 색상 반복
            multiples_indices = [idx for idx, val in enumerate(x) if val % m == 0]
            plt.scatter([x[idx] for idx in multiples_indices],
                        [y[idx] for idx in multiples_indices], 
                        color=color, label=f"{m}-multiple", zorder=5)

    plt.xticks(xticks)
    legendTitle=name[7:10]
    plt.legend(title="# of non-zero " + legendTitle + " pannels",loc='upper left')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(name)
    plt.savefig(name)