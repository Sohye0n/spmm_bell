#pragma once
#include <string>
using namespace std;

class DCN{
    public:
        int num_rows;
        int num_cols;
        int ldb;

        float* B_value;

        DCN(int lhs_column, int rhs_column, bool option);
};