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

typedef struct _time_series_dimension_description
{
	char* dimension_type;
	size_t size;
} time_series_dimension_description;

typedef struct _time_series_dimensions_description
{
	time_series_dimension_description* dimensions;
	int num_dimensions;
} time_series_dimensions_description;


