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
            //cout<<"tmp : "<<tmp<<endl;
        }

        //1,2번째 라인
        if(getline(inn, line)){
            istringstream ss(line);
            ss>>num_rows>>num_cols>>num_value;
            //cout<<"num_rows : "<<num_rows<<" num_cols : "<<num_cols<<" num_value : "<<num_value<<endl;
        }
        ell_blocksize = tileSize;


        /*ellCols 알아내기*/        
        float value;
        int cur_tileIdx;
        int last_row=0, last_tileIdx=-1; // 0번째 행에서 시작하기 위해 초기화 
        int cnt_tile_in_row=0; // 각 row에 포함된 tile 개수
        int max_cnt_tile_in_row = 0; // 행렬의 모든 row 중에서 가장 많은 tile을 포함한 row의 tile 개수.
        int cur_row, cur_col; //현재 row, col

        // 각 row에 대해, 몇 개의 타일이 존재하는지 파악한다.
        while(getline(inn, line)){
            istringstream ss(line);
            if(ss>>cur_row>>cur_col>>value){
                //cout<<"cur_row : "<<cur_row<<"cur_ col : "<<cur_col<<endl;

                //현재 원소가 포함된 타일
                cur_tileIdx = cur_col / ell_blocksize;

                // 이전과 동일한 행이고, 이전에 카운트한 tile에 포함되지 않은 원소이면 tile 개수를 업데이트.
                if(cur_row == last_row && last_tileIdx != cur_tileIdx){
                    last_tileIdx = cur_tileIdx;
                    cnt_tile_in_row+=1;
                }

                // 다음 행으로 넘어가면 tile개수와 현재 행을 업데이트 해준다.
                else if(cur_row != last_row){
                    max_cnt_tile_in_row = max(max_cnt_tile_in_row, cnt_tile_in_row); //이전 행의 타일 개수를 최대값과 비교하여 업데이트
                    cnt_tile_in_row=1; //새로운 행의 타일 개수는 이제 1개
                    last_row = cur_row;
                    last_tileIdx = cur_tileIdx;
                }

                arr.push_back(make_tuple(cur_row, cur_col, value, cur_tileIdx, cnt_tile_in_row-1));
            }
        }
        inn.close();
        max_cnt_tile_in_row = max(max_cnt_tile_in_row, cnt_tile_in_row); // non zero가 첫번째 row에만 존재하는 행렬을 위해
        ell_cols = max_cnt_tile_in_row * ell_blocksize;


        //메모리 할당
        ellColInd =     (int*) malloc((num_rows / ell_blocksize) * (ell_cols / ell_blocksize) * sizeof(int));
        ellValue =      (float*) malloc(num_rows * ell_cols * sizeof(float));
        //cout<<"ellColInd : "<<(num_rows / ell_blocksize) * (ell_cols / ell_blocksize)<<"  ellValue : "<<num_rows * ell_cols * sizeof(float)<<endl;
        fill(ellColInd, ellColInd+(num_rows / ell_blocksize) * (ell_cols / ell_blocksize), -1);
        fill(ellValue, ellValue + num_rows * ell_cols, 0.0f);


        last_row = 0;
        last_tileIdx=-1;
        int local_col=0;
        int ellValue_Idx; int ellColInd_Idx; int cur_tileOrder;
        for (auto data:arr){
            cur_row = get<0>(data);
            cur_col = get<1>(data);
            value   = get<2>(data);
            cur_tileIdx = get<3>(data);
            cur_tileOrder = get<4>(data);

            if(cur_row == last_row){
                //다음 블록으로 넘어갔을 때
                if(last_tileIdx != cur_tileIdx){
                    local_col = 0;
                    last_tileIdx = cur_tileIdx;
                }
            }

            else{
                last_tileIdx = cur_tileIdx;
                last_row = cur_row;
                local_col = 0;
            }

            ellValue_Idx = cur_row * ell_cols + cur_tileOrder * ell_blocksize + local_col;
            ellColInd_Idx = (cur_row / ell_blocksize) * (ell_cols / ell_blocksize) + cur_tileOrder;
            local_col += 1;

            ellValue[ellValue_Idx] = value;
            ellColInd[ellColInd_Idx] = cur_tileIdx;
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

                // cout<<"ellValue row : "<<cur_row <<" | ellValue col : "<< cur_tileOrder * ell_blocksize + local_col <<endl;
                // cout<<"ellColInd row : "<<(cur_row / ell_blocksize)<<" | ellColInd col : "<< cur_tileOrder<<" tile Idx : "<<cur_tileIdx<<endl;
