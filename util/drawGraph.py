import csv
import os
import pandas as pd
from matplotlib import pyplot as plt
import re

def drawGraph(y: list, x: list, name: str, filepath: str, xticks: list, legends: list, xlabel: str, ylabel:str = "elapsed time (ms)", fsize:tuple=(20,10)):
    plt.figure(figsize=fsize) 
    plt.plot(x,y,marker="o", linestyle="-")

    plt.xticks(xticks)
    legendTitle=name[7:10]
    plt.legend(title="# of non-zero " + legendTitle + " pannels")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(name)
    plt.savefig(name)