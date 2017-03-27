#pragma once

#ifndef STRDUP
#ifdef _WIN32
#define STRDUP _strdup
#else
#define STRDUP strdup
#endif
#endif // !STRDUP

typedef struct _date_time_to_second
{
	int year;
	int month;
	int day;
	int hour;
	int minute;
	int second;
} date_time_to_second;

