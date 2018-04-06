#pragma once

// Template specialisations for interop with Rcpp

#include <cinterop/rcpp_strict_r_headers.hpp>

#include "cinterop/c_interop_forward_decl.h"
#include "cinterop/timeseries_c_interop.h"
#include "cinterop/timeseries_interop.hpp"
#include "cinterop/rcpp_interop.hpp"

using namespace Rcpp;

#define RCPP_TS_START_NAME "Start"
#define RCPP_TS_END_NAME "End"
#define RCPP_TS_LENGTH_NAME "Length"
#define RCPP_TS_TSTEPSECONDS_NAME "TimeStepSeconds"
#define RCPP_TS_GEOM_CLASSNAMENAME "RegularTimeSeriesGeometry"
#define RCPP_TS_GEOM_SLOTNAME "TsGeom"
#define RCPP_TS_ENSEMBLESIZE_SLOTNAME "EnsembleSize"
#define RCPP_TS_NUMERICDATA_SLOTNAME "NumericData"
#define RCPP_TS_MULTISERIES_CLASSNAME "RegularTimeSeries"
#define RCPP_TS_DATA_ITEMNAME "Data"
#define RCPP_TS_TIMESTEP_ITEMNAME "TimeStep"

namespace cinterop
{
	namespace rcpp
	{

		template<typename From>
		NumericMatrix to_r_numeric_matrix(const From& mts);

		template<>
		inline NumericMatrix to_r_numeric_matrix<multi_regular_time_series_data>(const multi_regular_time_series_data& mts)
		{
			size_t ensSize = mts.ensemble_size;
			if (mts.ensemble_size > 0) // NOT ensSize!
			{
				size_t length = mts.time_series_geometry.length;
				NumericMatrix m(mts.time_series_geometry.length /*nrows*/, mts.ensemble_size /*ncols*/);
				for (size_t i = 0; i < ensSize; i++)
				{
					NumericVector values = cinterop::utils::to_custom_numeric_vector<NumericVector>(mts.numeric_data[i], length, false);
					m(_, i) = values;
				}
				return m;
			}
			else {
				NumericMatrix m(1, 1);
				m(0,0) = NumericMatrix::get_na();
				return m;
			}
		}
	}

	namespace timeseries
	{
		template<>
		inline void to_regular_time_series_geometry<Rcpp::S4>(const Rcpp::S4& rTsInfo, regular_time_series_geometry& mts)
		{
			mts.start = cinterop::utils::to_date_time_to_second<Rcpp::Datetime>(rTsInfo.slot(RCPP_TS_START_NAME));
			mts.length = as<int>(rTsInfo.slot(RCPP_TS_LENGTH_NAME));
			mts.time_step_seconds = as<int>(rTsInfo.slot(RCPP_TS_TSTEPSECONDS_NAME));
		}

		template<>
		inline Rcpp::S4 from_regular_time_series_geometry<Rcpp::S4>(const regular_time_series_geometry& mts)
		{
			Rcpp::S4 rTsInfo(RCPP_TS_GEOM_CLASSNAMENAME);
			rTsInfo.slot(RCPP_TS_START_NAME) = cinterop::utils::to_posix_ct_date_time<NumericVector>(mts.start);
			rTsInfo.slot(RCPP_TS_LENGTH_NAME) = mts.length;
			rTsInfo.slot(RCPP_TS_TSTEPSECONDS_NAME) = mts.time_step_seconds;

			// 	Note that the class character itself has a list as an attribute. May be necessary, not sure yet
			return rTsInfo;
		}


		template<>
		inline multi_regular_time_series_data to_multi_regular_time_series_data<Rcpp::S4>(const Rcpp::S4& timeSeriesEnsemble)
		{
			multi_regular_time_series_data result;

			const Rcpp::S4& rTsInfo = timeSeriesEnsemble.slot(RCPP_TS_GEOM_SLOTNAME);
			result.ensemble_size = timeSeriesEnsemble.slot(RCPP_TS_ENSEMBLESIZE_SLOTNAME);
			const Rcpp::NumericMatrix& m = timeSeriesEnsemble.slot(RCPP_TS_NUMERICDATA_SLOTNAME);
			result.numeric_data = cinterop::utils::to_double_ptr_array<NumericMatrix>(m);
			result.time_series_geometry = to_regular_time_series_geometry(rTsInfo);
			return result;
		}



		template<>
		inline Rcpp::S4 from_multi_regular_time_series_data<Rcpp::S4>(const multi_regular_time_series_data& mts)
		{
			Rcpp::S4 timeSeriesEnsemble(RCPP_TS_MULTISERIES_CLASSNAME);
			timeSeriesEnsemble.slot(RCPP_TS_GEOM_SLOTNAME) = from_regular_time_series_geometry<Rcpp::S4>(mts.time_series_geometry);
			timeSeriesEnsemble.slot(RCPP_TS_ENSEMBLESIZE_SLOTNAME) = mts.ensemble_size;
			timeSeriesEnsemble.slot(RCPP_TS_NUMERICDATA_SLOTNAME) = cinterop::rcpp::to_r_numeric_matrix(mts);

			/*
			Note that the class character itself has a list as an attribute. May be necessary, not sure yet
			> attributes(attributes(blah)$class)
			$package
			[1] "mypkg"
			*/
			return timeSeriesEnsemble;
		}


		template<typename T=List> // Kludge to be header only
		T make_time_series_info(const NumericVector& data, const regular_time_series_geometry& mtsg, const string& time_zone="UTC")
		{
			IntegerVector tStep(1, mtsg.time_step_seconds);
			CharacterVector tzone(time_zone);
			return Rcpp::List::create(
				Rcpp::Named(RCPP_TS_START_NAME) = cinterop::utils::to_posix_ct_date_time<Rcpp::NumericVector>(mtsg.start),
				Rcpp::Named("tzone") = tzone,
				Rcpp::Named(RCPP_TS_DATA_ITEMNAME) = data,
				Rcpp::Named(RCPP_TS_TIMESTEP_ITEMNAME) = tStep);
		}

		template<typename T = List> // Kludge to be header only
		Rcpp::List make_regular_time_series_geometry_info(const date_time_to_second& start, const date_time_to_second& end, const string& tStep)
		{
			return Rcpp::List::create(
				Rcpp::Named(RCPP_TS_START_NAME) = cinterop::utils::to_posix_ct_date_time<Rcpp::NumericVector>(start), // we ust use cinterop::utils::to_posix_ct_date_time<Rcpp::NumericVector> since Datetime has no timezone concept that I can see.
				Rcpp::Named(RCPP_TS_END_NAME) = cinterop::utils::to_posix_ct_date_time<Rcpp::NumericVector>(end),
				Rcpp::Named(RCPP_TS_TIMESTEP_ITEMNAME) = tStep);
		}



	}
}