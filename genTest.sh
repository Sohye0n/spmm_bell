#!/bin/bash

size1=$1
size2=$2
blockSize=$3
rhsCol=$4
runMask=$5

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
subdirs[0]="/skinny"
subdirs[1]="/long"
subdirs[2]="/stair"
subdirs[3]="/zigzag"
subdirs[4]="/twoline_col"
subdirs[5]="/twoline_row"

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

# runMask에서 각 값을 배열로 변환
mask=($(echo "$runMask" | grep -o .))  # 각 숫자를 배열 요소로 저장
echo $runMask
echo "${mask[5]}"

for type in ${types[@]}; do
    echo "---- $type ----"
    if [[ $type == ${types[0]} ]]; then
        command_default=$command_default1
    else
        command_default=$command_default2
    fi

    if [ "${mask[0]}" -eq "1" ]; then

        ######## 실행 - skinny #######
        echo "---- skinny----"
        csv_file="${type}${subdirs[0]}.csv"
        echo "this $csv_file"

        # 데이터셋 생성
        echo "generating dataset for skinny"
        python3 ./util/gen_skinny.py $command_default

        # 실행시간 측정
        for i in {1..3}; do
            echo "set $i"
            results=()
            for file in $type/skinny/*.mtx; do
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
                    results+=("$blockSize,$A,$B,$i,$result")
                fi
            done


            # csv 파일에 기록
            echo "saving results to csv file"
            printf "%s\n" "${results[@]}" >> "$csv_file"

            # mtx 파일들은 모두 삭제
            rm -f $type/skinny/*.mtx
        done
    fi
    #####################################################

    if [ "${mask[1]}" -eq "1" ]; then

        ######## 실행 - long #######
        echo "---- long ----"
        csv_file="${type}${subdirs[1]}.csv"
        echo "this $csv_file"

        # 데이터셋 생성
        echo "generating dataset for long"
        python3 ./util/gen_long.py $command_default

        # 실행시간 측정
        for i in {1..3}; do
            echo "set $i"
            results=()
            for file in $type/long/*.mtx; do
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
                    results+=("$blockSize,$A,$B,$i,$result")
                fi
            done


            # csv 파일에 기록
            echo "saving results to csv file"
            printf "%s\n" "${results[@]}" >> "$csv_file"

            # mtx 파일들은 모두 삭제
            rm -f $type/long/*.mtx
        done
    fi
    #######################################################

    if [ "${mask[2]}" -eq "1" ]; then
        ######## 실행 - stair #######
        echo "---- stair ----"
        csv_file="${type}${subdirs[2]}.csv"
        echo "this $csv_file"

        # 데이터셋 생성
        echo "generating dataset for stair"
        python3 ./util/gen_stair.py $command_default

        # 실행시간 측정
        for i in {1..3}; do
            echo "set $i"
            results=()
            for file in $type/stair/*.mtx; do
                if [ -f "$file" ]; then
                    echo "$file"
                    base_name=$(basename "$file")
                    A=$(echo "$base_name" | cut -d'_' -f2)
                    B=$(echo "$base_name" | cut -d'_' -f3 | sed 's/\.mtx$//')  # 확장자 .mtx 제거

                    # 파일에서 ./data 부분 제거
                    relative_file="${file#./data}"

                    # main 명령 실행 결과를 result 변수에 저장
                    result=$(./main "$relative_file" "$blockSize" "$rhsCol" "1")

                    # result 값을 소수점 두 자리로 맞추어 저장
                    results+=("$blockSize,$A,$B,$i,$result")
                fi
            done


            # csv 파일에 기록
            echo "saving results to csv file"
            printf "%s\n" "${results[@]}" >> "$csv_file"

            # mtx 파일들은 모두 삭제
            rm -f $type/stair/*.mtx
        done
    fi
    ######################################################

    if [ "${mask[3]}" -eq "1" ]; then
        ######## 실행 - zigzag #######
        echo "---- zigzag ----"
        csv_file="${type}${subdirs[3]}.csv"
        echo "this $csv_file"

        # 데이터셋 생성
        echo "generating dataset for zigzag"
        python3 ./util/gen_zigzag.py $command_default

        # 실행시간 측정
        for i in {1..3}; do
            echo "set $i"
            results=()
            for file in $type/zigzag/*.mtx; do
                if [ -f "$file" ]; then
                    echo "$file"
                    base_name=$(basename "$file")
                    A=$(echo "$base_name" | cut -d'_' -f2)
                    B=$(echo "$base_name" | cut -d'_' -f3 | sed 's/\.mtx$//')  # 확장자 .mtx 제거

                    # 파일에서 ./data 부분 제거
                    relative_file="${file#./data}"

                    # main 명령 실행 결과를 result 변수에 저장
                    result=$(./main "$relative_file" "$blockSize" "$rhsCol" "1")

                    # result 값을 소수점 두 자리로 맞추어 저장
                    results+=("$blockSize,$A,$B,$i,$result")
                fi
            done


            # csv 파일에 기록
            echo "saving results to csv file"
            printf "%s\n" "${results[@]}" >> "$csv_file"

            # mtx 파일들은 모두 삭제
            rm -f $type/zigzag/*.mtx
        done
    fi
    ######################################################

    if [ "${mask[4]}" -eq "1" ]; then
        ######## 실행 - twoline_col #######
        echo "---- twoline_col ----"
        csv_file="${type}${subdirs[4]}.csv"
        echo "this $csv_file"

        # 데이터셋 생성
        echo "generating dataset for twoline_col"
        python3 ./util/gen_twoline_col.py $command_default

        # 실행시간 측정
        for i in {1..3}; do
            echo "set $i"
            results=()
            for file in $type/twoline_col/*.mtx; do
                if [ -f "$file" ]; then
                    echo "$file"
                    base_name=$(basename "$file")
                    A=$(echo "$base_name" | cut -d'_' -f2)
                    B=$(echo "$base_name" | cut -d'_' -f3 | sed 's/\.mtx$//')  # 확장자 .mtx 제거

                    # 파일에서 ./data 부분 제거
                    relative_file="${file#./data}"

                    # main 명령 실행 결과를 result 변수에 저장
                    result=$(./main "$relative_file" "$blockSize" "$rhsCol" "1")

                    # result 값을 소수점 두 자리로 맞추어 저장
                    results+=("$blockSize,$A,$B,$i,$result")
                fi
            done


            # csv 파일에 기록
            echo "saving results to csv file"
            printf "%s\n" "${results[@]}" >> "$csv_file"

            # mtx 파일들은 모두 삭제
            rm -f $type/twoline_col/*.mtx
        done
    fi
    ######################################################

    if [ "${mask[5]}" -eq "1" ]; then
        ######## 실행 - twoline_row #######
        echo "---- twoline_row ----"
        csv_file="${type}${subdirs[5]}.csv"
        echo "this $csv_file"

        # 데이터셋 생성
        echo "generating dataset for twoline_row"
        python3 ./util/gen_twoline_row.py $command_default

        # 실행시간 측정
        for i in {1..3}; do
            echo "set $i"
            results=()
            for file in $type/twoline_row/*.mtx; do
                if [ -f "$file" ]; then
                    echo "$file"
                    base_name=$(basename "$file")
                    A=$(echo "$base_name" | cut -d'_' -f2)
                    B=$(echo "$base_name" | cut -d'_' -f3 | sed 's/\.mtx$//')  # 확장자 .mtx 제거

                    # 파일에서 ./data 부분 제거
                    relative_file="${file#./data}"

                    # main 명령 실행 결과를 result 변수에 저장
                    result=$(./main "$relative_file" "$blockSize" "$rhsCol" "1")

                    # result 값을 소수점 두 자리로 맞추어 저장
                    results+=("$blockSize,$A,$B,$i,$result")
                fi
            done


            # csv 파일에 기록
            echo "saving results to csv file"
            printf "%s\n" "${results[@]}" >> "$csv_file"

            # mtx 파일들은 모두 삭제
            rm -f $type/twoline_row/*.mtx
        done
    fi
done
