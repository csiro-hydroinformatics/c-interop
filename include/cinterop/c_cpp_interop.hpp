#pragma once

#include <vector>
#include <map>
#include <functional>

#include "cinterop/common_c_interop.h"
#include "cinterop/c_interop_forward_decl.h"
#include "cinterop/object_lifetimes.hpp"

using std::vector;
using std::string;
using std::map;

namespace cinterop
{
	namespace utils
	{
		// template declarations
		template<typename S>
		char* to_ansi_string(const S& s);

		template<typename V>
		char** to_ansi_char_array(const V& charVec);

		template<typename S>
		char** to_ansi_char_array(const std::vector<S>& charVec);

		template<typename F>
		F* to_c_array(const std::vector<F>& dblvec);

		template<typename F>
		double** to_double_ptr_array(const F& mat);

		template<typename F>
		double** to_double_ptr_array(const std::vector<std::vector<F>>& mat);

		template<typename T>
		T to_custom_character_vector(char** names, int size, bool cleanup);

		template<typename N>
		N to_custom_numeric_vector(double* values, int length, bool cleanup);

		template<typename T>
		date_time_to_second to_date_time_to_second(const T& dt);

		template<typename T>
		T from_date_time_to_second(const date_time_to_second& dt);

		template<typename T = double, typename U = double>
		U* vector_to_c_array(const vector<T>& values, std::function<U(const T&)> converter, int* size = nullptr)
		{
			size_t n = values.size();
			if (size != nullptr)
				*size = static_cast<int>(n);
			if (n == 0)
				return nullptr;
			U* cArray = new U[n];
			for (size_t i = 0; i < n; i++)
			{
				U c = converter(values[i]);
				cArray[i] = c;
			}
			return cArray;
		}

		template<typename T = double>
		T* vector_identity_to_c_array(const vector<T>& values)
		{
			int* size = nullptr;
			auto identity = [](T x) {return x; };
			return cinterop::utils::vector_to_c_array<T, T>(values, identity, size);
		}

		template<typename T>
		named_values_vector to_named_values_vector(const T& x);

		template<typename T>
		void to_named_values_vector(const T& x, named_values_vector& nvv);

		template<typename T>
		T from_named_values_vector(const named_values_vector& nvv);

		template<typename T>
		T from_named_values_vector_ptr(named_values_vector* nvv, bool dispose)
		{
			T result = from_named_values_vector<T>(*nvv);
			if (dispose) cinterop::disposal::dispose_of(nvv);
			return result;
		}

		template<typename T>
		named_values_vector* to_named_values_vector_ptr(const T& x)
		{
			named_values_vector* nvv = new named_values_vector();
			to_named_values_vector<T>(x, *nvv);
			return nvv;
		}

		template<typename T = double> // hack to be header-only
		named_values_vector create_named_values_vector(const std::vector<std::string>& names, const std::vector<T>& values)
		{
			size_t n = names.size();
			named_values_vector vv;
			vv.size = n;
			vv.names = new char* [n];
			vv.values = new T[n];
			for (size_t i = 0; i < n; i++)
			{
				vv.names[i] = STRDUP(names[i].c_str());
				vv.values[i] = values[i];
			}
			return vv;
		}

		template<typename T = double> // hack to be header-only
		named_values_vector* create_named_values_vector_ptr(const std::vector<std::string>& names, const std::vector<T>& values)
		{
			named_values_vector vtmp = create_named_values_vector<double>(names, values);
			return new named_values_vector(vtmp);
		}

		template<typename T>
		string_string_map to_string_string_map(const T& x);

		template<typename T>
		T from_string_string_map(const string_string_map& x);

		template<typename T = std::string> // hack to be header-only
		string_string_map create_string_string_map(const std::vector<std::string>& names, const std::vector<T>& values)
		{
			size_t n = names.size();
			string_string_map vv;
			vv.size = n;
			vv.keys = new char*[n];
			vv.values = new char*[n];
			for (size_t i = 0; i < n; i++)
			{
				vv.keys[i] = STRDUP(names[i].c_str());
				vv.values[i] = STRDUP(values[i].c_str());
			}
			return vv;
		}

		template<typename T>
		T from_string_string_map_ptr(string_string_map* m, bool dispose)
		{
			T result = from_string_string_map<T>(*m);
			if (dispose) cinterop::disposal::dispose_of(m);
			return result;
		}

		template<typename T, typename K, typename V>
		std::map<K, V> to_map(const T& x);

		template<typename T, typename K, typename V>
		void to_columns(const T& x, std::vector<K>& k, std::vector<V>& v);

		template<typename T = double>
		T Identity(const T& x)
		{
			return x;
		}

