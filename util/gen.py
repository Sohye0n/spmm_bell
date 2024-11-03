import argparse

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-R','--nRow',type=int)
    parser.add_argument('-C','--nCol',type=int)
    parser.add_argument('-T','--tileSize',type=int)
    parser.add_argument('-tiles','--tiles',type=int, nargs='+')

    args = parser.parse_args()

    f1= open("./data/m1.smtx","w")

    stride=args.tileSize
    pannel_num = args.nRow // stride
    density_per_tile = 1/3
    nonzero_per_tile = round(args.tileSize * args.tileSize * density_per_tile)
    nonzero_per_row_in_tile = nonzero_per_tile / args.tileSize

    arr=[]
    
    #헤더
    f1.write("%%MatrixMarket matrix coordinate real general\n")

    # 행 개수, 열 개수, non-zero 개수
    total_tiles = sum(args.tiles)
    arr.append([args.nRow, args.nCol, total_tiles * args.tileSize * args.tileSize * density_per_tile])

    # 타일 사이즈
    arr.append([args.tileSize, args.tileSize])


    # 행, 열, non-zero value
    # 윗 패널부터 접근
    for i in range(1,pannel_num+1):
        cnt_tile = args.tiles[i-1]
        for row in range((i-1)*stride, i*stride):
            for col in range(args.nCol):
                tileId = col // args.tileSize
                col_local = col - tileId * args.tileSize
                # 범위 안의 타일이고, 타일의 local column idx < 타일의 row별 non zero 개수
                if(tileId < cnt_tile and col_local < nonzero_per_row_in_tile ):
                    arr.append([row,col,1.0])

    for line in arr:
        for word in line:
            f1.write(str(word)+" ")
        f1.write("\n")
    f1.close()

if __name__=="__main__":
    main()