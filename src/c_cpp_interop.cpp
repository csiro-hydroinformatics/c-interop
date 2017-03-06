
#include "c_cpp_interop.h"

char** to_ansi_char_array(const std::vector<std::string>& charVec)
{
	char** result = new char*[charVec.size()];
	for (size_t i = 0; i < charVec.size(); i++)
	{
		result[i] = STRDUP(charVec[i].c_str());
	}
	return result;
}

double* to_double_array(const std::vector<double>& dblvec)
{
	int n = dblvec.size();
	auto numArray = new double[n];
	std::copy(dblvec.begin(), dblvec.begin() + n, numArray);
	return numArray;
}

void free_double_array(double* values, int arrayLength)
{
	delete values;
}

double** to_double_ptr_array(const std::vector<std::vector<double>>& mat)
{
	double** result = new double*[mat.size()];
	for (size_t i = 0; i < mat.size(); i++)
	{
		result[i] = to_double_array(mat[i]);
	}
	return result;
}

void free_double_ptr_array(double** values, int arrayLength)
{
	for (int i = 0; i < arrayLength; i++)
		delete[] values[i];
	delete[] values;
}

std::vector<std::string> to_cpp_string_vector(char** names, int size, bool cleanup)
{
	std::vector<std::string> v(size);
	for (size_t i = 0; i < size; i++)
		v[i] = std::string(names[i]);
	if (cleanup)
		delete_ansi_string_array(names, size);
	return v;
}

std::vector<double> to_cpp_double_vector(double* values, int size, bool cleanup)
{
	std::vector<double> data(values, values + size);
	if (cleanup)
		delete_array(values);
	return data;
}

