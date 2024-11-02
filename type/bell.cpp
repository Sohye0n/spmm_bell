#include "bell.h"
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

void BELL::read_smtx(string filename){
    string tmp;
    ifstream inn(filename);
    int num_value = 0;
    int cur_row, cur_col; float value; int cur_tileIdx;
    int last_row=0, last_col_tile=-1, cnt=0, maxi=0; // used to find ellCols

    vector<tuple<int, int, float, int>> arr;

    if(inn.is_open()){
        
        //헤더 날리기
        string line;
        
        if(getline(inn,line)){
            istringstream ss(line);
            string tmp;
            ss>>tmp;
            cout<<"tmp : "<<tmp<<endl;
        }

        //1,2번째 라인
        if(getline(inn, line)){
            istringstream ss(line);
            ss>>num_rows>>num_cols>>num_value;
            cout<<"num_rows : "<<num_rows<<" num_cols : "<<num_cols<<" num_value : "<<num_value<<endl;
        }
        if(getline(inn, line)){
            istringstream ss(line);
            ss>>ell_blocksize;
            cout<<"ell_blocksize : "<<ell_blocksize<<endl;
        }

        //nonzero 부분
        while(getline(inn, line)){
            istringstream ss(line);
            if(ss>>cur_row>>cur_col>>value){
                // 각 row에 대해, 몇 개의 타일이 존재하는지 파악한다.
                if(cur_row == last_row && last_col_tile != cur_col / ell_blocksize){
                    last_col_tile = cur_col / ell_blocksize;
                    cnt+=1;
                }
                else if(cur_row != last_row){
                    maxi = max(maxi, cnt);
                    cnt=1;
                    last_row = cur_row;
                    last_col_tile = cur_col / ell_blocksize;
                }

                arr.push_back(make_tuple(cur_row, cur_col, value, cnt-1));
            }
        }
        inn.close();
        ell_cols = maxi * ell_blocksize;


        //메모리 할당
        ellColInd =     (int*) malloc((num_rows / ell_blocksize) * (ell_cols / ell_blocksize) * sizeof(int));
        ellValue =      (float*) malloc(num_rows * ell_cols * sizeof(float));
        fill(ellColInd, ellColInd+(num_rows / ell_blocksize) * (ell_cols / ell_blocksize), -1);
        fill(ellValue, ellValue + num_rows * ell_cols, 0.0f);


        last_row = 0;
        int last_tileIdx=-1;
        int local_col=0;
        int ellValue_Idx; int ellColInd_Idx;
        for (auto data:arr){
            cur_row = get<0>(data);
            cur_col = get<1>(data);
            value   = get<2>(data);
            cur_tileIdx = get<3>(data);

            cout<<"r : "<<cur_row<<" c : "<<cur_col<<" tileIdx : "<<cur_tileIdx<<endl;

            if(cur_row == last_row){
                
                //다음 블록으로 넘어갔을 때
                if(last_tileIdx != cur_tileIdx){
                    local_col = 0;
                    ellValue_Idx = cur_row * ell_cols + cur_tileIdx * ell_blocksize + local_col;
                    ellColInd_Idx = (cur_row / ell_blocksize) * (ell_cols / ell_blocksize) + cur_tileIdx;
                    
                    cout<<"ellValue row : "<<cur_row * ell_cols<<" | ellValue col : "<< cur_tileIdx * ell_blocksize + local_col <<endl;
                    cout<<"ellColInd row : "<<(cur_row / ell_blocksize)<<" | ellColInd col : "<< cur_tileIdx<<" tile Idx : "<<cur_tileIdx<<endl;
                    
                    last_tileIdx = cur_tileIdx;
                    local_col += 1;
                }

                //동일 블록 내일 때
                else{
                    ellValue_Idx = cur_row * ell_cols + cur_tileIdx * ell_blocksize + local_col;
                    ellColInd_Idx = (cur_row / ell_blocksize) * (ell_cols / ell_blocksize) + cur_tileIdx;
                    cout<<"ellValue row : "<<cur_row * ell_cols<<" | ellValue col : "<< cur_tileIdx * ell_blocksize + local_col <<endl;
                    cout<<"ellColInd row : "<<(cur_row / ell_blocksize)<<" | ellColInd col : "<< cur_tileIdx<<" tile Idx : "<<cur_tileIdx<<endl;
                    local_col += 1;
                }
                ellValue[ellValue_Idx] = value;
                ellColInd[ellColInd_Idx] = cur_tileIdx;

            }

            else{
                last_tileIdx = cur_tileIdx;
                last_row = cur_row;
                local_col = 0;

                ellValue_Idx = cur_row * ell_cols + cur_tileIdx * ell_blocksize + local_col;
                ellColInd_Idx = (cur_row / ell_blocksize) * (ell_cols / ell_blocksize) + cur_tileIdx;
                cout<<"ellValue row : "<<cur_row * ell_cols<<" | ellValue col : "<< cur_tileIdx * ell_blocksize + local_col <<endl;
                cout<<"ellColInd row : "<<(cur_row / ell_blocksize)<<" | ellColInd col : "<< cur_tileIdx<<" tile Idx : "<<cur_tileIdx<<endl;

                last_tileIdx = cur_tileIdx;
                local_col += 1;

                ellValue[ellValue_Idx] = value;
                ellColInd[ellColInd_Idx] = cur_tileIdx;

                
            }
        }


    }
    else{
        cerr<<"file open error : "<<strerror(errno)<<endl;
    }
}

BELL::BELL(string filename){
    //1. add directory path to filename
    string filepath = "./data/" + filename;

    //2. read smtx file
    read_smtx(filepath);
}

void BELL::print_bell(){
    // ellColInd
    int r = num_rows / ell_blocksize;
    int c = ell_cols / ell_blocksize;

    cout<<"ellColInd"<<endl;
    for(int i = 0; i < r; i++){
        for(int j = 0; j < c; j++){
            printf("%d ",ellColInd[i*c + j]);
        }
        printf("\n");
    }

    cout<<"\nellValue"<<endl;
    r = num_rows;
    c = ell_cols;
    for(int i = 0; i < r; i++){
        for(int j = 0; j < c; j++){
            printf("%.1f ",ellValue[i*c + j]);
        }
        printf("\n");
    }

}
