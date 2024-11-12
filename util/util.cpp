#include "util.h"
#include <iostream>
#include <string>
#include <cstdlib> 
#include <tuple>
using namespace std;

tuple<string, int, int, int> get_arg(int argc, char* argv[]) {
    if (argc < 4) {
        throw std::invalid_argument("Usage: <program> <filename> <rhs_num_columns> <mode>");
    }

    string filename = argv[1];

    int tileSize = 0;
    int rhs_num_columns = 0;
    int mode = 0;
    try {
        tileSize = stoi(argv[2]);
        rhs_num_columns = stoi(argv[3]);
        mode = stoi(argv[4]);

    } catch (const invalid_argument& e) {
        throw invalid_argument("Error: rhs_num_columns should be an integer.");
    } catch (const out_of_range& e) {
        throw out_of_range("Error: rhs_num_columns is out of range.");
    }

    return make_tuple(filename, tileSize, rhs_num_columns, mode);
}