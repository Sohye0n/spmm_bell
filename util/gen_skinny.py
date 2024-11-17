import argparse
import random
import os
from to_mtx import to_mtx

offset = "./data"
directory = "/skinny"

def skinny(args : argparse.Namespace, filepath: str):
    number_of_nonzero_panels = args.panelNum
    nonzero_blocks_per_panel = args.nCol / args.blockSize
    total_nonzero_blocks = number_of_nonzero_panels * nonzero_blocks_per_panel

    #데이터 생성 - column의 k%까지 4씩 밀면서 측정 (텐서코어가 4x4)
    #column이 20480이니까 2.5%하면 512까지. (만약 터미널 터져서 10240 가면 5%로 조정)
    #for leftgap in range(0,512,4):
    for leftgap in range(0,5,4):
        result=[]
        for i in range(args.nRow):
            for j in range(number_of_nonzero_panels * args.blockSize):
                result.append([i,j+leftgap,1.0])

        to_mtx(filepath,number_of_nonzero_panels,nonzero_blocks_per_panel,args.nRow,args.nCol,args.blockSize,total_nonzero_blocks,result,leftgap)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-R','--nRow',type=int)
    parser.add_argument('-C','--nCol',type=int)
    parser.add_argument('-B','--blockSize',type=int)
    parser.add_argument('-P','--panelNum',type=int, default=3)

    #gen.py만 단독 실행할 때 옵션
    parser.add_argument('--mode',type=str, default="shell")

    args = parser.parse_args()
    global offset

    # gen.py만 단독 실행 - 따로 디렉토리 생성./data/R_C/skinny 생성. (이미 존재할 시 pass)
    offset += ("/" + str(args.nRow) + "_" + str(args.nCol))
    if(args.mode == "exclusive"): os.makedirs(offset+directory, exist_ok=True)

    skinny(args, offset+directory+"/")


if __name__=="__main__":
    main()