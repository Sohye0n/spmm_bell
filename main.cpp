#include <stdio.h>
#include <iostream>
#include "bell.h"
#include "dcn.h"
#include "util.h"
#include "spmm_bell.h"
using namespace std;

int type(string filename){
    char target = '/';  // 찾고자 하는 특정 문자
    int type=-1;

    // 특정 문자가 등장하는 첫 번째 인덱스 찾기
    size_t pos = filename.find(target);

    // 문자가 발견되었는지 확인하고, 해당 인덱스까지 자르기
    if (pos != std::string::npos) {
        string result = filename.substr(0, pos);

        if(result == "simple_row") type=0;
        else if(result == "simple_col") type=1;
        else if(result == "random_row") type=2;
        else if(result == "random_col") type=3;

    } else {
        return -1;
    }

    return type;
}

int main(int argc, char* argv[]) {
    try {
        // 1. get params
        auto [filename, rhs_num_columns] = get_args(argc, argv);

        // 2. prepare lhs, rhs, result matrix
        BELL lhs    = BELL(filename);
        DCN  rhs    = DCN(lhs.num_cols, rhs_num_columns, true);
        DCN  result = DCN(lhs.num_rows, rhs.num_cols, false);

        // // 2.1 is BELL correct?
        // lhs.print_bell();

        // // 2.2 is DCN correct?
        // rhs.print_value();

        // 3. spmm
        float avg_time = spmm_bell(lhs, rhs, result, 1);
        printf("%f",avg_time);

        // //3.1 is spmm correct?
        // result.print_value();

        return 0;


    } catch (const exception& e) {
        cerr << e.what() << endl;
        return 1;
    }

    return 0;
}


    // "-R 5120 -C 5120 -T 32"
    // "-R 5120 -C 10240 -T 32"
    // "-R 10240 -C 5120 -T 32"
    // "-R 10240 -C 10240 -T 32"
    // "-R 10240 -C 20480 -T 32"
    // "-R 120480 -C 10240 -T 32"