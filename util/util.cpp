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
    std::string filename = argv[1];
    
    // 두 번째 인자는 rhs_num_columns
    int rhs_num_columns = 0;
    try {
        rhs_num_columns = std::stoi(argv[2]);
    } catch (const std::invalid_argument& e) {
        throw std::invalid_argument("Error: rhs_num_columns should be an integer.");
    } catch (const std::out_of_range& e) {
        throw std::out_of_range("Error: rhs_num_columns is out of range.");
    }

    return make_tuple(filename, rhs_num_columns);
}