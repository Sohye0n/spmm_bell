#pragma once
#include "bell.h"
#include <stdint.h> 
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <tuple>
#include <filesystem>
using namespace std;

void BELL::update_ptr(int pannelIdx){
    int ptr_width = num_cols / ell_blocksize;
    int offset = pannelIdx * ptr_width;
    
    for (int i=1; i<ptr_width; i++){
        ptr[offset+i] += ptr[offset+i-1];
    }
}

void BELL::read_smtx(string filename, int tileSize){
    string tmp;
    ifstream inn(filename);
    int num_value = 0;

    vector<tuple<int, int, float, int, int>> arr;

    if(inn.is_open()){
        
        //헤더 날리기
        string line;
        
        if(getline(inn,line)){
            istringstream ss(line);
            string tmp;
            ss>>tmp;
        }

        //1,2번째 라인
        if(getline(inn, line)){
            istringstream ss(line);
            ss>>num_rows>>num_cols>>num_value;
        }
        ell_blocksize = tileSize;
        ptr = (int*)malloc((num_rows / tileSize) * (num_cols / tileSize) * sizeof(int));


        /*ellCols 알아내기*/        
        float value;
        int cur_blockIdx; 
        int cur_pannel, last_pannel;
        int last_row=0, last_blockIdx=-1; // 0번째 행에서 시작하기 위해 초기화
        int cnt_block_in_row=0; // 각 pannel에 포함된 block 개수
        int cnt_block_in_pannel=0; // 각 pannel에 포함된 block 개수
        int max_cnt_block_in_pannel = 0; // 행렬의 모든 row 중에서 가장 많은 block을 포함한 row의 block 개수.
        int cur_row, cur_col; //현재 row, col
        int ptr_width = num_cols / ell_blocksize;

        // 각 row에 대해, 몇 개의 block이 존재하는지 파악한다.
        while(getline(inn, line)){
            istringstream ss(line);
            if(ss>>cur_row>>cur_col>>value){
                //현재 원소가 포함된 block
                cur_blockIdx = cur_col / ell_blocksize;
                cur_pannel = cur_row / ell_blocksize;
                last_pannel = last_row / ell_blocksize;

                // 이전과 동일한 pannel && 카운트 한 적 없는 block -> block 개수를 업데이트.
                if(cur_pannel == last_pannel && !ptr[cur_pannel * (num_cols / ell_blocksize) + cur_blockIdx]){
                    cnt_block_in_pannel+=1;
                }
                // 다음 pannel로 넘어가면 -> block개수, 위치 업데이트.
                else if(cur_pannel != last_pannel){
                    //이전 행 관련 업데이트트
                    max_cnt_block_in_pannel = max(max_cnt_block_in_pannel, cnt_block_in_pannel);
                    update_ptr(last_pannel);
    
                    //새로운 행에 대한 처리
                    cnt_block_in_pannel=1;
                }

                // row별 non-zero 블록 개수도 따로 카운트
                if(cur_row == last_row && cur_blockIdx != last_blockIdx) cnt_block_in_row +=1;
                else if(cur_row != last_row) cnt_block_in_row = 1;
                
                ptr[cur_pannel * ptr_width + cur_blockIdx] = 1;
                last_row = cur_row;
                last_blockIdx = cur_blockIdx;
                arr.push_back(make_tuple(cur_row, cur_col, value, cur_blockIdx, cnt_block_in_row-1));
            }
        }
        //마지막 pannel에 대한 업데이트
        update_ptr(cur_row / ell_blocksize);
        max_cnt_block_in_pannel = max(max_cnt_block_in_pannel, cnt_block_in_pannel);

        //ell_cols 업데이트
        ell_cols = max_cnt_block_in_pannel * ell_blocksize;
        inn.close();


        //메모리 할당
        ellColInd =     (int*) malloc((num_rows / ell_blocksize) * (ell_cols / ell_blocksize) * sizeof(int));
        ellValue =      (float*) malloc(num_rows * ell_cols * sizeof(float));
        fill(ellColInd, ellColInd+(num_rows / ell_blocksize) * (ell_cols / ell_blocksize), -1);
        fill(ellValue, ellValue + num_rows * ell_cols, 0.0f);

        last_row = 0;
        last_blockIdx=-1;
        cur_pannel = 0;
        int ellColInd_width = ell_cols / ell_blocksize;
        int cnt_nonZeroBlock_ahead;
        int ellValue_Idx, ellColInd_Idx, cur_blockOrder;
        for (auto data:arr){
            cur_row = get<0>(data);
            cur_col = get<1>(data);
            value   = get<2>(data);
            cur_blockIdx = get<3>(data);
            cur_blockOrder = get<4>(data);

            cur_pannel = cur_row / ell_blocksize;
            cnt_nonZeroBlock_ahead = ptr[cur_pannel * ptr_width + cur_blockIdx] -1;
            ellValue_Idx = cur_row * ell_cols + cnt_nonZeroBlock_ahead * ell_blocksize + (cur_col % ell_blocksize);
            ellColInd_Idx = cur_pannel * ellColInd_width + cur_blockOrder;

            ellValue[ellValue_Idx] = value;
            ellColInd[ellColInd_Idx] = cur_blockIdx;
        }
    }
    else{
        cerr<<"file open error : "<<strerror(errno)<<"file path : "<<filename<<endl;
    }
    arr.clear();
}

BELL::BELL(string filename, int tileSize){
    //1. add directory path to filename
    string filepath =  filename;

    //2. read smtx file
    read_smtx(filepath, tileSize);
}

void BELL::print_bell(){
    // ellColInd
    int r = num_rows / ell_blocksize;
    int c = ell_cols / ell_blocksize;
    cout<<"ell_col : "<<ell_cols<<endl;

    cout<<"\n\n<ellColInd>\n"<<endl;
    for(int i = 0; i < r; i++){
        for(int j = 0; j < c; j++){
            printf("%d ",ellColInd[i*c + j]);
        }
        printf("\n");
    }

    cout<<"\n\n<ellValue>\n"<<endl;
    r = num_rows;
    c = ell_cols;
    for(int i = 0; i < r; i++){
        for(int j = 0; j < c; j++){
            printf("%.1f ",ellValue[i*c + j]);
        }
        printf("\n");
    }
}


            // cout<<"r : "<<cur_row<<" c : "<<cur_col<<" tileIdx : "<<cur_tileIdx<<" value : "<<value<<endl;

                // cout<<"ellValue row : "<<cur_row <<" | ellValue col : "<< cur_blockOrder * ell_blocksize + local_col <<endl;
                // cout<<"ellColInd row : "<<(cur_row / ell_blocksize)<<" | ellColInd col : "<< cur_blockOrder<<" tile Idx : "<<cur_tileIdx<<endl;
