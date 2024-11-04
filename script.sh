# #!/bin/bash

# T=0

# # 2) 디렉토리 목록 가져오기
# for dir in ./data/*/; do
#     # 디렉토리 이름에서 슬래시 제거
#     dir_name="${dir%/}"
#     dir_name="${dir_name##*/}"
    
#     # 3) 디렉토리 이름과 일치하는 CSV 파일 생성
#     csv_file="${dir_name}.csv"
#     touch "./data/$csv_file"

#     # 결과 값을 저장할 배열
#     results=()
    
#     # 4) 각 디렉토리 내부의 파일을 하나씩 처리
#     for file in "./data/$dir_name"/*; do
#         if [[ -f $file ]]; then
#             # 파일 이름에서 K, A, B 파싱 (예: mK_A_B)
#             base_name=$(basename "$file")
#             K=$(echo "$base_name" | cut -d'_' -f1 | cut -c2-)
#             A=$(echo "$base_name" | cut -d'_' -f2)
#             B=$(echo "$base_name" | cut -d'_' -f3 | sed 's/\.smtx$//')  # 확장자 .smtx 제거

#             relative_file="${file#./data}"

#             # main 실행하고 결과를 변수에 저장
#             result=$(./main "$relative_file" "512")
            
#             # 결과를 배열에 추가
#             results+=("$T,$A,$B,$K,$result")
#         fi
#     done

#     printf "%s\n" "${results[@]}" >> "$csv_file"

# done


#!/bin/bash


options=(
    "-R 5120 -C 5120 -T 32"
    "-R 5120 -C 10240 -T 32"
    "-R 10240 -C 5120 -T 32"
    "-R 10240 -C 10240 -T 32"
 )

for opt in "${options[@]}"; do
    python3 ./util/gen.py $opt
    echo "./util/gen.py $opt"

    T=$(echo "$opt" | grep -oP "(?<=-T )\d+")
    R=$(echo "$opt" | grep -oP "(?<=-R )\d+")
    C=$(echo "$opt" | grep -oP "(?<=-C )\d+")

    for dir in ./data/*/; do
        dir_name="${dir%/}"
        dir_name="${dir_name##*/}"
        
        csv_file="./data/${dir_name}.csv"
        touch "$csv_file"

        results=()
        
        for file in "./data/$dir_name"/*; do
            if [[ -f $file ]]; then
                base_name=$(basename "$file")
                K=$(echo "$base_name" | cut -d'_' -f1 | cut -c2-)
                A=$(echo "$base_name" | cut -d'_' -f2)
                B=$(echo "$base_name" | cut -d'_' -f3 | sed 's/\.smtx$//')  # 확장자 .smtx 제거

                relative_file="${file#./data}"

                result=$(./main "$relative_file" "512")
                
                echo $relative_file
                results+=("$T,$A,$B,$K,$result")
            fi
        done

        printf "%s\n" "${results[@]}" >> "$csv_file"
    done

    new_dir="./${T}_${R}x${C}"
    mkdir -p "$new_dir"

    for item in ./data/*; do
        if [[ "$item" != "$new_dir" ]]; then
            mv "$item" "$new_dir/"
        fi
    done

    rm -rf ./data/*
done
