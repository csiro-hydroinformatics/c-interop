#pragma once

#include <string>
#include "cinterop/timeseries_c_interop.h"
#include "cinterop/object_lifetimes.hpp"

using std::string;

namespace cinterop
{
	namespace timeseries
	{

		/**
		 * \brief	templates for functions converting one time series representation into a #regular_time_series_geometry C interop struct
		 * 
		 * \tparam	From	The type of time series to transform from, for example an R list
		 * \param rTsInfo	Time series source representation
		 * \param mts	[out] mts heap or stack allocated struct; beware to choose appropriately how to dispose of it depending on its allocation. 
		 */
		template<typename From>
		void to_regular_time_series_geometry(const From& rTsInfo, regular_time_series_geometry& mts);

		/**
		 * \brief	template for functions converting from a #regular_time_series_geometry C interop struct to another representation.
		 * 
		 * \tparam	To	The type of time series to transform to, for example an R list
		 * \param mts	[in] mts heap or stack allocated struct; beware to choose appropriately how to dispose of it depending on its allocation. 
		 * 
		 * \return  the time series in its target representation (which should have a copy or move constructor and assigment operator)
		 */
		template<typename To>
		To from_regular_time_series_geometry(const regular_time_series_geometry& mts);

		/**
		 * \brief	templates for functions converting one time series representation into a #regular_time_series_geometry C interop struct
		 * 
		 * \tparam	From	The type of time series to transform from, for example an R list
		 * \param rTsInfo	Time series source representation
		 * 
		 * \return  the time series in its target representation (which should have a copy or move constructor and assigment operator)
		 */
		template<typename From>
		regular_time_series_geometry to_regular_time_series_geometry(const From& rTsInfo)
		{
			regular_time_series_geometry mts;
			to_regular_time_series_geometry(rTsInfo, mts);
			return mts;
		}

		/**
		 * \brief	templates for functions converting one time series representation into a #regular_time_series_geometry C interop struct
		 * 
		 * \tparam	From	The type of time series to transform from, for example an R list
		 * \param rTsInfo	Time series source representation
		 * 
		 * \return  pointer to heap allocated time series in its target representation
		 */
		template<typename From>
		regular_time_series_geometry* to_regular_time_series_geometry_ptr(const From& rTsInfo)
		{
			regular_time_series_geometry* mts = new regular_time_series_geometry();
			to_regular_time_series_geometry(rTsInfo, *mts);
			return mts;
		}

		/**
		 * \brief	templates for functions converting one time series representation into a #multi_regular_time_series_data C interop struct
		 * 
		 * \tparam	From	The type of time series to transform from, for example an R list
		 * \param timeSeriesEnsemble	Time series source representation
		 * 
		 * \return  the time series in its target representation (which should have a copy or move constructor and assigment operator)
		 */
		template<typename From>
		multi_regular_time_series_data to_multi_regular_time_series_data(const From& timeSeriesEnsemble);

		/**
		 * \brief	templates for functions converting one time series representation into a #multi_regular_time_series_data C interop struct
		 * 
		 * \tparam	From	The type of time series to transform from, for example an R list
		 * \param rTsInfo	Time series source representation
		 * \param m	[out] mts heap or stack allocated struct; beware to choose appropriately how to dispose of it depending on its allocation. 
		 */
		template<typename From>
		void to_multi_regular_time_series_data(const From& timeSeriesEnsemble, multi_regular_time_series_data& m);

		/**
		 * \brief	templates for functions converting one time series representation into a #multi_regular_time_series_data C interop struct
		 * 
		 * \tparam	From	The type of time series to transform from, for example an R list
		 * \param timeSeriesEnsemble	Time series source representation
		 * 
		 * \return  the time series in its target representation (which should have a copy or move constructor and assigment operator)
		 * \return  pointer to heap allocated time series in its target representation
		 */
		template<typename From>
		multi_regular_time_series_data* to_multi_regular_time_series_data_ptr(const From& timeSeriesEnsemble)
		{
			multi_regular_time_series_data* m = new multi_regular_time_series_data();
		    to_multi_regular_time_series_data(timeSeriesEnsemble, *m);
			return m;
		}

