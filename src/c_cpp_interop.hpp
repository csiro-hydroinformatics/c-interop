#pragma once

#include <vector>
#include <functional>
#include <boost/date_time/gregorian/gregorian.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>

#include "common_c_interop.h"
#include "c_interop_forward_decl.h"

using std::vector;

namespace cinterop
{
	namespace utils
	{
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

		//char* ToCStr(const string& s);

		template<typename T = double>
		T Identity(const T& x)
		{
			return x;
		}

		using namespace boost::gregorian;
		using namespace boost::posix_time;

		template<typename S = std::string>
		char** to_ansi_char_array(const std::vector<S>& charVec)
		{
			char** result = new char*[charVec.size()];
			for (size_t i = 0; i < charVec.size(); i++)
			{
				result[i] = STRDUP(charVec[i].c_str());
			}
			return result;
		}

		template<typename F = double>
		F* to_c_array(const std::vector<F>& dblvec)
		{
			int n = dblvec.size();
			auto numArray = new F[n];
			std::copy(dblvec.begin(), dblvec.begin() + n, numArray);
			return numArray;
		}

		template<typename F = double>
		void free_c_array(F* values, int arrayLength)
		{
			delete values;
		}

		template<typename F = double>
		F** to_double_ptr_array(const std::vector<std::vector<F>>& mat)
		{
			F** result = new F*[mat.size()];
			for (size_t i = 0; i < mat.size(); i++)
			{
				result[i] = to_c_array<F>(mat[i]);
			}
			return result;
		}

		template<typename F = double>
		void free_c_ptr_array(F** values, int arrayLength)
		{
			for (int i = 0; i < arrayLength; i++)
				delete[] values[i];
			delete[] values;
		}

		template<typename S = std::string>
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

		template<typename T = ptime>
		date_time_to_second to_date_time_to_second(const T& dt)
		{
			date_time_to_second tt;
			to_date_time_to_second(dt, tt);
			return tt;
		}

	}
}