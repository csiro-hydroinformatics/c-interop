import os
import sys
from datetime import datetime
import gc
import cinterop
from cinterop.cffi.marshal import * 

pkg_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, pkg_dir)

from refcount.interop import *
from refcount.putils import library_short_filename

fname = library_short_filename("test_native_library")

if sys.platform == "win32":
    dir_path = os.path.join(pkg_dir, "tests/test_native_library/x64/Debug")
else:
    dir_path = os.path.join(pkg_dir, "tests/test_native_library/build")
    cdefs_dir = os.path.join(pkg_dir, 'tests/test_native_library')

native_lib_path = os.path.join(dir_path, fname)

assert os.path.exists(native_lib_path)


# test_native_obj_ref_counting()
# test_cffi_native_handle_finalizers()
# test_cffi_native_handle_dispose()

ut_ffi = FFI()

with open(os.path.join(cdefs_dir, 'structs_cdef.h')) as f_headers:
    ut_ffi.cdef(f_headers.read())

with open(os.path.join(cdefs_dir, 'funcs_cdef.h')) as f_headers:
    ut_ffi.cdef(f_headers.read())

ut_dll = ut_ffi.dlopen(native_lib_path, 1)  # Lazy loading

marshal = CffiMarshal(ut_ffi)

# /home/per202/src/github_jm/rcpp-interop-commons/include/cinterop/common_c_interop.h
#   25,1: typedef struct _date_time_to_second
def test_date_time_interop():
    ptr = ut_dll.create_date(2019, 12, 1, 2, 3, 4)
    dt = marshal.as_datetime(ptr)
    ut_dll.dispose_date(ptr)
    assert dt.year == 2019
    # Pass in a datetime into a native lib function
    dt = datetime(2001, 1, 2, 3, 4, 5)
    dt_ptr = marshal.datetime_to_dtts(dt)
    assert ut_dll.get_year(dt_ptr.obj) == 2001

#   42,1: typedef struct _named_values_vector
def test_named_values_vector_interop():
    ptr = ut_dll.create_nvv()
    nvv = marshal.named_values_to_dict(ptr)
    ut_dll.dispose_nvv(ptr)
    assert nvv['a'] == 1.0
    nvv = {"c": 3.0, "d": 4.0}
    nvv_ptr = marshal.dict_to_named_values(nvv)
    assert ut_dll.first_in_nvv(nvv_ptr.obj) == 3.0
#   54,1: typedef struct _values_vector
def test_values_vector_interop():
    ptr = ut_dll.create_vv()
    vv = marshal.values_to_nparray(ptr)
    ut_dll.dispose_vv(ptr)
    assert vv[0] == 1.0
    vv = np.array([3.0, 4.0])
    vv_ptr = marshal.create_values_struct(vv)
    assert ut_dll.first_in_vv(vv_ptr.obj) == 3.0
#   66,1: typedef struct _character_vector
def test_character_vector_interop():
    ptr = ut_dll.create_cvec()
    cvec = marshal.character_vector_as_string_list(ptr)
    ut_dll.dispose_cvec(ptr)
    assert cvec[0] == "a"
    cvec = ["c", "d"]
    cvec_ptr = marshal.as_character_vector(cvec)
    x = ut_dll.first_in_cvec(cvec_ptr.obj)
    s = marshal.c_string_as_py_string(x)
    ut_dll.delete_char_array(x)
    assert s == "c"
#   78,1: typedef struct _string_string_map
def test_string_string_map():
    ptr = ut_dll.create_ssm()
    ssm = marshal.string_map_to_dict(ptr)
    ut_dll.dispose_ssm(ptr)
    assert ssm["a"] == "A"
    ssm = {"c":"C", "d":"D"}
    ssm_ptr = marshal.dict_to_string_map(ssm)
    k = marshal.as_charptr("c")
    x = ut_dll.value_for_key_ssm(k, ssm_ptr.obj)
    s = marshal.c_string_as_py_string(x)
    ut_dll.delete_char_array(x)
    assert s == "C"
# 

#   19,1: typedef enum _time_step_code
# def test_time_step_code():
#     ptr = ut_dll.create_tsc()
#     # ssm = marshal.string_map_to_dict(ptr)
#     ut_dll.dispose_tsc(ptr)
#     # assert ssm["a"] == "A"
#     # ssm = {"c":"C", "d":"D"}
#     ssm_ptr = marshal.time_step_code(1)

#   26,1: typedef struct _regular_time_series_geometry
def test_time_series_geometry():
    ptr = ut_dll.create_tsg()
    tsg = marshal.time_series_geometry(ptr)
    ut_dll.dispose_tsg(ptr)
    assert tsg.time_step_code == 0
    tsg = TimeSeriesGeometry(datetime(2010,5,4,3,2,1), 3600, 24, 0)
    tsg_ptr = marshal.as_native_tsgeom(tsg)
    assert ut_dll.tscode_tsg(tsg_ptr.obj) == 0

#   35,1: typedef struct _multi_regular_time_series_data
def test_multi_regular_time_series_data():
    ptr = ut_dll.create_mtsd()
    tsg = marshal.as_xarray_time_series(ptr)
    blah = tsg.dims
    ut_dll.dispose_mtsd(ptr)
#   43,1: typedef struct _time_series_dimension_description
#   50,1: typedef struct _time_series_dimensions_description
#   57,1: typedef struct _statistic_definition
#   69,1: typedef struct _multi_statistic_definition

if __name__ == "__main__":
    test_date_time_interop()
    test_named_values_vector_interop()
    test_values_vector_interop()
    test_character_vector_interop()
    test_string_string_map()
    test_time_series_geometry()
    test_multi_regular_time_series_data()
