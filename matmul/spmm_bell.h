#pragma once
#include "bell.h"
#include "dcn.h"

void copyFloatToHalf(const float* matrix_float, __half* matrix_half, int size);
void copyHalfToFloat(__half* dA_values, float* hA_values, int size);
float spmm_bell(BELL &lhs, DCN &rhs, DCN &result, int cnt);
float spmm_bell_exe(BELL &lhs, DCN &rhs, DCN &result);