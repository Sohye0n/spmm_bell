#!/bin/bash

# 1) data 디렉토리로 이동
cd data || { echo "data 디렉토리로 이동할 수 없습니다."; exit 1; }

T=0

# 2) 디렉토리 목록 가져오기
for dir in */; do
    # 디렉토리 이름에서 슬래시 제거
    dir_name="${dir%/}"
    
    # 3) 디렉토리 이름과 일치하는 CSV 파일 생성
    csv_file="${dir_name}.csv"
    touch "$csv_file"

    # 결과 값을 저장할 배열
    results=()
    
    # 4) 각 디렉토리 내부의 파일을 하나씩 처리
    for file in "$dir_name"/*; do
        if [[ -f $file ]]; then
            # 파일 이름에서 K, A, B 파싱 (예: mK_A_B)
            base_name=$(basename "$file")
            K=$(echo "$base_name" | cut -d'_' -f1 | cut -c2-)
            A=$(echo "$base_name" | cut -d'_' -f2)
            B=$(echo "$base_name" | cut -d'_' -f3 | sed 's/\.smtx$//')  # 확장자 .smtx 제거

            # main 실행하고 결과를 변수에 저장
            result=$(../main "$file" "512")
            
            # 결과를 배열에 추가
            echo "$T, $A, $B, $K, $result" 
            results+=("$T,$A,$B,$K,$result")
        fi
    done

    printf "%s\n" "${results[@]}" >> "$csv_file"

done