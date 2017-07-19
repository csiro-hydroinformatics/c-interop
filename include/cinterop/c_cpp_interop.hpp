#pragma once

#include <vector>
#include <functional>
#include <boost/date_time/gregorian/gregorian.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>

#include "cinterop/common_c_interop.h"
#include "cinterop/c_interop_forward_decl.h"
#include "cinterop/object_lifetimes.hpp"

using std::vector;
using std::string;

using namespace boost::posix_time;

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

		template<typename date_int_type = uint32_t>
		ptime as_ptime(date_int_type year, date_int_type month, date_int_type day, date_int_type hour = 0, date_int_type minute = 0, date_int_type second = 0)
		{
			return ptime(date(year, month, day), hours(hour) + minutes(minute) + seconds(second));
		}

		template<typename T>
		date_time_to_second to_date_time_to_second(const T& dt);

		template<typename T>
		T from_date_time_to_second(const date_time_to_second& dt);

		template<typename T = double, typename U = double>
		U* vector_to_c_array(const vector<T>& values, std::function<U(const T&)> converter, int* size = nullptr)
		{
			int n = values.size();
			if (size != nullptr)
				*size = n;
			if (n == 0)
				return nullptr;
			U* cArray = new U[n];
			for (int i = 0; i < n; i++)
			{
				U c = converter(values[i]);
				cArray[i] = c;
			}
			return cArray;
		}

		template<typename T>
		named_values_vector to_named_values_vector(const T& x);

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

		// date-time interop
		using namespace boost::gregorian;
		using namespace boost::posix_time;
		
		template<typename T = ptime>
		T to_ptime(const date_time_to_second& dt)
		{
			return T(date(dt.year, dt.month, dt.day), hours(dt.hour) + minutes(dt.minute) + seconds(dt.second));
		}

		template<typename T = ptime>
		void to_date_time_to_second(const T& dt, date_time_to_second& tt)
		{
			if (dt.is_not_a_date_time())
				throw std::invalid_argument("to_date_time_to_second cannot handle value not_a_datetime");
			auto d = dt.date();
			tt.year = d.year();
			tt.month = d.month();
			tt.day = d.day();
			auto t = dt.time_of_day();
			tt.hour = t.hours();
			tt.minute = t.minutes();
			tt.second = t.seconds();
		}


		/*
		// C interop Template specialisations for STL classes and common types
		*/

		/**
		 * \brief	interop template specialization for boost ptime
		 */
		template<>
		inline date_time_to_second to_date_time_to_second<ptime>(const ptime& dt)
		{
			date_time_to_second tt;
			to_date_time_to_second(dt, tt);
			return tt;
		}

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
		inline std::map<string, double> to_map<named_values_vector,string,double>(const named_values_vector& x)
		{
			std::map<string, double> y;
			for (size_t i = 0; i < x.size; i++)
				y[string(x.names[i])] = x.values[i];
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
	}
}