		template<typename S = string>
		std::vector<S> to_cpp_string_vector(char** names, int size, bool cleanup = true)
		{
			std::vector<S> v(size);
			for (size_t i = 0; i < size; i++)
				v[i] = S(names[i]);
			if (cleanup)
				delete_ansi_string_array(names, size);
			return v;
		}

		template<typename F = double>
		std::vector<F> to_cpp_numeric_vector(F* values, int size, bool cleanup = false)
		{
			std::vector<F> data(values, values + size);
			if (cleanup)
				delete_array(values);
			return data;
		}

		/*
		// C interop Template specialisations for STL classes and common types
		*/

		template<>
		inline char* to_ansi_string<string>(const string& s)
		{
			// Also of interest though not used here:
			// http://stackoverflow.com/questions/347949/convert-stdstring-to-const-char-or-char?rq=1
			//
			char* c = STRDUP(s.c_str());
			return c;
		}

		template<>
		inline char** to_ansi_char_array<string>(const std::vector<string>& charVec)
		{
			char** result = new char*[charVec.size()];
			for (size_t i = 0; i < charVec.size(); i++)
			{
				result[i] = STRDUP(charVec[i].c_str());
			}
			return result;
		}

		template<>
		inline double* to_c_array<double>(const std::vector<double>& dblvec)
		{
			size_t n = dblvec.size();
			auto numArray = new double[n];
			std::copy(dblvec.begin(), dblvec.begin() + n, numArray);
			return numArray;
		}

		template<>
		inline double** to_double_ptr_array<double>(const std::vector<std::vector<double>>& mat)
		{
			double** result = new double*[mat.size()];
			for (size_t i = 0; i < mat.size(); i++)
			{
				result[i] = to_c_array<double>(mat[i]);
			}
			return result;
		}

		template<>
		inline named_values_vector to_named_values_vector<std::map<string, double>>(const std::map<string, double>& x)
		{
			named_values_vector y;
			y.size = x.size();
			y.names = new char*[y.size];
			y.values = new double[y.size];

			size_t i = 0;
			for (const auto& kv : x)
			{
				y.names[i] = to_ansi_string(kv.first);
				y.values[i] = kv.second;
				i++;
			}
			return y;
		}

		template<>
		inline string_string_map to_string_string_map<std::map<string, string>>(const std::map<string, string>& x)
		{
			string_string_map y;
			y.size = x.size();
			y.keys = new char*[y.size];
			y.values = new char*[y.size];

			size_t i = 0;
			for (const auto& kv : x)
			{
				y.keys[i] = to_ansi_string(kv.first);
				y.values[i] = to_ansi_string(kv.second);
				i++;
			}
			return y;
		}


		template<>
		inline std::map<string, double> to_map<named_values_vector,string,double>(const named_values_vector& x)
		{
			std::map<string, double> y;
			for (size_t i = 0; i < x.size; i++)
				y[string(x.names[i])] = x.values[i];
			return y;
		}

		template<>
		inline std::map<string, string> to_map<string_string_map, string, string>(const string_string_map& x)
		{
			std::map<string, string> y;
			for (size_t i = 0; i < x.size; i++)
				y[string(x.keys[i])] = x.values[i];
			return y;
		}

		template<>
		inline void to_columns<named_values_vector, string, double>(
			const named_values_vector& x, 
			std::vector<string>& k, 
			std::vector<double>& v)
		{
			k.resize(x.size);
			v.resize(x.size);
			for (size_t i = 0; i < x.size; i++)
			{
				k[i] = x.names[i];
				v[i] = x.values[i];
			}
		}

		template<>
		inline void to_columns<string_string_map, string, string>(
			const string_string_map& x,
			std::vector<string>& k,
			std::vector<string>& v)
		{
			k.resize(x.size);
			v.resize(x.size);
			for (size_t i = 0; i < x.size; i++)
			{
				k[i] = x.keys[i];
				v[i] = x.values[i];
			}
		}
	}

	namespace disposal {
		template<>
		inline void dispose_of<named_values_vector>(named_values_vector& d)
		{

			if (d.names != nullptr)
			{
				free_c_ptr_array<char>(d.names, d.size);
				d.names = nullptr;
			}

			if (d.values != nullptr)
			{
				delete[] d.values;
				d.values = nullptr;
			}
		}

		template<>
		inline void dispose_of<string_string_map>(string_string_map& d)
		{

			if (d.keys != nullptr)
			{
				free_c_ptr_array<char>(d.keys, d.size);
				d.keys = nullptr;
			}

			if (d.values != nullptr)
			{
				free_c_ptr_array<char>(d.values, d.size);
				d.values = nullptr;
			}
		}
	}
}