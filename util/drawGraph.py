import csv
import os
import pandas as pd
from matplotlib import pyplot as plt
import re

def drawGraph(y: list, x: list, name: str, filepath: str, xticks: list, legends: list, xlabel: str, ylabel:str = "elapsed time (ms)"):
    plt.figure() 
    for lbl,arr in zip(legends,y):
        if(name[:6]=="simple") : plt.plot(x,arr,marker="o", linestyle="-", label=lbl) 
        else: plt.plot(x,arr,marker="|", linestyle="-",label=lbl)

    plt.xticks(xticks)
    legendTitle=name[7:10]
    plt.legend(title="# of non-zero " + legendTitle + " pannels")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(name)
    plt.savefig(name)