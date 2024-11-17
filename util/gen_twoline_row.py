import argparse
import random
import os
from to_mtx import to_mtx

offset = "./data"
directory = "/twoline_row"

# stride 달리 하면서 여러개 생성
def twoline(args : argparse.Namespace, filepath: str):

    number_of_nonzero_pannels = 2
    nonzero_blocks_per_pannel = int(args.nCol / args.blockSize)
    total_nonzero_blocks = number_of_nonzero_pannels * nonzero_blocks_per_pannel

    for stride in range(4,32,4): # 블록 간 여백 길이(block 단위)

        result = []
        for i in range(args.blockSize): #row
            for j in range(args.nCol):
                result.append([i,j,1.0])
        for i in range(args.blockSize):
            for j in range(args.nCol):
                result.append([i+stride*args.blockSize,j,1.0])

        to_mtx(filepath,stride,nonzero_blocks_per_pannel,args.nRow,args.nCol,args.blockSize,total_nonzero_blocks,result)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-R','--nRow',type=int)
    parser.add_argument('-C','--nCol',type=int)
    parser.add_argument('-B','--blockSize',type=int)

    #gen.py만 단독 실행할 때 옵션
    parser.add_argument('--mode',type=str, default="shell")

    args = parser.parse_args()
    global offset

    # gen.py만 단독 실행 - 따로 디렉토리 생성./data/R_C/long 생성. (이미 존재할 시 pass)
    offset += ("/" + str(args.nRow) + "_" + str(args.nCol))
    if(args.mode == "exclusive"): os.makedirs(offset+directory, exist_ok=True)

    twoline(args, offset+directory+"/")


if __name__=="__main__":
    main()