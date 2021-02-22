// test_native_library.cpp : Defines the exported functions for the DLL application.
//

#include "test_native_library.h"

#include "../../../../../include/cinterop/c_cpp_interop.hpp"

/***********************
* START OF THE API
************************/

void set_date(DTS_PTR start, int year, int month, int day, int hour, int min, int sec)
{
    start->year = year;
    start->month = month;
    start->day = day;
    start->hour = hour;
    start->minute = min;
    start->second = sec;
}

int get_year(DTS_OBJ start)
{
    return start.year;
}

DTS_PTR create_date(int year, int month, int day, int hour, int min, int sec)
{
    DTS_PTR result = new date_time_to_second();
    set_date(result, year, month, day, hour, min, sec);
    return result;
}

void dispose_date(DTS_PTR start)
{
    delete start;
}

void set_nvv(NVV_PTR nvv)
{
    // TODO?
}

NVV_PTR create_nvv()
{
    std::vector<string> n = {"a","b"};
    std::vector<double> v = {1.0, 2.0};
    return cinterop::utils::create_named_values_vector_ptr(n, v);
}

void dispose_nvv(NVV_PTR nvv)
{
    cinterop::disposal::dispose_of(*nvv);
}

int test_date(DTS_PTR start, int year, int month, int day, int hour, int min, int sec)
{
    if (start->year != year)
        return 0;
    if (start->month != month)
        return 0;
    if (start->day != day)
        return 0;
    if (start->hour != hour)
        return 0;
    if (start->minute != min)
        return 0;
    if (start->second != sec)
        return 0;

    return 1;
}
