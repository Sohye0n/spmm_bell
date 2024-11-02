#include <stdio.h>
#include <iostream>
#include "bell.h"
#include "dcn.h"
#include "util.h"
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



    } catch (const exception& e) {
        cerr << e.what() << endl;
        return 1;
    }

    return 0;
}