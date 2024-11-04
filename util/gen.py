import argparse
import random
import os

dir=["./data/simple_row/","./data/simple_col/","./data/random_row/","./data/random_col/"]

import random

def randomPick(s: int, e: int, cnt: int, tiles_per_pannel: int):
    interval = e - s
    result = []
    
    if cnt <= interval:
        # cnt가 interval보다 작거나 같으면 비복원 샘플링
        result.extend(random.sample(range(s, e), cnt))
    else:
        # cnt가 interval보다 크면 tiles_per_pannel 개씩 비복원 샘플링
        while len(result) < cnt:
            # interval이 현재의 result 길이보다 크거나 같다면 tiles_per_pannel을 샘플링
            samples = random.sample(range(s, e), tiles_per_pannel)
            result.extend(samples)

    return result[:cnt]



def to_smtx(args: argparse.Namespace, thickness_rate: int, tiles_per_pannel: int, total_tiles: int, loc: list, path: int, cnt: int = 0):

    filename = dir[path]+"m"+str(cnt)+"_"+str(thickness_rate)+"_"+str(tiles_per_pannel)+".smtx"

    with open(filename, "w") as f1:
        density_per_tile = 1

        arr=[]
        
        #헤더
        f1.write("%%MatrixMarket matrix coordinate real general\n")

        # 행 개수, 열 개수, non-zero 개수
        arr.append([args.nRow, args.nCol, total_tiles * args.tileSize * args.tileSize * density_per_tile])

        # 타일 사이즈
        arr.append([args.tileSize, args.tileSize])
        
        for item in loc:
            arr.append(item)


        for line in arr:
            for word in line:
                f1.write(str(word)+" ")
            f1.write("\n")


def type_simple_row(args: argparse.Namespace):

    for pannel_thickness_rate in range(10,41,10):
        pannel_thickness = int(args.nRow * pannel_thickness_rate / 100)
        result_per_thickness_rate=[]

        for i in range(pannel_thickness):
            for j in range(args.nCol):
                result_per_thickness_rate.append([i,j,1.0])


        to_smtx(args, (pannel_thickness/args.tileSize), (args.nCol / args.tileSize), (args.nCol / args.tileSize) * (pannel_thickness/args.tileSize), result_per_thickness_rate, 0)



def type_simple_col(args: argparse.Namespace):

    for pannel_thickness_rate in range(10,41,10):
        pannel_thickness = int(args.nCol * pannel_thickness_rate / 100.0)
        result_per_thickness_rate=[]

        for i in range(args.nRow):
            for j in range(pannel_thickness):
                result_per_thickness_rate.append([i,j,1.0])

        to_smtx(args, (args.nRow / args.tileSize), (pannel_thickness/args.tileSize), (args.nRow / args.tileSize) * (pannel_thickness/args.tileSize), result_per_thickness_rate, 1)


def type_random_row(args : argparse.Namespace, cnt: int):

    for pannel_thickness_rate in range(10,41,10):
        pannel_thickness = int((pannel_thickness_rate / 100.0) * (args.nRow // args.tileSize))
        
        for tiles_per_pannel in range(1,int(args.nCol / args.tileSize), int(0.1 * args.nCol / args.tileSize)):
            arr = randomPick(0,(args.nCol // args.tileSize), tiles_per_pannel * pannel_thickness, tiles_per_pannel)

            result = [[i, arr[j]] for i in range(pannel_thickness) for j in range(i * tiles_per_pannel, (i + 1) * tiles_per_pannel)]

            result_per_thickness_rate=[]
            
            for elem in result:
                r = elem[0]; c=elem[1]
                for i in range(r * args.tileSize , (r+1)*args.tileSize):
                    for j in range(c * args.tileSize , (c+1)*args.tileSize):
                        result_per_thickness_rate.append([i,j,1.0])

            sorted_data = sorted(result_per_thickness_rate, key=lambda x: (x[0], x[1], x[2]))

            to_smtx(args, pannel_thickness, tiles_per_pannel, len(arr), sorted_data, 2, cnt)


def type_random_col(args : argparse.Namespace, cnt: int):

    for pannel_thickness_rate in range(10,41,10):
        pannel_thickness = int((pannel_thickness_rate / 100.0) * (args.nCol // args.tileSize))
        
        for tiles_per_pannel in range(1,int(args.nRow / args.tileSize), int(0.1 * args.nRow / args.tileSize)):
            arr = randomPick(0,(args.nRow // args.tileSize), tiles_per_pannel * pannel_thickness, tiles_per_pannel)

            result = [[arr[j], i] for i in range(pannel_thickness) for j in range(i * tiles_per_pannel, (i + 1) * tiles_per_pannel)]

            result_per_thickness_rate=[]
            for elem in result:
                r = elem[0]; c=elem[1]
                for i in range(r * args.tileSize , (r+1)*args.tileSize):
                    for j in range(c * args.tileSize , (c+1)*args.tileSize):
                        result_per_thickness_rate.append([i,j,1.0])

            sorted_data = sorted(result_per_thickness_rate, key=lambda x: (x[0], x[1], x[2]))
            to_smtx(args, pannel_thickness, tiles_per_pannel, len(arr), sorted_data, 3, cnt)



def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-R','--nRow',type=int)
    parser.add_argument('-C','--nCol',type=int)
    parser.add_argument('-T','--tileSize',type=int)

    args = parser.parse_args()

    for directory in dir:
        os.makedirs(directory, exist_ok=True)


    for type in range(4):
        path=dir[type]

        #simple은 하나씩만 생성
        if(type == 0):
            arr = type_simple_row(args)

        elif(type == 1):
            arr = type_simple_col(args)

        elif(type == 2):
            for i in range(1):
                type_random_row(args,i)

        # # random은 10세트씩 생성
        elif(type == 3):
            for i in range(1):
                type_random_col(args,i)

            

if __name__=="__main__":
    main()