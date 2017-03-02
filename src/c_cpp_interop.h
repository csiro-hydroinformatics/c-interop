#pragma once

#include "c_interop_forward_decl.h"

char** to_ansi_char_array(const std::vector<std::string>& charVec);

double* to_double_array(const std::vector<double>& dblvec);

void free_double_array(double* values, int arrayLength);

double** to_double_ptr_array(const std::vector<std::vector<double>>& mat);

void free_double_ptr_array(double** values, int arrayLength);

std::vector<std::string> to_cpp_string_vector(char** names, int size);
