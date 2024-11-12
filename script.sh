#!/bin/bash

# 디렉토리, csv 파일 생성
size1=$1
size2=$2
tileSize=$3
rhsCol=$4

types=()

if [ "$size1" -eq "$size2" ]; then
    types[0]="./data/${size1}_${size2}"
else
    types[0]="./data/${size1}_${size2}"
    types[1]="./data/${size2}_${size1}"
fi

subdirs=()
subdirs[0]="/simple_row"
subdirs[1]="/simple_col"
subdirs[2]="/random_row"
subdirs[3]="/random_col"


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

command_default="-R $size1 -C $size2 -T $tileSize"
for type in ${types[@]}; do
    echo "---- $type ----"

    ######## 실행 - sr #######
    echo "---- simple_row ----"
    csv_file="${type}${subdirs[0]}.csv"
    echo "this $csv_file"

    # 데이터셋 생성
    echo "generating dataset for simple_row"
    python3 ./util/gen.py $command_default --type sr

    # 실행시간 측정
    for i in {1..4}; do
        echo "set $i"
        results=()
        for file in $type/simple_row/*.mtx; do
            if [ -f "$file" ]; then
                echo "$file"
                base_name=$(basename "$file")
                A=$(echo "$base_name" | cut -d'_' -f2)
                B=$(echo "$base_name" | cut -d'_' -f3 | sed 's/\.mtx$//')  # 확장자 .mtx 제거

                # 파일에서 ./data 부분 제거
                relative_file="${file#./data}"

                # main 명령 실행 결과를 result 변수에 저장
                result=$(./main "$relative_file" "$tileSize" "$rhsCol" "1")

                # result 값을 소수점 두 자리로 맞추어 저장
                printf -v result "%.2f" "$result"
                results+=("$tileSize,$A,$B,$i,$result")
            fi
        done


        # csv 파일에 기록
        echo "saving results to csv file"
        printf "%s\n" "${results[@]}" >> "$csv_file"

        # mtx 파일들은 모두 삭제
        #rm -f ./data/$type/simple_row/*.mtx
    done

    ######################################################

    ######## 실행 - sc #######
    echo "---- simple_col ----"
    csv_file="${type}${subdirs[1]}.csv"

    # 데이터셋 생성
    echo "generating dataset for simple_col"
    python3 ./util/gen.py $command_default --type sc

    # 실행시간 측정
    for i in {1..4}; do
        echo "set $i"
        results=()
        for file in $type/simple_col/*.mtx; do
            if [ -f "$file" ]; then
                base_name=$(basename "$file")
                A=$(echo "$base_name" | cut -d'_' -f2)
                B=$(echo "$base_name" | cut -d'_' -f3 | sed 's/\.mtx$//')  # 확장자 .mtx 제거

                # 파일에서 ./data 부분 제거
                relative_file="${file#./data}"

                result=$(./main "$relative_file" "$tileSize" "$rhsCol" "1")
                
                echo $relative_file
                printf -v result "%.2f" "$result"
                results+=("$tileSize,$A,$B,$i,$result")
            fi
        done

        # csv 파일에 기록
        echo "saving results to csv file"
        printf "%s\n" "${results[@]}" >> "$csv_file"

        # mtx 파일들은 모두 삭제
        #rm -f ./data/$type/simple_col/*.mtx
    done
    ######################################################

    ######## 실행 - rr #######
    echo "---- random_row ----"
    csv_file="${type}${subdirs[2]}.csv"

    # 데이터셋 생성
    echo "generating dataset for random_row"
    for i in {1..4}; do
        echo "set $i"
        results=()
        python3 ./util/gen.py $command_default --type rr

        # 실행시간 측정
        for file in $type/random_row/*.mtx; do
            if [ -f "$file" ]; then
                base_name=$(basename "$file")
                A=$(echo "$base_name" | cut -d'_' -f2)
                B=$(echo "$base_name" | cut -d'_' -f3 | sed 's/\.mtx$//')  # 확장자 .mtx 제거

                # 파일에서 ./data 부분 제거
                relative_file="${file#./data}"

                result=$(./main "$relative_file" "$tileSize" "$rhsCol" "1")
                
                echo $relative_file
                results+=("$tileSize,$A,$B,$i,$result")
            fi
        done

        # csv 파일에 기록
        echo "saving results to csv file"
        printf "%s\n" "${results[@]}" >> "$csv_file"

        # mtx 파일들은 모두 삭제
        rm -f $type/random_row/*.mtx
    done

    ######################################################

    ######## 실행 - rc #######
    echo "---- random_col ----"
    csv_file="${type}${subdirs[3]}.csv"

    # 데이터셋 생성
    echo "generating dataset for random_col"
    for i in {1..4}; do
        echo "set $i"
        results=()
        python3 ./util/gen.py $command_default --type rc

        # 실행시간 측정
        for file in $type/random_col/*.mtx; do
            echo $file
            if [ -f "$file" ]; then
                base_name=$(basename "$file")
                A=$(echo "$base_name" | cut -d'_' -f2)
                B=$(echo "$base_name" | cut -d'_' -f3 | sed 's/\.mtx$//')  # 확장자 .mtx 제거

                # 파일에서 ./data 부분 제거
                relative_file="${file#./data}"

                result=$(./main "$relative_file" "$tileSize" "$rhsCol" "1")
                
                echo $relative_file
                results+=("$tileSize,$A,$B,$i,$result")
            fi
        done

        # csv 파일에 기록
        echo "saving results to csv file"
        printf "%s\n" "${results[@]}" >> "$csv_file"

        # mtx 파일들은 모두 삭제
        rm -f $type/random_col/*.mtx
    done
done