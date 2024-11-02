#include "dcn.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>

DCN::DCN(int lhs_column, int rhs_column, bool option){
    num_rows = lhs_column;
    num_cols = rhs_column;
    ldb = num_rows;

    B_value = (float*)malloc(num_rows * num_cols * sizeof(float));
    
    // rhs
    if(option){
        fill(B_value, B_value + num_rows * num_cols, 1.0f);
    }
    // result
    else{
        fill(B_value, B_value + num_rows * num_cols, 0.0f);
    }
}