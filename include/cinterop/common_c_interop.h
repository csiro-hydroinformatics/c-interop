#pragma once

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
	size_t size;
	double* values;
	char** names;
} named_values_vector;

typedef struct _character_vector
{
	size_t size;
	char** values;
} character_vector;

typedef struct _string_string_map
{
	size_t size;
	char** keys;
	char** values;
} string_string_map;

