#pragma once

/**
 * @file common_c_interop.h
 * @author your name (you@domain.com)
 * @brief Core generic C99 structures defined for interoperability through a C API
 * @date 2020-06-14
 * 
 * @copyright Copyright (c) 2020
 * 
 */

#include <cstddef> // otherwise you may get "error: 'size_t' does not name a type" with gcc (at least compiling R pkgs)
#include <string.h>

#ifndef STRDUP
#ifdef _WIN32
#define STRDUP _strdup
#else
#define STRDUP strdup
#endif
#endif // !STRDUP

/** \brief	C-struct interop information for time stamps to a resolution of one second */
typedef struct _date_time_to_second
{
	int year;
	int month;
	int day;
	int hour;
	int minute;
	int second;
} date_time_to_second;

/**
 * \struct	named_values_vector
 *
 * \brief	a struct for interop, useful to convey equivalents to e.g. 
 * 			std::map<string,double>, or R's named numeric vectors
 */

typedef struct _named_values_vector
{
	size_t size; //!< Size of the vector
	double* values; //!< values of the vector
	char** names; //!< Names of the vector
} named_values_vector;

/**
 * @brief a struct for interop, useful to convey equivalents to e.g. 
 * 			std::vector<double>, or R's numeric vectors
 * 
 */
typedef struct _values_vector
{
	size_t size; //!< Size of the vector
	double* values; //!< values of the vector
} values_vector;

/**
 * \struct	character_vector
 *
 * \brief	a struct for interop, useful to convey equivalents to e.g. 
 * 			std::vector<double>, or R's character vectors
 */
typedef struct _character_vector
{
	size_t size;
	char** values;
} character_vector;

/**
 * \struct	string_string_map
 *
 * \brief	a struct for interop, useful to convey equivalents to e.g. 
 * 			std::map<string,string>, or R's named list or named vector of strings
 */
typedef struct _string_string_map
{
	size_t size;
	char** keys;
	char** values;
} string_string_map;

