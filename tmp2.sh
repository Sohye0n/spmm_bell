#!/bin/bash

size1=$1
size2=$2
blockSize=$3
rhsCol=$4

echo $size1 $size2 $blockSize $rhsCol

# (R x C), (C x R) 사이즈 행렬 생성
types=()

if [ "$size1" -eq "$size2" ]; then
    types[0]="./data/${size1}_${size2}"
else
    types[0]="./data/${size1}_${size2}"
    types[1]="./data/${size2}_${size1}"
fi

# csv 파일이 없으면 생성
subdirs=()
subdirs[0]="/zigzag"
subdirs[1]="/skinny"
subdirs[2]="/twoline_col"

for type in ${types[@]}; do
    # 없을 때만 새로 생성
    if [ ! -d "$type" ]; then
        mkdir "$type"
    fi

    for subdir in ${subdirs[@]}; do

        dir_path="${type}${subdir}"
        csv_file="${dir_path}.csv"

        #없을 때만 새로 생성
        if [ ! -d "$dir_path" ]; then
            mkdir -p "$dir_path"
        fi

        # .csv 파일이 존재하면 ./data로 이동시키고 새 파일 생성
        if [ -f "$csv_file" ]; then
            mv "$csv_file" ./data/
        fi

        touch "${type}${subdir}.csv"
    done
done

command_default1="-R $size1 -C $size2 -B $blockSize --mode exclusive"
command_default2="-R $size2 -C $size1 -B $blockSize --mode exclusive"

for type in ${types[@]}; do
    echo "---- $type ----"
    if [[ $type == ${types[0]} ]]; then
        command_default=$command_default1
    else
        command_default=$command_default2
    fi

    for i in $(seq 4 4 96); do
        ######## 실행 - zigzag #######
        echo "---- zigzag -P ${i} ----"
        csv_file="${type}${subdirs[0]}.csv"
        echo "this $csv_file"

        # 데이터셋 생성
        echo "generating dataset for zigzag"
        python3 ./util/gen_zigzag.py $command_default -S 64 -P $i

        for j in {1..5}; do
            # 실행시간 측정
            for a in {1..1}; do
                echo "set $a"
                results=()
                for file in $type/zigzag/*.mtx; do
                    if [ -f "$file" ]; then
                        echo "$file"
                        base_name=$(basename "$file")
                        A=$(echo "$base_name" | cut -d'_' -f1 | sed 's/^m//')
                        B=$(echo "$base_name" | cut -d'_' -f3 | sed 's/\.mtx$//')  # 확장자 .mtx 제거

                        echo $A, $B

                        # 파일에서 ./data 부분 제거
                        relative_file="${file#./data}"

                        # main 명령 실행 결과를 result 변수에 저장
                        result=$(./main "$relative_file" "$blockSize" "$rhsCol" "1")

                        # result 값을 소수점 두 자리로 맞추어 저장
                        results+=("$blockSize,$A,$B,$a,$result")
                    fi
                done


                # csv 파일에 기록
                echo "saving results to csv file"
                printf "%s\n" "${results[@]}" >> "$csv_file"
            done
        done
        # mtx 파일들은 모두 삭제
        rm -f $type/zigzag/*.mtx
    done

    for i in $(seq 4 4 96); do
        
        ######## 실행 - skinny #######
        echo "---- skinny -P ${i} ----"
        csv_file="${type}${subdirs[1]}.csv"
        echo "this $csv_file"

        # 데이터셋 생성
        echo "generating dataset for skinny"
        python3 ./util/gen_skinny.py $command_default -P $i
        for j in {1..5}; do
            # 실행시간 측정
            for a in {1..1}; do
                echo "set $a"
                results=()
                for file in $type/skinny/*.mtx; do
                    if [ -f "$file" ]; then
                        echo "$file"
                        base_name=$(basename "$file")
                        A=$(echo "$base_name" | cut -d'_' -f1 | sed 's/^m//')
                        B=$(echo "$base_name" | cut -d'_' -f2)

                        # 파일에서 ./data 부분 제거
                        relative_file="${file#./data}"

                        # main 명령 실행 결과를 result 변수에 저장
                        result=$(./main "$relative_file" "$blockSize" "$rhsCol" "1")

                        # result 값을 소수점 두 자리로 맞추어 저장
                        results+=("$blockSize,$A,$B,$a,$result")
                    fi
                done
                # csv 파일에 기록
                echo "saving results to csv file"
                printf "%s\n" "${results[@]}" >> "$csv_file"
            done
        done
        # mtx 파일들은 모두 삭제
        rm -f $type/skinny/*.mtx
    done

    for i in $(seq 4 4 96); do
        
        ######## 실행 - twoline_col #######
        echo "---- twoline_col -P ${i} ----"
        csv_file="${type}${subdirs[2]}.csv"
        echo "this $csv_file"

        # 데이터셋 생성
        echo "generating dataset for twoline_col"
        python3 ./util/gen_twoline_col.py $command_default -S 64 -P $i
        for j in {1..5}; do
            # 실행시간 측정
            for a in {1..3}; do
                echo "set $a"
                results=()
                for file in $type/twoline_col/*.mtx; do
                    if [ -f "$file" ]; then
                        echo "$file"
                        base_name=$(basename "$file")
                        A=$(echo "$base_name" | cut -d'_' -f1 | sed 's/^m//')
                        B=$(echo "$base_name" | cut -d'_' -f3 | sed 's/\.mtx$//')  # 확장자 .mtx 제거

                        # 파일에서 ./data 부분 제거
                        relative_file="${file#./data}"

                        # main 명령 실행 결과를 result 변수에 저장
                        result=$(./main "$relative_file" "$blockSize" "$rhsCol" "1")

                        # result 값을 소수점 두 자리로 맞추어 저장
                        results+=("$blockSize,$A,$B,$a,$result")
                    fi
                done


                # csv 파일에 기록
                echo "saving results to csv file"
                printf "%s\n" "${results[@]}" >> "$csv_file"
            done
        done
        # mtx 파일들은 모두 삭제
        rm -f $type/twoline_col/*.mtx
    done
done