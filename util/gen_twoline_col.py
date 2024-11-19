import argparse
import random
import sys
import os
from to_mtx import to_mtx

offset = "./data"
directory = "/twoline_col"

# stride 달리 하면서 여러개 생성
def twoline(args : argparse.Namespace, filepath: str):

    number_of_nonzero_pannels = int(args.nRow / args.blockSize)
    nonzero_blocks_per_pannel = 2 * args.panelNum
    total_nonzero_blocks = number_of_nonzero_pannels * nonzero_blocks_per_pannel

    for stride in range(4,args.stride+1,4): # 블록 간 여백 길이(block 단위)

        result = []
        for i in range(args.nRow): #row
            for j in range(args.blockSize * args.panelNum):
                result.append([i,j,1.0]) #left
            for j in range(args.blockSize * args.panelNum):
                result.append([i,j+stride*args.blockSize + args.blockSize*args.panelNum,1.0]) #right #블록 단위 좌표가 아니라서 stride * blockSize

        to_mtx(filepath,number_of_nonzero_pannels,nonzero_blocks_per_pannel,args.nRow,args.nCol,args.blockSize,total_nonzero_blocks,result,stride)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-R','--nRow',type=int)
    parser.add_argument('-C','--nCol',type=int)
    parser.add_argument('-B','--blockSize',type=int)
    parser.add_argument('-S','--stride',type=int, default=32)
    parser.add_argument('-P','--panelNum',type=int, default=32)

    #gen.py만 단독 실행할 때 옵션
    parser.add_argument('--mode',type=str, default="shell")

    args = parser.parse_args()
    global offset
    if((args.panelNum*2+args.stride) * args.blockSize > args.nCol): sys.exit(f"Error: panelNum * 2 + stride ({args.panelNum * 2 + args.stride}) exceeds nCol ({args.nCol})")

    # gen.py만 단독 실행 - 따로 디렉토리 생성./data/R_C/long 생성. (이미 존재할 시 pass)
    offset += ("/" + str(args.nRow) + "_" + str(args.nCol))
    if(args.mode == "exclusive"): os.makedirs(offset+directory, exist_ok=True)

    twoline(args, offset+directory+"/")


if __name__=="__main__":
    main()