		/**
		 * \brief	template for functions converting from a #multi_regular_time_series_data C interop struct to another representation.
		 * 
		 * \tparam	To	The type of time series to transform to, for example an R list
		 * \param mts	[in] mts heap or stack allocated struct; beware to choose appropriately how to dispose of it depending on its allocation. 
		 * 
		 * \return  the time series in its target representation (which should have a copy or move constructor and assigment operator)
		 */
		template<typename To>
		To from_multi_regular_time_series_data(const multi_regular_time_series_data& mts);

	}
	namespace statistics
	{
		/**
		 * \brief	templates for functions converting one statistics representation into a #multi_statistic_definition C interop struct
		 * 
		 * \tparam	From	The type of statistics representation to transform from, for example an R S4 object
		 * \param stat_defn	Statistics source representation
		 * \param mts	[out] msd heap or stack allocated struct; beware to choose appropriately how to dispose of it depending on its allocation. 
		 */
		template<typename From>
		void to_multi_statistic_definition(const From& stat_defn, multi_statistic_definition& msd);
			
		/**
		 * \brief	templates for functions converting one statistics representation into a #multi_statistic_definition C interop struct
		 * 
		 * \tparam	From	The type of statistics representation to transform from, for example an R S4 object
		 * \param definition	Statistics source representation
		 * \return	[out] pointer to heap allocated struct
		 */
		template<typename From>
		multi_statistic_definition* to_multi_statistic_definition_ptr(const From& definition)
		{
			multi_statistic_definition* mts = new multi_statistic_definition();
			to_multi_statistic_definition(definition, *mts);
			return mts;
		}

		template<typename From>
		statistic_definition* to_statistic_definition_ptr(const std::string& model_variable_id, const std::string& statistic_identifier, const std::string& objective_identifier, const std::string& objective_name,
			const date_time_to_second& start, const date_time_to_second& end, const From& time_series_data);
		// Tried to have a default implementation and relying on finding an implementation for to_multi_regular_time_series_data_ptr<From> but had issues getting this working. 
		//{
		//	using namespace cinterop::timeseries;
		//	statistic_definition* stat = new statistic_definition();
		//	stat->statistic_identifier = STRDUP(statistic_identifier.c_str());
		//	stat->start = start;
		//	stat->end = end;
		//	stat->model_variable_id = STRDUP(model_variable_id.c_str());
		//	stat->objective_identifier = STRDUP(objective_identifier.c_str());
		//	stat->objective_name = STRDUP(objective_name.c_str());
		//	stat->observations = to_multi_regular_time_series_data_ptr<From>(time_series_data);
		//	return stat;
		//}
	}

	namespace disposal {
		template<>
		inline void dispose_of<multi_regular_time_series_data>(multi_regular_time_series_data& d)
		{
			if (d.numeric_data != nullptr)
			{
				for (int i = 0; i < d.ensemble_size; i++)
					if (d.numeric_data[i] != nullptr)
					{
						delete[] d.numeric_data[i];
						d.numeric_data[i] = nullptr;
					}
				delete[] d.numeric_data;
				d.numeric_data = nullptr;
			}
		}

		template<>
		inline void dispose_of<time_series_dimensions_description>(time_series_dimensions_description& d)
		{
			for (int i = 0; i < d.num_dimensions; i++)
			{
				auto p = d.dimensions[i];
				if (p.dimension_type != nullptr)
				{
					delete[](p.dimension_type);
					p.dimension_type = nullptr;
				}
			}
			delete[](d.dimensions);
		}

		template<>
		inline void dispose_of<statistic_definition>(statistic_definition& stat)
		{
			if (stat.statistic_identifier != nullptr) delete[] stat.statistic_identifier;
			if (stat.model_variable_id != nullptr) delete[] stat.model_variable_id;
			if (stat.objective_identifier != nullptr) delete[] stat.objective_identifier;
			if (stat.objective_name != nullptr) delete[] stat.objective_name;
			if (stat.observations != nullptr)
			{
				dispose_of<multi_regular_time_series_data>(*stat.observations);
				delete stat.observations;
			}
		}

		template<>
		inline void dispose_of<multi_statistic_definition>(multi_statistic_definition& stat)
		{
			if (stat.statistics != nullptr)
			{
				for (int i = 0; i < stat.size; i++)
					dispose_of<statistic_definition>(*(stat.statistics[i]));
				delete[] stat.statistics;
			}
			if (stat.mix_statistics_id != nullptr) delete[] stat.mix_statistics_id;
		}
	}
}