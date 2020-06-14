#pragma once

/**
 * @file rcpp_interop.hpp
 * @author your name (you@domain.com)
 * @brief specialisations to map C99 interop constructs to R (Rcpp) constructs
 * @date 2020-06-14
 * 
 * @copyright Copyright (c) 2020
 * 
 */

// Template specialisations for interop with Rcpp

#include <vector>
#include <string>
#include <map>

#include "cinterop/rcpp_strict_r_headers.hpp"

#include "cinterop/common_c_interop.h"
#include "cinterop/c_interop_forward_decl.h"
#include "cinterop/c_cpp_interop.hpp"

using namespace Rcpp;

#include "moirai/opaque_pointers.hpp"
using moirai::opaque_pointer_handle;

//void callGc()
//{
//	Rcpp::Function gc("gc");
//	gc();
//}

namespace cinterop
{
	namespace utils
	{
		template<>
		inline char* to_ansi_string<CharacterVector>(const CharacterVector& s)
		{
			std::string ss = as<std::string>(s[0]);
			return to_ansi_string<std::string>(ss);
		}

		template<>
		inline char** to_ansi_char_array<CharacterVector>(const CharacterVector& charVec)
		{
			char** res = new char*[charVec.length()];
			for (int i = 0; i < charVec.length(); i++)
				res[i] = STRDUP(as<std::string>(charVec[i]).c_str());
			return res;
		}

		template<typename M>
		double** as_double_ptr_array(M& mat);
			
		template<>
		inline double** as_double_ptr_array<NumericMatrix>(NumericMatrix& mat)
		{
			int nrow = mat.nrow();
			double** rows = new double*[nrow];
			for (int i = 0; i < nrow; i++)
			{
				rows[i] = &(mat[nrow*i]);
			}
			return rows;
		}

		template<>
		inline double** to_double_ptr_array<NumericMatrix>(const NumericMatrix& mat)
		{
			int nrow = mat.nrow();
			int ncol = mat.ncol();
			size_t length = nrow;
			double** columns = new double*[ncol];
			for (int i = 0; i < ncol; i++)
			{
				columns[i] = new double[nrow];
				NumericMatrix::ConstColumn c = mat.column(i);
				std::copy(c.begin(), c.begin() + length, columns[i]);
			}
			return columns;
		}

		template<>
		inline CharacterVector to_custom_character_vector<CharacterVector>(char** names, int size, bool cleanup)
		{
			CharacterVector v(size);
			for (int i = 0; i < size; i++)
				v[i] = std::string(names[i]);
			if (cleanup)
				delete_ansi_string_array(names, size);
			return v;
		}

		template<>
		inline Rcpp::NumericVector to_custom_numeric_vector<Rcpp::NumericVector>(double* values, int length, bool cleanup)
		{
			std::vector<double> v(values, values + length);
			Rcpp::NumericVector data(length);
			data.assign(v.begin(), v.end());
			if (cleanup)
				delete_array(values);
			return data;
		}

		template<>
		inline date_time_to_second to_date_time_to_second<Rcpp::Datetime>(const Rcpp::Datetime& dt)
		{
			// Datetime stores its values as UTC, so the following is adequate. 
			// The inverst transform requires more care as to which Datetime
			// constructor to use
			date_time_to_second d;
			d.year = dt.getYear();
			d.month = dt.getMonth();
			d.day = dt.getDay();
			d.hour = dt.getHours();
			d.minute = dt.getMinutes();
			d.second = dt.getSeconds();
			return d;
		}

		template<>
		inline date_time_to_second to_date_time_to_second<Rcpp::NumericVector>(const Rcpp::NumericVector& dt_num)
		{
			return to_date_time_to_second(Datetime(dt_num));
		}

		template<typename T>
		T to_posix_ct_date_time(const date_time_to_second& dt);

		template<>
		inline Rcpp::NumericVector to_posix_ct_date_time<Rcpp::NumericVector>(const date_time_to_second& mdt)
		{
			Rcpp::Function asPOSIXct("ISOdate"); // and we need to convert to POSIXct
			Rcpp::NumericVector result(asPOSIXct(
				Rcpp::wrap(mdt.year),
				Rcpp::wrap(mdt.month),
				Rcpp::wrap(mdt.day),
				Rcpp::wrap(mdt.hour),
				Rcpp::wrap(mdt.minute),
				Rcpp::wrap(mdt.second),
				CharacterVector("UTC")));

			return result;
		}

