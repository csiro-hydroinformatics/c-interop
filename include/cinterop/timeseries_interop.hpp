#pragma once

#include "cinterop/timeseries_c_interop.h"
#include "cinterop/object_lifetimes.hpp"

namespace cinterop
{
	namespace timeseries
	{

		template<typename From>
		void to_regular_time_series_geometry(const From& rTsInfo, regular_time_series_geometry& mts);

		template<typename To>
		To from_regular_time_series_geometry(const regular_time_series_geometry& mts);

		template<typename From>
		regular_time_series_geometry to_regular_time_series_geometry(const From& rTsInfo)
		{
			regular_time_series_geometry mts;
			to_regular_time_series_geometry(rTsInfo, mts);
			return mts;
		}

		template<typename From>
		regular_time_series_geometry* to_regular_time_series_geometry_ptr(const From& rTsInfo)
		{
			regular_time_series_geometry* mts = new regular_time_series_geometry();
			to_regular_time_series_geometry(rTsInfo, *mts);
			return mts;
		}

		template<typename From>
		multi_regular_time_series_data to_multi_regular_time_series_data(const From& timeSeriesEnsemble);

		template<typename From>
		multi_regular_time_series_data* to_multi_regular_time_series_data_ptr(const From& timeSeriesEnsemble);

		template<typename To>
		To from_multi_regular_time_series_data(const multi_regular_time_series_data& mts);

	}
	namespace statistics
	{
		template<typename From>
		void to_multi_statistic_definition(const From& rTsInfo, multi_statistic_definition& mts);
			
		template<typename From>
		multi_statistic_definition* to_multi_statistic_definition_ptr(const From& definition)
		{
			multi_statistic_definition* mts = new multi_statistic_definition();
			to_multi_statistic_definition(rTsInfo, *mts);
			return mts;
		}

		template<typename From>
		statistic_definition* to_statistic_definition_ptr(const string& model_variable_id, const string& statistic_identifier, const string& objective_identifier, const string& objective_name,
			const date_time_to_second& start, const date_time_to_second& end, const From& time_series_data)
		{
			using namespace cinterop::timeseries;
			statistic_definition* stat = new statistic_definition();
			stat->statistic_identifier = STRDUP(statistic_identifier.c_str());
			stat->start = start;
			stat->end = end;
			stat->model_variable_id = STRDUP(model_variable_id.c_str());
			stat->objective_identifier = STRDUP(objective_identifier.c_str());
			stat->objective_name = STRDUP(objective_name.c_str());
			stat->observations = to_multi_regular_time_series_data_ptr<From>(time_series_data);
			return stat;
		}
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