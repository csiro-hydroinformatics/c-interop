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
#define NVV_PTR named_values_vector *

#define DTS_OBJ date_time_to_second
#define NVV_OBJ named_values_vector

#ifdef __cplusplus
extern "C"
{
#endif

    TESTLIB_API void set_date(DTS_PTR start, int year, int month, int day, int hour, int min, int sec);
    TESTLIB_API DTS_PTR create_date(int year, int month, int day, int hour, int min, int sec);
    TESTLIB_API void dispose_date(DTS_PTR start);
    TESTLIB_API int get_year(DTS_OBJ start);

    TESTLIB_API void set_nvv(NVV_PTR nvv);
    TESTLIB_API NVV_PTR create_nvv();
    TESTLIB_API void dispose_nvv(NVV_PTR nvv);

#ifdef __cplusplus
}
#endif
