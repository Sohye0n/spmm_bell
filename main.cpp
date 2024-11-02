#include <stdio.h>
#include <iostream>
#include "bell.h"
#include "dcn.h"
#include "util.h"
#include "spmm_bell.h"
using namespace std;


int main(int argc, char* argv[]) {
    try {
        // 1. get params
        auto [filename, rhs_num_columns] = get_args(argc, argv);

        cout << "Filename: " << filename << std::endl;
        cout << "rhs_num_columns: " << rhs_num_columns << std::endl;

        // 2. prepare lhs, rhs, result matrix
        BELL lhs    = BELL(filename);
        DCN  rhs    = DCN(lhs.num_cols, rhs_num_columns, true);
        DCN  result = DCN(lhs.num_rows, rhs.num_cols, false);

        // 2.1 is BELL correct?
        lhs.print_bell();

        // 2.2 is DCN correct?
        rhs.print_value();

        // 3. spmm
        float avg_time = spmm_bell(lhs, rhs, result, 1);

        //3.1 is spmm correct?
        result.print_value();


    } catch (const exception& e) {
        cerr << e.what() << endl;
        return 1;
    }

    return 0;
}