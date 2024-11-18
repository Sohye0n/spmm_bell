#pragma once
#include <stdint.h> 
#include <string>
#include <cuda_fp16.h>  
using namespace std;

class DCN{
    public:
        int num_rows;
        int num_cols;
        int ldb;

        __half* value;

        DCN(int lhs_column, int rhs_column, bool option);
        ~DCN(){
            delete [] value;
        }
        void print_value();
};