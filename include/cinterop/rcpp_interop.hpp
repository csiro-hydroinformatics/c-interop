#pragma once

// Template specialisations for interop with Rcpp

#include <Rcpp.h>

#include "common_c_interop.h"
#include "c_interop_forward_decl.h"
#include "c_cpp_interop.hpp"

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
		inline char** to_ansi_char_array<CharacterVector>(const CharacterVector& charVec)
		{
			char** res = new char*[charVec.length()];
			for (int i = 0; i < charVec.length(); i++)
				res[i] = STRDUP(as<std::string>(charVec[i]).c_str());
			return res;
		}

		//template<typename T>
		//void free_jagged_array(T** values, int arrayLength)
		//{
		//	for (int i = 0; i < arrayLength; i++)
		//		delete[] values[i];
		//	delete[] values;
		//}

		//void free_ansi_char_array(char ** values, int arrayLength)
		//{
		//	free_jagged_array<char>(values, arrayLength);
		//}

		//void free_double_ptr_array(double** values, int arrayLength)
		//{
		//	free_jagged_array<double>(values, arrayLength);
		//}

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
		inline NumericVector to_custom_numeric_vector<NumericVector>(double* values, int length, bool cleanup)
		{
			std::vector<double> v(values, values + length);
			NumericVector data(length);
			data.assign(v.begin(), v.end());
			if (cleanup)
				delete_array(values);
			return data;
		}

		template<>
		inline date_time_to_second to_date_time_to_second<Rcpp::Datetime>(const Rcpp::Datetime& dt)
		{
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
		inline Rcpp::Datetime from_date_time_to_second<Rcpp::Datetime>(const date_time_to_second& dt)
		{
			char sf[200];
			// const std::string &fmt = "%Y-%m-%d %H:%M:%OS");
			std::sprintf(sf, "%d-%d-%d %d:%d:%d",
				dt.year,
				dt.month,
				dt.day,
				dt.hour,
				dt.minute,
				dt.second);
			auto res = Datetime(sf);
			return res;
		}

		template<typename T>
		T to_posix_ct_date_time(const date_time_to_second& dt);

		template<>
		inline Rcpp::NumericVector to_posix_ct_date_time<Rcpp::NumericVector>(const date_time_to_second& mdt)
		{
			Rcpp::Function asPOSIXct("ISOdate"); // and we need to convert to POSIXct
			NumericVector result(asPOSIXct(
				Rcpp::wrap(mdt.year),
				Rcpp::wrap(mdt.month),
				Rcpp::wrap(mdt.day),
				Rcpp::wrap(mdt.hour),
				Rcpp::wrap(mdt.minute),
				Rcpp::wrap(mdt.second),
				CharacterVector("UTC")));

			return result;
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