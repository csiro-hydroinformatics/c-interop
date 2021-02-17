#pragma once

/**
 * @file timeseries_c_interop.h
 * @author your name (you@domain.com)
 * @brief C99 structures for time series concepts, defined for interoperability through a C API
 * @date 2020-06-14
 * 
 * @copyright Copyright (c) 2020
 * 
 */


/* C-API interoperable representation of time series */

#include "cinterop/common_c_interop.h"

/** \brief	C-struct interop information describing the geometry of a time steps. Used to cater for strictly regular versus period varying ones (e.g. monthly)*/
typedef enum _time_step_code
{
	strictly_regular = 0,    //!< time steps can be expressed strictly with the same length e.g. 3600 seconds
	monthly_step = 1 //!< monthly time stepping
} time_step_code;

/** \brief	C-struct interop information describing the geometry of a time series with regular (fixed temporal period) time steps */
typedef struct _regular_time_series_geometry
{
	date_time_to_second start; //!< First index of the time series.
	int time_step_seconds; //!< Length of the time step for the time series e.g. 3600 for hourly time series
	int length; //!< Size of the time series
	::time_step_code time_step_code; //!< Optional code of the time series for non-strictly fixed temporal periods, e.g. "monthly", possibly overriding the time_step_seconds property
} regular_time_series_geometry;

/** \brief	C-struct interop information defining a multivariate time series with regular (fixed temporal period) time steps */
typedef struct _multi_regular_time_series_data
{
	regular_time_series_geometry time_series_geometry; //!< Temporal definition (geometry) of this multivariate time series
	int ensemble_size; //!< Number of variables in this multivariate time series
	double** numeric_data; //!< Data of the multivariate time series.
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
	char* model_variable_id; //!< A unique identifier defining which model state variable is used for the statistic
	char* objective_identifier; //!< A unique identifier defining the objective, e.g. "NSE_flow_node_2"
	char* objective_name; //!< A human readable name of the statistic
	char* statistic_identifier; //!< A unique identifier defining which statistic (typically a bivariate statistic)
	date_time_to_second start; //!< Start of the time interval to use in the time series based statistic
	date_time_to_second end; //!< End of the time interval to use in the time series based statistic
	multi_regular_time_series_data* observations; //!< Observation(s) used in this bivariate statistic
} statistic_definition;

/** \brief	C-struct interop information defining a bivariate statistic used in objetive definition for optimisation/calibration */
typedef struct _multi_statistic_definition
{
	int size;  //!< number of statistics in this definition, i.e. length of the #statistics member
	statistic_definition** statistics; //!< array of statistic definitions
	char* mix_statistics_id; //!< Name of this list of statistics. This may be used to refer to this contructs e.g. in log information
} multi_statistic_definition;


