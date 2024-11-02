#pragma once
#include "bell.h"
#include "dcn.h"

float spmm_bell(BELL &lhs, DCN &rhs, DCN &result, int cnt);
float spmm_bell_exe(BELL &lhs, DCN &rhs, DCN &result);