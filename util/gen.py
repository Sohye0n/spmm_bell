import argparse
import random
import os

dir=["../data/simple_row/","../data/simple_col/","../data/random_row/","../data/random_col/"]

def randomPick(s: int, e: int, cnt: int):
    interval = e - s + 1 
    result = []
    
    if cnt <= interval:
        result.extend(random.sample(range(s, e + 1), cnt))
    else:
        while len(result) < cnt:
            result.extend(random.sample(range(s, e + 1), min(interval, cnt - len(result))))

    return result[:cnt]


def to_smtx(args: argparse.Namespace, thickness_rate: int, tiles_per_pannel: int, total_tiles: int, loc: list, path: int, cnt: int = 0):

    filename = dir[path]+"m"+str(cnt)+"_"+str(thickness_rate)+"_"+str(tiles_per_pannel)+".smtx"

    with open(filename, "w") as f1:
        density_per_tile = 1

        arr=[]
        
        #헤더
        f1.write("%%MatrixMarket matrix coordinate real general\n")

        # 행 개수, 열 개수, non-zero 개수
        print(total_tiles)
        arr.append([args.nRow, args.nCol, total_tiles * args.tileSize * args.tileSize * density_per_tile])

        # 타일 사이즈
        arr.append([args.tileSize, args.tileSize])
        
        for item in loc:
            arr.append(item)


        for line in arr:
            for word in line:
                f1.write(str(word)+" ")
            f1.write("\n")


# def type_simple_row(args : argparse.Namespace):

#     stride=args.tileSize
#     pannel_num = args.nRow // stride
#     density_per_tile = 1/3
#     nonzero_per_tile = round(args.tileSize * args.tileSize * density_per_tile)
#     nonzero_per_row_in_tile = nonzero_per_tile / args.tileSize

#     arr=[]

#     for i in range(1,pannel_num+1):
#         cnt_tile = args.tiles[i-1]
#         for row in range((i-1)*stride, i*stride):
#             for col in range(args.nCol):
#                 tileId = col // args.tileSize
#                 col_local = col - tileId * args.tileSize
#                 # 범위 안의 타일이고, 타일의 local column idx < 타일의 row별 non zero 개수
#                 if(tileId < cnt_tile and col_local < nonzero_per_row_in_tile ):
#                     arr.append([row,col,1.0])

#     return arr

def type_simple_row(args: argparse.Namespace):
    
    ans=[]

    for pannel_thickness_rate in range(10,41,10):
        pannel_thickness = int(pannel_thickness_rate * pannel_thickness_rate / 100 * args.nRow)
        print(pannel_thickness)
        result_per_thickness_rate=[]

        for i in range(pannel_thickness):
            for j in range(args.nCol):
                result_per_thickness_rate.append([i,j,1.0])

        ans.append(result_per_thickness_rate)

    return ans


def type_simple_col(args: argparse.Namespace):

    ans=[]

    for pannel_thickness_rate in range(10,41,10):
        pannel_thickness = int(pannel_thickness_rate * pannel_thickness_rate / 100.0 * args.nCol)

        result_per_thickness_rate=[]

        for i in range(args.nRow):
            for j in range(pannel_thickness):
                result_per_thickness_rate.append([i,j,1.0])

        ans.append(result_per_thickness_rate)

    return ans


def type_random_row(args : argparse.Namespace, cnt: int):

    for pannel_thickness_rate in range(10,11,10):
        pannel_thickness = int((pannel_thickness_rate / 100.0) * (args.nRow // args.tileSize))
        print("pannel_thickenss",pannel_thickness)
        
        for tiles_per_pannel in range(1,16,1):
        #for tiles_per_pannel in range(1,2,1):
            arr = randomPick(1,(args.nCol // args.tileSize), tiles_per_pannel * pannel_thickness)

            result = [[i, arr[j]] for i in range(pannel_thickness) for j in range(i * tiles_per_pannel, (i + 1) * tiles_per_pannel)]
            if(tiles_per_pannel == 1) : print(len(result))

            result_per_thickness_rate=[]
            
            for elem in result:
                r = elem[0]; c=elem[1]
                for i in range(r * args.tileSize , (r+1)*args.tileSize):
                    for j in range(c * args.tileSize , (c+1)*args.tileSize):
                        result_per_thickness_rate.append([i,j,1.0])

            to_smtx(args, pannel_thickness, tiles_per_pannel, len(arr), result_per_thickness_rate, 2, cnt)


def type_random_col(args : argparse.Namespace):

    ans=[]

    for pannel_thickness_rate in range(10,41,10):
        pannel_thickness = int(pannel_thickness_rate * (pannel_thickness_rate / 100.0) * (args.nCol // args.tileSize))
        
        for tiles_per_pannel in range(1,21,1):
            arr = randomPick(1,(args.nRow // args.tileSize), tiles_per_pannel * pannel_thickness)

            result = [[arr[j], i] for i in range(pannel_thickness) for j in range(i * tiles_per_pannel, (i + 1) * tiles_per_pannel)]

            result_per_thickness_rate=[]
            for elem in result:
                r = elem[0]; c=elem[1]
                for i in range(r * args.tileSize , (r+1)*args.tileSize):
                    for j in range(c * args.tileSize , (c+1)*args.tileSize):
                        result_per_thickness_rate.append([i,j,1.0])

            
            ans.append(result_per_thickness_rate)

    return ans


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-R','--nRow',type=int)
    parser.add_argument('-C','--nCol',type=int)
    parser.add_argument('-T','--tileSize',type=int)
    parser.add_argument('-tiles','--tiles',type=int, nargs='+')

    args = parser.parse_args()

    for directory in dir:
        os.makedirs(directory, exist_ok=True)


    for type in range(4):
        path=dir[type]

        # simple은 하나씩만 생성
        # if(type == 0):
        #     arr = type_simple_row(args)
        #     for thickness_rate, elem in enumerate(arr):
        #         to_smtx(args, (1+thickness_rate)*10, arr, path)

        # elif(type == 1):
        #     arr = type_simple_col(args)
        #     for thickness_rate, elem in enumerate(arr):
        #         to_smtx(args, (1+thickness_rate)*10, arr, path)

        if(type == 2):
            for i in range(1):
                arr = type_random_row(args,i)

        # # random은 10세트씩 생성
        # elif(type == 3):
        #     for i in range(10):
        #         arr = type_random_col(args)
        #         for thickness_rate, elem in enumerate(arr):
        #             to_smtx(args, (1+thickness_rate//20)*10, arr, path, i)
            

if __name__=="__main__":
    main()