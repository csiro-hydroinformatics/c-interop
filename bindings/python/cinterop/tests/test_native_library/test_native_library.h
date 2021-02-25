/**
 * \file	test_native_library.h
 *
 * \brief	A C API to test and document how one can use dynamic interop from .NET.
 * 			This test library has two concepts, a dog and its owner. Both have a (simplistic) mechanism for 
 * 			reference counting within C API, something you might encounter in real situations, 
 * 			in which case your .NET wrapper may use these instead of doing it at the .NET level.
 */

#pragma once

#include "../../../../../include/cinterop/common_c_interop.h"
#include "../../../../../include/cinterop/timeseries_c_interop.h"

// Using patterns in https://msdn.microsoft.com/en-us/library/as6wyhwt(v=vs.100).aspx to mark
// C interop function as being exported or imported, something necessary with MS cpp tooling.
#ifdef _WIN32
#ifdef USING_TESTLIB_CORE
#define TESTLIB_CORE_DLL_LIB __declspec(dllimport)
#else
#define TESTLIB_CORE_DLL_LIB __declspec(dllexport)
// To prevent warnings such as:
// Warning	C4251	'blah::MyClass' : class 'std::basic_string<char,std::char_traits<char>,std::allocator<char>>' needs to have dll - interface to be used by clients of class 'something'
#pragma warning(disable : 4251)
#endif
#else
#define TESTLIB_CORE_DLL_LIB // nothing
#endif

#define TESTLIB_API TESTLIB_CORE_DLL_LIB

#define DTS_PTR date_time_to_second *
#define DTS_OBJ date_time_to_second

#define NVV_PTR named_values_vector *
#define NVV_OBJ named_values_vector

#define VV_PTR values_vector *
#define VV_OBJ values_vector

#define CV_PTR character_vector *
#define CV_OBJ character_vector

#define SSM_PTR string_string_map *
#define SSM_OBJ string_string_map

#define TTC_PTR time_step_code *
#define TTC_OBJ time_step_code

#define TSG_PTR regular_time_series_geometry *
#define TSG_OBJ regular_time_series_geometry

#define MTS_PTR multi_regular_time_series_data *
#define MTS_OBJ multi_regular_time_series_data



#ifdef __cplusplus
extern "C"
{
#endif

    TESTLIB_API void delete_char_array(char* ptr);

    TESTLIB_API void set_date(DTS_PTR start, int year, int month, int day, int hour, int min, int sec);
    TESTLIB_API DTS_PTR create_date(int year, int month, int day, int hour, int min, int sec);
    TESTLIB_API void dispose_date(DTS_PTR start);
    TESTLIB_API int get_year(DTS_OBJ start);

    TESTLIB_API void set_nvv(NVV_PTR nvv);
    TESTLIB_API NVV_PTR create_nvv();
    TESTLIB_API void dispose_nvv(NVV_PTR nvv);
    TESTLIB_API double first_in_nvv(NVV_OBJ nvv);

//   54,1: typedef struct _values_vector
    TESTLIB_API void set_vv(VV_PTR vv);
    TESTLIB_API VV_PTR create_vv();
    TESTLIB_API void dispose_vv(VV_PTR vv);
    TESTLIB_API double first_in_vv(VV_OBJ vv);


//   66,1: typedef struct _character_vector
    TESTLIB_API void set_cvec(CV_PTR cvec);
    TESTLIB_API CV_PTR create_cvec();
    TESTLIB_API void dispose_cvec(CV_PTR cvec);
    TESTLIB_API char* first_in_cvec(CV_OBJ cvec);

//   78,1: typedef struct _string_string_map
    TESTLIB_API void set_ssm(SSM_PTR ssm);
    TESTLIB_API SSM_PTR create_ssm();
    TESTLIB_API void dispose_ssm(SSM_PTR ssm);
    TESTLIB_API char* value_for_key_ssm(const char* key, SSM_OBJ ssm);

// 

//   19,1: typedef enum _time_step_code
    // TESTLIB_API int get_tsc_value(SSM_PTR tsc);
    // TESTLIB_API SSM_PTR create_tsc();
    // TESTLIB_API void dispose_tsc(SSM_PTR tsc);
    // TESTLIB_API char* value_for_key_tsc(const char* key, SSM_OBJ tsc);

//   26,1: typedef struct _regular_time_series_geometry
    TESTLIB_API void set_tsg(TSG_PTR tsg);
    TESTLIB_API TSG_PTR create_tsg();
    TESTLIB_API void dispose_tsg(TSG_PTR tsg);
    TESTLIB_API int tscode_tsg(TSG_OBJ tsg);

//   35,1: typedef struct _multi_regular_time_series_data
    TESTLIB_API MTS_PTR create_mtsd();
    TESTLIB_API void dispose_mtsd(MTS_PTR mtsd);
//   43,1: typedef struct _time_series_dimension_description
//   50,1: typedef struct _time_series_dimensions_description
//   57,1: typedef struct _statistic_definition
//   69,1: typedef struct _multi_statistic_definition

#ifdef __cplusplus
}
#endif
