#!/bin/bash

# 1104 디렉토리의 모든 하위 디렉토리(1, 2, 3, 4) 탐색
# 1104 디렉토리의 모든 하위 디렉토리 탐색
for num_dir in ./1104/*/; do
    echo "num_dir: $num_dir"  # num_dir 확인
    dir_name="${num_dir%/}"    # 마지막 슬래시 제거
    dir_name="${dir_name##*/}"  # 디렉토리 이름 추출
    echo "dir_name: $dir_name"   # dir_name 확인

    # 서브디렉토리 탐색 (a, b, c, d를 포함한 모든 서브디렉토리)
    for sub_dir in "$num_dir"*; do
        if [[ -d $sub_dir ]]; then  # 디렉토리인지 확인
            csv_file="./1104/${dir_name}_${sub_dir##*/}.csv"  # CSV 파일 이름 생성
            touch "$csv_file"        # CSV 파일 생성 또는 초기화
            results=()               # 결과 배열 초기화

            # 각 서브디렉토리의 파일 반복
            for file in "$sub_dir"/*; do
                #echo $file
                if [[ -f $file ]]; then
                    base_name=$(basename "$file")
                    K=$(echo "$base_name" | cut -d'_' -f1 | cut -c2-)
                    A=$(echo "$base_name" | cut -d'_' -f2)
                    B=$(echo "$base_name" | cut -d'_' -f3 | sed 's/\.smtx$//')  # .smtx 확장자 제거

                    relative_file="/${file#./1104/}"  # 상대 경로 가져오기

                    #main 프로그램 실행 및 결과 캡처
                    result=$(./main "$relative_file" "512")
                    
                    #결과 배열에 추가
                    echo $relative_file
                    results+=("$dir_name,$A,$B,$K,$result")
                fi
            done

            # 결과를 CSV 파일에 기록
            printf "%s\n" "${results[@]}" >> "$csv_file"
        fi
    done
done
