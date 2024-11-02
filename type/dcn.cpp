#include "dcn.h"
#include <stdint.h> 
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>

DCN::DCN(int lhs_column, int rhs_column, bool option){
    num_rows = lhs_column;
    num_cols = rhs_column;
    ldb = num_rows;

    value = (float*)malloc(num_rows * num_cols * sizeof(float));
    
    // rhs
    if(option){
        fill(value, value + num_rows * num_cols, 1.0f);
    }
    // result
    else{
        fill(value, value + num_rows * num_cols, 0.0f);
    }
}

void DCN::print_value(){
    for(int i=0; i<num_rows; i++){
        for(int j=0; j<num_cols; j++){
            printf("% .1f ",value[i*num_cols + j]);
        }
        printf("\n");
    }
}