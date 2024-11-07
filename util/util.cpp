#include "util.h"
#include <iostream>
#include <string>
#include <cstdlib> 
#include <tuple>
using namespace std;

tuple<string, int> get_args(int argc, char* argv[]) {
    if (argc < 3) {
        throw std::invalid_argument("Usage: <program> <filename> <rhs_num_columns>");
    }

    // 첫 번째 인자는 filename
    string filename = argv[1];

    
    // 두 번째 인자는 rhs_num_columns
    int rhs_num_columns = 0;
    try {
        rhs_num_columns = stoi(argv[2]);
    } catch (const invalid_argument& e) {
        throw invalid_argument("Error: rhs_num_columns should be an integer.");
    } catch (const out_of_range& e) {
        throw out_of_range("Error: rhs_num_columns is out of range.");
    }

    return make_tuple(filename, rhs_num_columns);
}