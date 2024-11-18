import argparse
import random
import os
from to_mtx import to_mtx

offset = "./data"
directory = "/zigzag"

# stride 달리 하면서 여러개 생성
def zigzag(args : argparse.Namespace, filepath: str):

    number_of_nonzero_panels = int(args.nRow / args.blockSize)
    nonzero_blocks_per_panel = 2
    total_nonzero_blocks = number_of_nonzero_panels * nonzero_blocks_per_panel

    # block 단위로 non-zero 좌표 표시
    for stride in range(4,args.stride,4): # 블록 간 여백 길이

        result_block=[]
        result = []
        for i in range(number_of_nonzero_panels): #row
            result_block.append([i,0]) #left
            result_block.append([i,stride+1]) #right

        # block 단위 좌표 -> 원래 행렬 기준 좌표로 변환
        for elem in result_block:
            row = elem[0]; col=elem[1]

            for i in range(row*args.blockSize, (row+1)*args.blockSize):
                for j in range(col*args.blockSize, (col+1)*args.blockSize): 
                    result.append([i,j,1.0])


        to_mtx(filepath,stride,nonzero_blocks_per_panel,args.nRow,args.nCol,args.blockSize,total_nonzero_blocks,result)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-R','--nRow',type=int)
    parser.add_argument('-C','--nCol',type=int)
    parser.add_argument('-B','--blockSize',type=int)
    parser.add_argument('-S','--stride',type=int, default=32)

    #gen.py만 단독 실행할 때 옵션
    parser.add_argument('--mode',type=str, default="shell")

    args = parser.parse_args()
    global offset

    # gen.py만 단독 실행 - 따로 디렉토리 생성./data/R_C/long 생성. (이미 존재할 시 pass)
    offset += ("/" + str(args.nRow) + "_" + str(args.nCol))
    if(args.mode == "exclusive"): os.makedirs(offset+directory, exist_ok=True)

    zigzag(args, offset+directory+"/")


if __name__=="__main__":
    main()