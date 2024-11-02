#pragma once
#include <string>
#include <stdint.h> 
using namespace std;

class BELL{
    public: 
        int num_rows;
        int num_cols;
        int ell_blocksize;
        int ell_cols;
        int num_blocks;

        int* ellColInd;
        float* ellValue;
        int* ellColInd_idx;

        BELL(string filename);
        void read_smtx(string filename);
        void print_bell();
};