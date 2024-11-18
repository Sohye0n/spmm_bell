#pragma once
#include <string>
#include <stdint.h>
#include <cuda_fp16.h>  
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
        __half* ellValue;

        BELL(string filename, int tileSize, int mode);
        void read_smtx(string filename, int tileSize);
        void print_bell();
        void update_ptr(int pannelIdx);

        ~BELL(){
            delete [] ellColInd;
            delete [] ptr;
            delete [] ellValue;
        }
};