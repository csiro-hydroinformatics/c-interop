#pragma once

/* C-API interoperable representation of time series */

#include "cinterop/common_c_interop.h"

/** \brief	C-struct interop information describing the geometry of a time series with regular (fixed temporal period) time steps */
typedef struct _regular_time_series_geometry
{
	date_time_to_second start;
	int time_step_seconds;
	int length;
} regular_time_series_geometry;

/** \brief	C-struct interop information defining a multivariate time series with regular (fixed temporal period) time steps */
typedef struct _multi_regular_time_series_data
{
	regular_time_series_geometry time_series_geometry;
	int ensemble_size;
	double** numeric_data;
} multi_regular_time_series_data;

/** \brief	C-struct interop information defining one of the dimension of a multidimensional time series */
typedef struct _time_series_dimension_description
{
	char* dimension_type;
	size_t size;
} time_series_dimension_description;

/** \brief	C-struct interop information defining the dimensions of a multidimensional time series */
typedef struct _time_series_dimensions_description
{
	time_series_dimension_description* dimensions;
	int num_dimensions;
} time_series_dimensions_description;

/** \brief	C-struct interop information defining a bivariate statistic used in objetive definition for optimisation/calibration */
typedef struct _statistic_definition
{
	char* model_variable_id;
	char* objective_identifier;
	char* objective_name;
	char* statistic_identifier;
	date_time_to_second start;
	date_time_to_second end;
	multi_regular_time_series_data* observations;
} statistic_definition;

typedef struct _multi_statistic_definition
{
	int size;
	statistic_definition** statistics;
	char* mix_statistics_id;
} multi_statistic_definition;


