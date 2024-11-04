#pragma once

/**
 * @file c_cpp_interop.hpp
 * @author your name (you@domain.com)
 * @brief specialisations to map C99 interop constructs to C++ constructs
 * @date 2020-06-14
 * 
 * @copyright Copyright (c) 2020
 * 
 */

#include <string>
#include <vector>
#include <map>
#include <functional>
#include <stdexcept>
#include <iostream>
#include <sstream>

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

		/**
		 * @brief Template declaration for specific objects convertible to an ANSI character array representation.
		 * 
		 * @tparam S type of the source object to convert
		 * @param s object to convert
		 * @return char* 
		 */
		template<typename S>
		char* to_ansi_string(const S& s);

		/**
		 * @brief Template declaration for objects convertible to a representation as an array of ANSI character array
		 * 
		 * @details This template declaration is useful for source objects such as Rcpp::CharacterVector 
		 * 
		 * @tparam V type of the source object to convert
		 * @param charVec object to convert
		 * @return char** 
		 */
		template<typename V>
		char** to_ansi_char_array(const V& charVec);

		/**
		 * @brief Template declaration for vector of objects convertible to a representation as an array of ANSI character array
		 * 
		 * @tparam S type of the elements in the source vectors
		 * @param charVec vector of object to convert
		 * @return char** 
		 */
		template<typename S>
		char** to_ansi_char_array(const std::vector<S>& charVec);

		template<typename F>
		F* to_c_array(const std::vector<F>& dblvec);

		template<typename F>
		double** to_double_ptr_array(const F& mat);

		template<typename F>
		double** to_double_ptr_array(const std::vector<std::vector<F>>& mat);

		/**
		 * @brief convert an array of ANSI strings to a custom representation, 
		 * typically in a higher level language such as R for instance Rcpp::CaracterVector
		 * 
		 * @tparam T type of object to convert to 
		 * @param names source array of ANSI strings
		 * @param size size of the array of ANSI strings
		 * @param cleanup if True, the caller requests the input 'names' argument to be disposed 
		 * of by this function. This is appropriate when the caller knows that the array of ANSI 
		 * strings was created in the module called, for instance in transient operation in glue 
		 * code for conciseness.
		 * 
		 * @details This can be used in glue code such as the following:
		 * @code{.cpp}
		 * // [[Rcpp::export]]
		 * CharacterVector GetPlayedVariableNames_Rcpp(XPtr<opaque_pointer_handle> simulation)
		 * {
		 *     int size; 
		 *     char** values = GetPlayedVariableNames(simulation->get(),  &size);
		 *     return to_custom_character_vector<CharacterVector>(values, size, true);
		 * }
		 * @endcode
		 * 
		 * @return T 
		 */
		template<typename T>
		T to_custom_character_vector(char** names, int size, bool cleanup);

		/**
		 * @brief convert an C numeric array to a custom representation, 
		 * typically in a higher level language such as R for instance Rcpp::CaracterVector
		 * 
		 * @tparam N type of object to convert to 
		 * @param values source C numeric array
		 * @param length size of the C numeric array
		 * @param cleanup if True, the caller requests the input 'values' argument to be disposed 
		 * of by this function. This is appropriate when the caller knows that the array of values 
		 * was created in the module called, for instance in transient operation in glue 
		 * code for conciseness.
		 * 
		 * @details This can be used in glue code such as the following:
		 * @code{.cpp}
		 * NumericVector GetPlayedData(XPtr<opaque_pointer_handle> simulation, CharacterVector variableIdentifier, MarshaledTsGeometry& mtsg)
		 * {
		 *     GetPlayedTsGeometry(simulation->get(), variableIdentifier[0], &mtsg);
		 *     double * values = new double[mtsg.length];
		 *     GetPlayed(simulation->get(), variableIdentifier[0], values, mtsg.length);
		 *     NumericVector data = to_custom_numeric_vector<NumericVector>(values, mtsg.length, false);
		 *     delete[] values;
		 *     return data;
		 * }
		 * @endcode
		 * 
		 */
		template<typename N>
		N to_custom_numeric_vector(double* values, int length, bool cleanup);

		template<typename T>
		date_time_to_second to_date_time_to_second(const T& dt);

		template<typename T>
		T from_date_time_to_second(const date_time_to_second& dt);

		/**
		 * @brief Templates for functions that transform values in an STL vectors, and returned as a C99-style array
		 * 
		 * @tparam T type of the elements in the source array
		 * @tparam U type of the elements in the resulting C array
		 * @param values source vector 
		 * @param converter function converting source T elements to resulting elements of type U
		 * @param size [out] size of the resulting C-array
		 * @return U* 
		 * @details The primary intent of this template is to have a vectorised syntax 
		 * for the conversion of multidimensional arrays. The following example converts STL 
		 * vectors of vectors of strings to C-style a char*** array.
		 * @code{.cpp}
		 * template<typename S = string>
		 * char*** str_vector_vector_to_char_arrays(const vector<vector<S>>& data, int* size)
		 * {
		 * 	std::function<char**(const vector<S>& x)> conv = [](const vector<S>& x) {return cinterop::utils::to_ansi_char_array<S>(x); };
		 * 	return cinterop::utils::vector_to_c_array<vector<S>, char**>(data, conv, size);
		 * }
		 * @endcode
		 */
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

		/**
		 * @brief Template for conversion to a value_vector struct
		 * 
		 */
		template<typename T>
		values_vector to_values_vector(const T& x);

		/**
		 * @brief Template for conversion to a value_vector struct
		 * 
		 */
		template<typename T>
		void to_values_vector(const T& x, values_vector& vv);

		/**
		 * @brief Template for conversions from a value_vector struct
		 * 
		 */
		template<typename T>
		T from_values_vector(const values_vector& vv);

		template<typename T>
		T from_values_vector_ptr(values_vector* vv, bool dispose)
		{
			T result = from_values_vector<T>(*vv);
			if (dispose) cinterop::disposal::dispose_of(vv);
			return result;
		}

		template<typename T>
		values_vector* to_values_vector_ptr(const T& x)
		{
			values_vector* vv = new values_vector();
			to_values_vector<T>(x, *vv);
			return vv;
		}

		template<>
		inline std::vector<double> from_values_vector<std::vector<double>>(const values_vector& vv)
		{
			std::vector<double> values(vv.size);
			values.assign(vv.values, vv.values + vv.size);
			return values;
		}

		template<typename T>
		void to_character_vector(const T& x, character_vector& charv);

		template<typename T>
		T from_character_vector(const character_vector& charv);

		template<typename T>
		T from_character_vector_ptr(character_vector* charv, bool dispose)
		{
			T result = from_character_vector<T>(*charv);
			if (dispose) cinterop::disposal::dispose_of(charv);
			return result;
		}

		template<typename T>
		character_vector* to_character_vector_ptr(const T& x)
		{
			character_vector* charv = new character_vector();
			to_character_vector<T>(x, *charv);
			return charv;
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

		template<typename T = double> // hack to be header-only
		values_vector create_values_vector(const std::vector<T>& values)
		{
			size_t n = values.size();
			values_vector vv;
			vv.size = n;
			vv.values = new T[n];
			for (size_t i = 0; i < n; i++)
			{
				vv.values[i] = values[i];
			}
			return vv;
		}

		template<typename T = double> // hack to be header-only
		values_vector* create_values_vector_ptr(const std::vector<T>& values)
		{
			values_vector vtmp = create_values_vector<double>(values);
			return new values_vector(vtmp);
		}

		template<typename T>
		void to_string_string_map(const T& x, string_string_map& m);

		template<typename T>
		string_string_map to_string_string_map(const T& x)
		{
			string_string_map m;
			to_string_string_map(x, m);
			return m;
		}

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

		template<typename T>
		string_string_map* to_string_string_map_ptr(const T& from)
		{
			string_string_map* m = new string_string_map();
			to_string_string_map<T>(from, *m);
			return m;
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
		inline char* to_ansi_string<std::string>(const string& s)
		{
			// Also of interest though not used here:
			// http://stackoverflow.com/questions/347949/convert-stdstring-to-const-char-or-char?rq=1
			//
			char* c = STRDUP(s.c_str());
			return c;
		}

		template<>
		inline char** to_ansi_char_array<std::string>(const std::vector<std::string>& charVec)
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
		inline named_values_vector to_named_values_vector<std::map<std::string, double>>(const std::map<std::string, double>& x)
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
		inline values_vector to_values_vector<std::vector<double>>(const std::vector<double>& x)
		{
			return create_values_vector<double>(x);
		}

		template<>
		inline void to_string_string_map<std::map<std::string, std::string>>(const std::map<std::string, std::string>& x, string_string_map& y)
		{
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
		}

		template<>
		inline std::map<std::string, double> to_map<named_values_vector,string,double>(const named_values_vector& x)
		{
			std::map<std::string, double> y;
			for (size_t i = 0; i < x.size; i++)
				y[string(x.names[i])] = x.values[i];
			return y;
		}

		template<>
		inline std::map<std::string, std::string> to_map<string_string_map, std::string, std::string>(const string_string_map& x)
		{
			std::map<std::string, std::string> y;
			for (size_t i = 0; i < x.size; i++)
				y[string(x.keys[i])] = x.values[i];
			return y;
		}

		template<>
		inline std::map<std::string, std::string> from_string_string_map(const string_string_map& x)
		{
			return to_map<string_string_map, std::string, std::string>(x);
		}

		template<>
		inline void to_columns<named_values_vector, std::string, double>(
			const named_values_vector& x, 
			std::vector<std::string>& k, 
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
		inline void to_columns<string_string_map, std::string, std::string>(
			const string_string_map& x,
			std::vector<std::string>& k,
			std::vector<std::string>& v)
		{
			k.resize(x.size);
			v.resize(x.size);
			for (size_t i = 0; i < x.size; i++)
			{
				k[i] = x.keys[i];
				v[i] = x.values[i];
			}
		}

		template<>
		inline void to_character_vector<vector<std::string>>(const vector<std::string>& x, character_vector& charv)
		{
			charv.size = x.size();
			charv.values = new char* [x.size()];
			for (size_t i = 0; i < x.size(); i++)
				charv.values[i] = STRDUP(x[i].c_str());
		}

		template<>
		inline vector<std::string> from_character_vector(const character_vector& charv)
		{
			vector<std::string> x;
			for (size_t i = 0; i < charv.size; i++)
				x.push_back(string(charv.values[i]));
			return x;
		}

		template<>
		inline void to_values_vector<std::vector<double>>(const std::vector<double>& x, values_vector& vv)
		{
			int n = x.size();
			vv.size = n;
			vv.values = new double[n];
			for (size_t i = 0; i < n; i++)
			{
				vv.values[i] = x[i];
			}
		}

		template<>
		inline std::map<std::string, double> from_named_values_vector<std::map<std::string, double>>(const named_values_vector& nvv)
		{
			std::vector<double> values;
			std::vector<std::string> names;
			cinterop::utils::to_columns(nvv, names, values);
			std::map<std::string, double> v;
			for (size_t i = 0; i < names.size(); i++)
				if (v.find(names[i]) == v.end())
					v[names[i]] = values[i];
				else
				{
					std::stringstream ss;
					ss << "Duplicate key " << names[i] << " found in the named_values_vector. This cannot be converted to a C++ std::map<string,double>.";
					throw std::logic_error(ss.str());
				}
			return v;
		}

		// Parse a string and cast to a target type.
		// There appears not to be any equivalent to boost::lexical_cast (TBC for c++14 and later).
		template <typename T>
		T parse(const string& str);

		template<>
		inline double parse<double>(const string& str)
		{
			return std::stod(str);
		}

		template<>
		inline int parse<int>(const string& str)
		{
			return std::stoi(str);
		}

		template<>
		inline string parse<std::string>(const string& str)
		{
			return str;
		}

		template<typename K = string, typename V = string>
		bool has_key(const std::map<K, V>& dict, const string& key)
		{
			return (dict.find(key) != dict.end());
		}

		template <typename T>
		T get_optional_parameter(const string& key, const std::map<std::string, T>& params, T fallback)
		{
			if (has_key<std::string, T>(params, key))
				return params.at(key);
			else
				return fallback;
		}

		template <typename T>
		T get_mandatory_parameter(const std::map<std::string, T>& params, const string& key)
		{
			if (!has_key<std::string, T>(params, key))
				throw std::logic_error("Mandatory key expected in the dictionary but not found: " + key);
			return params.at(key);
		}

		template <typename U>
		U parse_kwarg(const string& key, const std::map<std::string, std::string>& params, bool optional, U fallback)
		{
			if (!has_key<std::string, std::string>(params, key))
			{
				if (optional)
					return fallback;
				else
					throw std::logic_error("Mandatory key expected in the dictionary but not found: " + key);
			}
			else
			{
				return parse<U>(params.at(key));
			}
		}
	}

	namespace disposal {
		template<>
		inline void dispose_of<values_vector>(values_vector& d)
		{
			if (d.values != nullptr)
			{
				delete[] d.values;
				d.values = nullptr;
			}
		}

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
		inline void dispose_of<character_vector>(character_vector& d)
		{
			if (d.values != nullptr)
			{
				free_c_ptr_array<char>(d.values, d.size);
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