#pragma once
#include <stdint.h> 
#include <string>
using namespace std;

class DCN{
    public:
        int num_rows;
        int num_cols;
        int ldb;

        float* value;

        DCN(int lhs_column, int rhs_column, bool option);
        void print_value();
};