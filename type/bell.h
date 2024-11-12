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
        int* ptr;
        float* ellValue;

        BELL(string filename, int tileSize, int mode);
        void read_smtx(string filename, int tileSize);
        void print_bell();
        void update_ptr(int pannelIdx);
};