		template<>
		inline Rcpp::Datetime from_date_time_to_second<Rcpp::Datetime>(const date_time_to_second& dt)
		{
			//Datetime(string) seems to assume the input is in locals time 
			//	and there is no way to specify another time zone. This is bug prone, so let
			//	 us instead use to_posix_ct_date_time which is explicit with UTC
			return Datetime(to_posix_ct_date_time<Rcpp::NumericVector>(dt));
		}

		template<>
		inline Rcpp::NumericVector from_named_values_vector<Rcpp::NumericVector>(const named_values_vector& nvv)
		{
			std::vector<double> values;
			std::vector<std::string> names;
			cinterop::utils::to_columns(nvv, names, values);
			Rcpp::NumericVector v = wrap(values);
			v.names() = names;
			return v;
		}

		template<>
		inline Rcpp::NumericVector from_values_vector<Rcpp::NumericVector>(const values_vector& vv)
		{
			std::vector<double> values = from_values_vector<std::vector<double>>(vv);
			Rcpp::NumericVector v = wrap(values);
			return v;
		}

		template<>
		inline CharacterVector from_character_vector<CharacterVector>(const character_vector& cv)
		{
			std::vector<std::string> names;
			return cinterop::utils::to_custom_character_vector<CharacterVector>(cv.values, cv.size, false);
		}

		template<>
		inline CharacterVector from_string_string_map(const string_string_map& m)
		{
			std::vector<std::string> values;
			std::vector<std::string> names;
			cinterop::utils::to_columns(m, names, values);
			CharacterVector v = wrap(values);
			v.names() = names;
			return v;
		}

		template<>
		inline void to_string_string_map<CharacterVector>(const CharacterVector& x, string_string_map& m)
		{
			m.size = x.size();
			m.keys = new char* [m.size];
			m.values = new char* [m.size];
			CharacterVector c = x.names();
			size_t i = 0;
			for (const auto& kv : x)
			{
				m.keys[i] = to_ansi_string(as<std::string>(c[i]));
				m.values[i] = to_ansi_string(as<std::string>(x[i]));
				i++;
			}
		}

		template<>
		inline void to_named_values_vector<Rcpp::NumericVector>(const Rcpp::NumericVector& x, named_values_vector& vv)
		{
			int n = x.length();
			vv.size = n;
			CharacterVector c = x.names();
			vv.names = new char* [n];
			vv.values = new double[n];
			for (size_t i = 0; i < n; i++)
			{
				vv.names[i] = to_ansi_string(as<std::string>(c[i]));
				vv.values[i] = x[i];
			}
		}

		template<>
		inline void to_character_vector<CharacterVector>(const CharacterVector& x, character_vector& vv)
		{
			int n = x.length();
			vv.size = n;
			vv.values = new char* [n];
			for (size_t i = 0; i < n; i++)
				vv.values[i] = to_ansi_string(as<std::string>(x[i]));
		}
	}
#define S4_EXTERNAL_OBJ_CLASSNAME "ExternalObjRef"
#define S4_OBJ_SLOTNAME "obj"
#define S4_TYPE_SLOTNAME "type"
	template<typename T = opaque_pointer_handle>
	Rcpp::S4 create_rcpp_xptr_wrapper(const XPtr<T>& xptr, const string& type = "")
	{
		Rcpp::S4 xptrWrapper(S4_EXTERNAL_OBJ_CLASSNAME);
		xptrWrapper.slot(S4_OBJ_SLOTNAME) = xptr;
		xptrWrapper.slot(S4_TYPE_SLOTNAME) = type;
		return xptrWrapper;
	}

	template<typename T = opaque_pointer_handle>
	Rcpp::S4 create_rcpp_xptr_wrapper(void* pointer, const string& type = "")
	{
		auto xptr = XPtr<T>(new T(pointer));
		Rcpp::S4 xptrWrapper(S4_EXTERNAL_OBJ_CLASSNAME);
		xptrWrapper.slot(S4_OBJ_SLOTNAME) = xptr;
		xptrWrapper.slot(S4_TYPE_SLOTNAME) = type;
		return xptrWrapper;
	}

}