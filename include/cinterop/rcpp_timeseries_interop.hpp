#pragma once

/**
 * @file rcpp_timeseries_interop.hpp
 * @author your name (you@domain.com)
 * @brief Template specialisations for interop with Rcpp of time series concepts
 * @date 2020-06-14
 * 
 * @copyright Copyright (c) 2020
 */


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
#define RCPP_TS_TSTEPCODE_NAME "TimeStepCode"
#define RCPP_TS_GEOM_CLASSNAMENAME "RegularTimeSeriesGeometry"
#define RCPP_TS_GEOM_SLOTNAME "TsGeom"
#define RCPP_TS_ENSEMBLESIZE_SLOTNAME "EnsembleSize"
#define RCPP_TS_NUMERICDATA_SLOTNAME "NumericData"
#define RCPP_TS_MULTISERIES_CLASSNAME "RegularTimeSeries"
#define RCPP_TS_DATA_ITEMNAME "Data"
#define RCPP_TS_TIMESTEP_ITEMNAME "TimeStep"
#define RCPP_TS_TIMESTEPCODE_ITEMNAME "TimeStepCode"

#define RCPP_TZONE_NAME "tzone"

#define RCPP_STAT_LENGTH_NAME "Length"
#define RCPP_STAT_SPEC_NAME "Statistics"
#define RCPP_STAT_OBSERVATIONS_NAME "Observations"

#define RCPP_STAT_VAR_ID_NAME "ModelVarId"
#define RCPP_STAT_STAT_ID_NAME "StatisticId"
#define RCPP_STAT_OBJ_ID_NAME "ObjectiveId"
#define RCPP_STAT_OBJ_NAME_NAME "ObjectiveName"

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
			mts.time_step_code = time_step_code(as<int>(rTsInfo.slot(RCPP_TS_TSTEPCODE_NAME)));
		}

		template<>
		inline Rcpp::S4 from_regular_time_series_geometry<Rcpp::S4>(const regular_time_series_geometry& mts)
		{
			Rcpp::S4 rTsInfo(RCPP_TS_GEOM_CLASSNAMENAME);
			rTsInfo.slot(RCPP_TS_START_NAME) = cinterop::utils::to_posix_ct_date_time<NumericVector>(mts.start);
			rTsInfo.slot(RCPP_TS_LENGTH_NAME) = mts.length;
			rTsInfo.slot(RCPP_TS_TSTEPCODE_NAME) = (int) mts.time_step_code;
			rTsInfo.slot(RCPP_TS_TSTEPSECONDS_NAME) = mts.time_step_seconds;

			// 	Note that the class character itself has a list as an attribute. May be necessary, not sure yet
			return rTsInfo;
		}

		template<>
		inline void to_multi_regular_time_series_data<Rcpp::S4>(const Rcpp::S4& timeSeriesEnsemble, multi_regular_time_series_data& mts)
		{
			const Rcpp::S4& rTsInfo = timeSeriesEnsemble.slot(RCPP_TS_GEOM_SLOTNAME);
			mts.ensemble_size = timeSeriesEnsemble.slot(RCPP_TS_ENSEMBLESIZE_SLOTNAME);
			const Rcpp::NumericMatrix& m = timeSeriesEnsemble.slot(RCPP_TS_NUMERICDATA_SLOTNAME);
			mts.numeric_data = cinterop::utils::to_double_ptr_array<NumericMatrix>(m);
			mts.time_series_geometry = to_regular_time_series_geometry(rTsInfo);
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
			IntegerVector tStepCode(1, (int)mtsg.time_step_code);
			IntegerVector tStep(1, mtsg.time_step_seconds);
			CharacterVector tzone(time_zone);
			return Rcpp::List::create(
				Rcpp::Named(RCPP_TS_START_NAME) = cinterop::utils::to_posix_ct_date_time<Rcpp::NumericVector>(mtsg.start),
				Rcpp::Named(RCPP_TZONE_NAME) = tzone,
				Rcpp::Named(RCPP_TS_DATA_ITEMNAME) = data,
				Rcpp::Named(RCPP_TS_TIMESTEP_ITEMNAME) = tStep,
				Rcpp::Named(RCPP_TS_TIMESTEPCODE_ITEMNAME) = tStepCode);
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
	namespace statistics
	{
		template<>
		inline statistic_definition* to_statistic_definition_ptr<S4>(const string& model_variable_id, const string& statistic_identifier, const string& objective_identifier, const string& objective_name,
			const date_time_to_second& start, const date_time_to_second& end, const S4& time_series_data)
		{
			using namespace cinterop::timeseries;
			statistic_definition* stat = new statistic_definition();
			stat->statistic_identifier = STRDUP(statistic_identifier.c_str());
			stat->start = start;
			stat->end = end;
			stat->model_variable_id = STRDUP(model_variable_id.c_str());
			stat->objective_identifier = STRDUP(objective_identifier.c_str());
			stat->objective_name = STRDUP(objective_name.c_str());
			stat->observations = to_multi_regular_time_series_data_ptr<S4>(time_series_data);
			return stat;
		}

		template<>
		inline void to_multi_statistic_definition<Rcpp::List>(const Rcpp::List& rTsInfo, multi_statistic_definition& msd)
		{
			using namespace cinterop::utils;

			rTsInfo[0];

			//NumericVector resid = as<NumericVector>(mod["residuals"]);
			//NumericVector fitted = as<NumericVector>(mod["fitted.values"]);

			msd.size = as<int>(rTsInfo[RCPP_STAT_LENGTH_NAME]);
			msd.statistics = new statistic_definition * [msd.size];

			DataFrame specs = as<DataFrame>(rTsInfo[RCPP_STAT_SPEC_NAME]);

			List observations = as<List>(rTsInfo[RCPP_STAT_OBSERVATIONS_NAME]);

			auto model_variable_id = Rcpp::as<CharacterVector>(specs[RCPP_STAT_VAR_ID_NAME]);
			auto statistic_identifier = Rcpp::as<CharacterVector>(specs[RCPP_STAT_STAT_ID_NAME]);
			auto objective_identifier = Rcpp::as<CharacterVector>(specs[RCPP_STAT_OBJ_ID_NAME]);
			auto objective_name = Rcpp::as<CharacterVector>(specs[RCPP_STAT_OBJ_NAME_NAME]);
			auto start = Rcpp::as<NumericVector>(specs[RCPP_TS_START_NAME]);
			auto end = Rcpp::as<NumericVector>(specs[RCPP_TS_END_NAME]);

			for (size_t i = 0; i < msd.size; i++)
			{
				string mvid = as<string>(model_variable_id[i]);
				string sid = as<string>(statistic_identifier[i]);
				string objid = as<string>(objective_identifier[i]);
				string objname = as<string>(objective_name[i]);
				S4 obsSeries = as<S4>(observations[i]);
				NumericVector s(1);
				s[0] = start[i];
				NumericVector e(1);
				e[0] = end[i];
				statistic_definition* stat = to_statistic_definition_ptr<S4>(
					mvid, 
					sid,
					objid,
					objname,
					to_date_time_to_second(s),
					to_date_time_to_second(e),
					obsSeries);
				msd.statistics[i] = stat;
			}

			msd.mix_statistics_id = nullptr;
		}
	}
}