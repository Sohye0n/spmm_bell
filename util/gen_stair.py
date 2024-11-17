import argparse
import random
import os
from to_mtx import to_mtx

offset = "./data"
directory = "/stair"

def stair(args : argparse.Namespace, filepath: str):
    number_of_nonzero_pannels = args.panelNum

    max_nonzero_blocks = args.panelNum # 수평 방향으로 최대 몇 개의 non-zero block을 배치할 수 있는가?
    max_height = int(args.nRow / args.blockSize) - max_nonzero_blocks +1 #수평 방향으로 가장 마지막 non-zero block아래에, 최대 몇 개의 non-zero block을 붙일 수 있는가?


    # block 단위로 non-zero 좌표 표시
    for h in range(1,max_height): #수직 방향 두께

        nonzero_blocks_per_pannel = h
        total_nonzero_blocks = number_of_nonzero_pannels * nonzero_blocks_per_pannel

        result_block=[]
        result = []
        for i in range(0,h): # row
            for j in range(0,max_nonzero_blocks-1): #col
                result_block.append([j+i,j])

        # block 단위 좌표 -> 원래 행렬 기준 좌표로 변환
        for elem in result_block:
            row = elem[0]; col=elem[1]

            for i in range(row*args.blockSize, (row+1)*args.blockSize):
                for j in range(col*args.blockSize, (col+1)*args.blockSize): 
                    result.append([i,j,1.0])


        to_mtx(filepath,number_of_nonzero_pannels,nonzero_blocks_per_pannel,args.nRow,args.nCol,args.blockSize,total_nonzero_blocks,result)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-R','--nRow',type=int)
    parser.add_argument('-C','--nCol',type=int)
    parser.add_argument('-B','--blockSize',type=int)
    parser.add_argument('-P','--panelNum',type=int, default=64)

    #gen.py만 단독 실행할 때 옵션
    parser.add_argument('--mode',type=str, default="shell")

    args = parser.parse_args()
    global offset

    # gen.py만 단독 실행 - 따로 디렉토리 생성./data/R_C/skinny 생성. (이미 존재할 시 pass)
    offset += ("/" + str(args.nRow) + "_" + str(args.nCol))
    if(args.mode == "exclusive"): os.makedirs(offset+directory, exist_ok=True)

    stair(args, offset+directory+"/")


if __name__=="__main__":
    main()