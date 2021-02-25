// test_native_library.cpp : Defines the exported functions for the DLL application.
//

#include "test_native_library.h"

#include <string>
#include <vector>
#include <map>

#include "../../../../../include/cinterop/c_cpp_interop.hpp"
#include "../../../../../include/cinterop/timeseries_interop.hpp"

/***********************
* START OF THE API
************************/

void delete_char_array(char* ptr)
{
    delete ptr;
}

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
    cinterop::disposal::dispose_of(nvv);
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

double first_in_nvv(NVV_OBJ nvv)
{
    return nvv.values[0];
}


void set_vv(VV_PTR vv){
    if (vv->size > 0)
        vv->values[0] = 1.2345;
}

VV_PTR create_vv(){
    std::vector<double> v = {1.0, 2.0, 3.0, 4.0, 5.0};
    return cinterop::utils::create_values_vector_ptr(v);
}
void dispose_vv(VV_PTR vv){
    cinterop::disposal::dispose_of(vv);
}

double first_in_vv(VV_OBJ vv){
    if (vv.size > 0)
        return vv.values[0];
    return -9999.0;
}

void set_cvec(CV_PTR cvec)
{
    int blah = cvec->size;
}

CV_PTR create_cvec(){
    std::vector<std::string> s = {"a", "b"};
    return cinterop::utils::to_character_vector_ptr(s);
}
void dispose_cvec(CV_PTR cvec)
{
    cinterop::disposal::dispose_of(cvec);
}

char* first_in_cvec(CV_OBJ cvec)
{
    return STRDUP(cvec.values[0]);
}

void set_ssm(SSM_PTR ssm)
{
    // nothing?
}

SSM_PTR create_ssm()
{
    std::map<std::string,std::string> m;
    m[std::string("a")] = std::string("A");
    m[std::string("b")] = std::string("B");
    return cinterop::utils::to_string_string_map_ptr(m);
}

void dispose_ssm(SSM_PTR ssm)
{
    cinterop::disposal::dispose_of(ssm);
}

char* value_for_key_ssm(const char* key, SSM_OBJ ssm)
{
    auto v = cinterop::utils::from_string_string_map<std::map<std::string,std::string>>(ssm)[key];
    return STRDUP(v.c_str());
}

// int get_tsc_value(SSM_PTR tsc) {
// }
// SSM_PTR create_tsc() {
//     return new time_step_code(time_step_code::strictly_regular);
// }
// void dispose_tsc(SSM_PTR tsc) {

// }

void set_tsg(TSG_PTR tsg){
    tsg->length = 8;
}

#define TEST_TS_LENGTH 7
void _set_test_tsg(TSG_PTR ptr)
{
    date_time_to_second dts;
    set_date(&dts, 2001,1,2,3,4,5);
    ptr->start = dts;
    ptr->length = TEST_TS_LENGTH;
    ptr->time_step_code = time_step_code::strictly_regular;
    ptr->time_step_seconds = 86400;
}

TSG_PTR create_tsg(){
    auto ptr = new regular_time_series_geometry();
    _set_test_tsg(ptr);
    return ptr;
}
void dispose_tsg(TSG_PTR tsg){
    delete tsg;
}
int tscode_tsg(TSG_OBJ tsg){
    return (int)tsg.time_step_code;
}

MTS_PTR create_mtsd(){
    auto ts = new multi_regular_time_series_data();
    _set_test_tsg(&ts->time_series_geometry);
    ts->ensemble_size = 2;
    ts->numeric_data = new double*[2];
    ts->numeric_data[0] = new double[TEST_TS_LENGTH];
    ts->numeric_data[1] = new double[TEST_TS_LENGTH];
    for (size_t i = 0; i < TEST_TS_LENGTH; i++)
    {
        ts->numeric_data[0][i] = (double)i;
        ts->numeric_data[1][i] = (double)i + 0.1;
    }
    return ts;
}
void dispose_mtsd(MTS_PTR mtsd){
    cinterop::disposal::dispose_of(mtsd);
}



