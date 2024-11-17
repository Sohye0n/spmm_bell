# filepath : ../../../ 형태
def to_mtx(filepath: str, number_of_nonzero_pannels: int, nonzero_blocks_per_pannel: int, nRow: int, nCol: int, blockSize: int, total_blocks: int, loc: list, cnt: int = 0):

    filename = filepath+"m"+str(cnt)+"_"+str(number_of_nonzero_pannels)+"_"+str(nonzero_blocks_per_pannel)+".mtx"
    #print(filename)
    with open(filename, "w") as f1:
        density_per_tile = 1

        arr=[]
        
        #헤더
        f1.write("%%MatrixMarket matrix coordinate real general\n")

        # 행 개수, 열 개수, non-zero 개수
        arr.append([nRow, nCol, total_blocks * blockSize * blockSize * density_per_tile])
        
        for item in loc:
            arr.append(item)

        for line in arr:
            for word in line:
                f1.write(str(word)+" ")
            f1.write("\n")