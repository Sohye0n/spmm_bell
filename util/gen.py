import argparse
import random
import os


import random

offset = "./data"
dir=["/simple_row/","/simple_col/","/random_row/","/random_col/"]

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


def to_mtx(args: argparse.Namespace, thickness_rate: int, tiles_per_pannel: int, total_tiles: int, loc: list, path: int, cnt: int = 0):

    filename = offset+dir[path]+"m"+str(cnt)+"_"+str(thickness_rate)+"_"+str(tiles_per_pannel)+".mtx"
    #print(filename)
    with open(filename, "w") as f1:
        density_per_tile = 1

        arr=[]
        
        #헤더
        f1.write("%%MatrixMarket matrix coordinate real general\n")

        # 행 개수, 열 개수, non-zero 개수
        arr.append([args.nRow, args.nCol, total_tiles * args.tileSize * args.tileSize * density_per_tile])
        
        for item in loc:
            arr.append(item)


        for line in arr:
            for word in line:
                f1.write(str(word)+" ")
            f1.write("\n")


def type_simple_row(args: argparse.Namespace):

    for pannel_thickness_rate in range(10,41,10):
        pannel_thickness = round( (args.nRow / args.tileSize) * (pannel_thickness_rate / 100) )
        result_per_thickness_rate=[]

        for i in range(pannel_thickness * args.tileSize):
            for j in range(args.nCol):
                result_per_thickness_rate.append([i,j,1.0])


        to_mtx(args, pannel_thickness, int(args.nCol / args.tileSize), (args.nCol / args.tileSize) * pannel_thickness, result_per_thickness_rate, 0)


def type_simple_col(args: argparse.Namespace):

    for pannel_thickness_rate in range(10,41,10):
        pannel_thickness = round((args.nCol / args.tileSize) * (pannel_thickness_rate / 100.0))
        result_per_thickness_rate=[]

        for i in range(args.nRow):
            for j in range(pannel_thickness * args.tileSize):
                result_per_thickness_rate.append([i,j,1.0])

        to_mtx(args, int(args.nRow / args.tileSize), pannel_thickness, (args.nRow / args.tileSize) * pannel_thickness, result_per_thickness_rate, 1)


def type_random_row(args : argparse.Namespace, cnt: int):

    for pannel_thickness_rate in range(10,41,10):
        pannel_thickness = round((args.nRow / args.tileSize) * (pannel_thickness_rate / 100.0))
        
        for tiles_per_pannel in range(1, int(args.nCol / args.tileSize), round(0.1 * args.nCol / args.tileSize)):
            arr = randomPick(0,(args.nCol // args.tileSize), tiles_per_pannel * pannel_thickness, tiles_per_pannel)

            result = [[i, arr[j]] for i in range(pannel_thickness) for j in range(i * tiles_per_pannel, (i + 1) * tiles_per_pannel)]

            result_per_thickness_rate=[]
            
            for elem in result:
                r = elem[0]; c=elem[1]
                for i in range(r * args.tileSize , (r+1)*args.tileSize):
                    for j in range(c * args.tileSize , (c+1)*args.tileSize):
                        result_per_thickness_rate.append([i,j,1.0])

            sorted_data = sorted(result_per_thickness_rate, key=lambda x: (x[0], x[1], x[2]))

            to_mtx(args, pannel_thickness, tiles_per_pannel, len(arr), sorted_data, 2, cnt)


def type_random_col(args : argparse.Namespace, cnt: int):

    for pannel_thickness_rate in range(10,41,10):
        pannel_thickness = round((pannel_thickness_rate / 100.0) * (args.nCol / args.tileSize))
        
        for tiles_per_pannel in range(1,int(args.nRow / args.tileSize), round(0.1 * args.nRow / args.tileSize)):
            arr = randomPick(0,(args.nRow // args.tileSize), tiles_per_pannel * pannel_thickness, tiles_per_pannel)

            result = [[arr[j], i] for i in range(pannel_thickness) for j in range(i * tiles_per_pannel, (i + 1) * tiles_per_pannel)]

            result_per_thickness_rate=[]
            for elem in result:
                r = elem[0]; c=elem[1]
                for i in range(r * args.tileSize , (r+1)*args.tileSize):
                    for j in range(c * args.tileSize , (c+1)*args.tileSize):
                        result_per_thickness_rate.append([i,j,1.0])

            sorted_data = sorted(result_per_thickness_rate, key=lambda x: (x[0], x[1], x[2]))
            to_mtx(args, pannel_thickness, tiles_per_pannel, len(arr), sorted_data, 3, cnt)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-R','--nRow',type=int)
    parser.add_argument('-C','--nCol',type=int)
    parser.add_argument('-T','--tileSize',type=int)
    parser.add_argument('--type',type=str)
    #gen.py만 단독 실행할 때 옵션
    parser.add_argument('--mode',type=str, default="shell")

    args = parser.parse_args()
    global offset

    # gen.py만 단독 실행
    if(args.mode == "exclusive"):
        for directory in dir:
            offset += ("/" + str(args.nRow) + "_" + str(args.nCol))
            os.makedirs(offset+directory, exist_ok=True)

            for type in range(4):

                if(type == 0):
                    arr = type_simple_row(args)

                elif(type == 1):
                    arr = type_simple_col(args)

                elif(type == 2):
                    for i in range(1):
                        type_random_row(args,i)

                elif(type == 3):
                    for i in range(1):
                        type_random_col(args,i)

    # 셸 스크립트로 실행
    else:
        offset += ("/" + str(args.nRow) + "_" + str(args.nCol))
        if(args.type == "sr"):
            type_simple_row(args)

        elif(args.type == "sc"):
            type_simple_col(args)

        elif(args.type == "rr"):
            for i in range(1):
                type_random_row(args,i)

        elif(args.type == "rc"):
            for i in range(1):
                type_random_col(args,i)



            

if __name__=="__main__":
    main()