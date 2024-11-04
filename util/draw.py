import csv
import os
import pandas as pd

data = os.path.join(os.getcwd(), "./data")

csv_files = []
arr=[]

for file in os.listdir(data):
    if file.endswith('.csv'):
        csv_files.append("./data/"+file)

for file in csv_files:
    try:
        df = pd.read_csv(file)
        cnt = df[df.columns[0]].nunique()
        arr.append(cnt)

    except Exception as e:
        print(f"파일 {csv_files}을 읽는 중 오류 발생: {e}")
