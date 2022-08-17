import os
from pathlib import Path
import sys
from datetime import datetime

from cinterop.cffi.marshal import *

from cinterop.timeseries import as_datetime64, end_ts, mk_daily_xarray_series, mk_hourly_xarray_series, mk_xarray_series, start_ts, xr_ts_end, xr_ts_start

import pytest
pkg_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, pkg_dir)

from refcount.interop import *
from refcount.putils import library_short_filename

fname = library_short_filename("test_native_library")

if sys.platform == "win32":
    dir_path = os.path.join(pkg_dir, "tests/test_native_library/x64/Debug")
else:
    dir_path = os.path.join(pkg_dir, "tests/test_native_library/build")
    cdefs_dir = os.path.join(pkg_dir, "tests/test_native_library")

native_lib_path = os.path.join(dir_path, fname)

assert os.path.exists(native_lib_path)


# test_native_obj_ref_counting()
# test_cffi_native_handle_finalizers()
# test_cffi_native_handle_dispose()

ut_ffi = FFI()

with open(os.path.join(cdefs_dir, "structs_cdef.h")) as f_headers:
    ut_ffi.cdef(f_headers.read())

with open(os.path.join(cdefs_dir, "funcs_cdef.h")) as f_headers:
    ut_ffi.cdef(f_headers.read())

ut_dll = ut_ffi.dlopen(native_lib_path, 1)  # Lazy loading

marshal = CffiMarshal(ut_ffi)

def test_array_creations():
    x_ptr = new_ctype_array(ut_ffi, "int", 5)
    assert isinstance(x_ptr, FFI.CData)
    x_ptr[0] = 1
    x_ptr[4] = 2
    assert ut_dll.get_array_int(x_ptr, 0) == 1
    assert ut_dll.get_array_int(x_ptr, 4) == 2
    x_ptr = new_ctype_array(ut_ffi, "int", 5, True)
    assert isinstance(x_ptr, OwningCffiNativeHandle)

    x_ptr = new_int_array(ut_ffi, 5)
    assert isinstance(x_ptr, FFI.CData)
    x_ptr[0] = 1
    x_ptr[4] = 2
    assert ut_dll.get_array_int(x_ptr, 0) == 1
    assert ut_dll.get_array_int(x_ptr, 4) == 2

    x_ptr = new_double_array(ut_ffi, 5)
    assert isinstance(x_ptr, FFI.CData)
    x_ptr[0] = 1.0
    x_ptr[4] = 2.0
    assert ut_dll.get_array_double(x_ptr, 0) == 1.0
    assert ut_dll.get_array_double(x_ptr, 4) == 2.0


def test_charptr():
    x_ptr = marshal.as_charptr("abcdef")
    assert isinstance(x_ptr, FFI.CData)
    assert x_ptr[0] == b'a'
    assert x_ptr[1] == b'b'
    assert x_ptr[5] == b'f'
    x_ptr = marshal.as_charptr("abcdef", True)
    assert isinstance(x_ptr, OwningCffiNativeHandle)

def test_as_c_double_array():
    def _p(x_np, wanted_shallow, expected_shallow, test_indx=3):
        x_native = marshal.as_c_double_array(x_np, shallow=wanted_shallow)
        ptr = x_native.ptr
        if isinstance(x_np, xr.DataArray):
            y_np = x_np.values
        else:
            y_np = x_np
        for i in range(len(y_np)):
            assert ptr[i] == float(y_np[i])
        init_val = y_np[test_indx]
        ptr[test_indx] = 3.1415
        if expected_shallow:
            assert y_np[test_indx] == 3.1415
        else:
            assert x_np[test_indx] == init_val
    x_np = np.arange(9, dtype=int)
    _p(x_np, wanted_shallow=False, expected_shallow=False, test_indx=3)
    _p(x_np, wanted_shallow=True, expected_shallow=False, test_indx=3)
    x_np = [i for i in range(6)]
    _p(x_np, wanted_shallow=False, expected_shallow=False, test_indx=3)
    _p(x_np, wanted_shallow=True, expected_shallow=False, test_indx=3)
    x_np = np.arange(9, dtype=float)
    _p(x_np, wanted_shallow=False, expected_shallow=False, test_indx=3)
    _p(x_np, wanted_shallow=True, expected_shallow=True, test_indx=3)

    x_np = np.arange(18, dtype=float).reshape((9, 2))
    with pytest.raises(TypeError):
        _p(x_np, wanted_shallow=False, expected_shallow=False, test_indx=3)

    x_np = np.arange(9, dtype=float).reshape((9, 1))
    _p(x_np, wanted_shallow=False, expected_shallow=False, test_indx=3)
    _p(x_np, wanted_shallow=True, expected_shallow=False, test_indx=3)

    fort_np = np.asfortranarray(x_np)
    _p(fort_np, wanted_shallow=False, expected_shallow=False, test_indx=3)
    _p(fort_np, wanted_shallow=True, expected_shallow=False, test_indx=3)

    from cinterop.timeseries import mk_daily_xarray_series
    x_np = np.arange(9, dtype=int)
    xr_ts = mk_daily_xarray_series(x_np, "2020-01-01")
    _p(xr_ts, wanted_shallow=False, expected_shallow=False, test_indx=3)
    # dtype is int, so shallowness is not supported
    _p(xr_ts, wanted_shallow=True, expected_shallow=False, test_indx=3)

    x_np = np.arange(9, dtype=float)
    xr_ts = mk_daily_xarray_series(x_np, "2020-01-01")
    _p(xr_ts, wanted_shallow=False, expected_shallow=False, test_indx=3)
    # dtype is int, so shallowness is supported
    _p(xr_ts, wanted_shallow=True, expected_shallow=True, test_indx=3)

def test_as_np_array_double():
    ptr_c = marshal.new_double_array(9, wrap=False)
    for i in range(9):
        ptr_c[i] = float(i)
    x_np = marshal.as_np_array_double(ptr_c, 9, False)
    for i in range(9):
        assert x_np[i] == float(i)
    ptr_c[0] = 3.1415
    assert x_np[0] == 0.0
    ptr_c = marshal.new_double_array(9, wrap=False)
    for i in range(9):
        ptr_c[i] = float(i)
    x_np = marshal.as_np_array_double(ptr_c, 9, True)
    for i in range(9):
        assert x_np[i] == float(i)
    ptr_c[0] = 3.1415
    assert x_np[0] == 3.1415

def test_as_numeric_np_array():
    ptr_c = marshal.new_double_array(9, wrap=False)
    ptr = marshal._ffi.cast('double *', ptr_c)
    for i in range(9): ptr[i] = float(i)
    x_np = marshal.as_numeric_np_array(ptr, 6)
    assert x_np.shape == (6,)
    x_np[1] = 3.14
    assert ptr[1] == 1.0
    x_np = marshal.as_numeric_np_array(ptr, 6, shallow=True)
    assert x_np.shape == (6,)
    x_np[1] = 3.14
    assert ptr[1] == 3.14

    ptr_c = marshal.new_int_array(9, wrap=False)
    with pytest.raises(TypeError):
        _ = marshal.as_numeric_np_array(ptr_c, 9, shallow=True)

def test_two_d_as_np_array_double():
    ptr = marshal.nullptr
    x = marshal.two_d_as_np_array_double(ptr, 2, 0)
    assert x.shape == (2,0)
    x = marshal.two_d_as_np_array_double(ptr, 0, 2)
    assert x.shape == (0,2)

    ptr = ut_dll.create_doublepp(3, 4)
    assert ptr[0][0] == 0.0
    assert ptr[0][1] == 1.0
    assert ptr[0][2] == 2.0
    assert ptr[2][3] == 11.0

    x_np = marshal.two_d_as_np_array_double(ptr, 2, 4)
    assert x_np.shape == (2, 4)
    assert x_np[0,0] == 0.0
    assert x_np[0,1] == 1.0
    assert x_np[0,2] == 2.0
    assert x_np[1,3] == 7.0

    x_np = marshal.two_d_as_np_array_double(ptr, 2, 4)
    assert x_np.shape == (2, 4)
    assert x_np[0,0] == 0.0
    assert x_np[0,1] == 1.0
    assert x_np[0,2] == 2.0
    assert x_np[1,3] == 7.0

    # check that we have a deep copy, no shallow copy

    x_np = marshal.two_d_as_np_array_double(ptr, 3, 4)
    assert x_np.shape == (3, 4)
    assert x_np[0,0] == 0.0
    assert x_np[0,1] == 1.0
    assert x_np[0,2] == 2.0
    assert x_np[2,3] == 11.0

    ptr[0][0] = 3.1415
    assert x_np[0,0] == 0.0
    ptr[0][1] = 1.234
    assert x_np[0,1] == 1.0


    ut_dll.delete_doublepp(ptr, 3)


def test_two_d_np_array_double_to_native():
    x_np = np.arange(18, dtype=float).reshape((9, 2))
    wrapper = marshal.two_d_np_array_double_to_native(x_np)
    ptr = wrapper.ptr
    for i in range(9):
        for j in range(2):
            assert ptr[i][j] == x_np[i][j]

    with pytest.raises(TypeError):
        d = datetime(2000,1,1)
        _ = marshal.two_d_np_array_double_to_native(d)

    x_np = np.arange(18, dtype=float).reshape((3, 3, 2))
    with pytest.raises(TypeError):
        _ = marshal.two_d_np_array_double_to_native(x_np)


def test_get_tsgeom():
    d = datetime(2000,1,1)
    data = np.arange(31, dtype=float)
    s = mk_daily_xarray_series(data, d)
    ss = [s, s.to_series(), s.to_dataframe(name="something")]
    for s in ss:
        geom = get_tsgeom(s)
        assert geom.length == 31
        assert as_datetime64(geom.start) == as_datetime64(d) 
        assert geom.time_step_code == 0
        assert geom.time_step_seconds == 86400

    for s in ss:
        assert start_ts(s) == as_datetime64(d)
        assert end_ts(s) == as_datetime64(datetime(2000,1,31))
        assert xr_ts_start(s) == as_datetime64(d)
        assert xr_ts_end(s) == as_datetime64(datetime(2000,1,31))

    data = np.arange(48, dtype=float)
    s = mk_hourly_xarray_series(data, d)
    geom = get_tsgeom(s)
    assert geom.length == 48
    assert as_datetime64(geom.start) == as_datetime64(d) 
    assert geom.time_step_code == 0
    assert geom.time_step_seconds == 3600

    data = np.arange(12, dtype=float)
    indx = create_monthly_time_index(d, 12)
    s = mk_xarray_series(data, time_index=indx)
    geom = get_tsgeom(s)
    assert geom.length == 12
    assert as_datetime64(geom.start) == as_datetime64(d) 
    assert geom.time_step_code == 1
    assert geom.time_step_seconds == -1

def test_charpp_returned():
    size = marshal.new_int_scalar_ptr()
    ptr = ut_dll.create_charpp(size)
    ssm = marshal.c_charptrptr_as_string_list(ptr, size[0])
    assert len(ssm) == 3
    assert ssm[0] == "a"
    ut_dll.delete_charptr_array(ptr, size[0])


# /home/per202/src/github_jm/c-interop/include/cinterop/common_c_interop.h
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
    assert nvv["a"] == 1.0
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
    ssm = {"c": "C", "d": "D"}
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

def _create_test_series_xr() -> xr.DataArray:
    a = np.array([[1, 2, 3.0], [4, 5, 6.0]])
    e = [1, 2]
    t = as_timestamp("2020-01-01")
    time_index = create_even_time_index(t, 86400, 3)
    data = create_ensemble_series(a, e, time_index)
    return data


def _create_test_series_pd_series() -> pd.Series:
    a = np.array([1, 2, 3.0])
    t = as_timestamp("2020-01-01")
    time_index = create_even_time_index(t, 86400, 3)
    return pd.Series(a, index=time_index)


def _create_test_series_pd_df() -> pd.DataFrame:
    a = np.array([[1, 2, 3.0], [4, 5, 6.0]]).transpose()
    t = as_timestamp("2020-01-01")
    time_index = create_even_time_index(t, 86400, 3)
    return pd.DataFrame(a, index=time_index)


#   26,1: typedef struct _regular_time_series_geometry
def test_time_series_geometry():

    xr_series = _create_test_series_xr()
    g = get_tsgeom(xr_series)
    assert g.length == 3
    assert g.start == as_timestamp("2020-01-01")
    assert g.time_step_seconds == 86400

    pd_series = _create_test_series_pd_series()
    g = get_tsgeom(pd_series)
    assert g.length == 3
    assert g.start == as_timestamp("2020-01-01")
    assert g.time_step_seconds == 86400

    pd_df = _create_test_series_pd_df()
    g = get_tsgeom(pd_df)
    assert g.length == 3
    assert g.start == as_timestamp("2020-01-01")
    assert g.time_step_seconds == 86400

    ptr = ut_dll.create_tsg()
    assert ptr.time_step_code == 0
    ut_dll.dispose_tsg(ptr)
    tsg = TimeSeriesGeometry(datetime(2010, 5, 4, 3, 2, 1), 3600, 24, 0)
    tsg_ptr = marshal.as_native_tsgeom(tsg)
    assert ut_dll.tscode_tsg(tsg_ptr.obj) == 0


def test_geom_to_xarray_time_series():
    tsgeom = marshal.new_native_tsgeom()
    tsgeom.length = 9
    sd = as_datetime64(datetime(2000,1,1))
    tsgeom.start = sd
    tsgeom.time_step_code = 0
    tsgeom.time_step_seconds = 3600
    d = geom_to_xarray_time_series(ts_geom=tsgeom, data=np.arange(9, dtype=float), name="test_name")
    assert d.name == "test_name"
    assert d.shape == (1,9)
    assert start_ts(d) == sd
    assert end_ts(d) == as_datetime64("2000-01-01T08")

def test_new_date_time_to_second():
    w_ptr = marshal.new_date_time_to_second()
    assert str(w_ptr).startswith("CFFI pointer handle to a native pointer")
    assert str(w_ptr).find("date_time_to_second") > -1

def test_as_bytes():
    xs = "abcdef"
    xb = b"abcdef"
    assert as_bytes(xb) == xb
    assert as_bytes(xs) == xb
    s = Path("blah")
    assert isinstance(as_bytes(s), Path)

def test_as_string():
    xs = "abcdef"
    xb = b"abcdef"
    assert as_string(xb) == xs
    assert as_string(xs) == xs
    s = Path("blah")
    assert isinstance(as_string(s), Path)

#   35,1: typedef struct _multi_regular_time_series_data
def test_multi_regular_time_series_data():
    data = _create_test_series_xr()
    x = as_native_time_series(ut_ffi, data)
    assert x.ptr.numeric_data[0][0] == 1.0
    assert x.ptr.numeric_data[0][2] == 3.0
    assert x.ptr.numeric_data[1][0] == 4.0
    assert x.ptr.numeric_data[1][2] == 6.0
    assert x.ptr.ensemble_size == 2

    data = _create_test_series_pd_series()
    x = as_native_time_series(ut_ffi, data)
    assert x.ptr.numeric_data[0][0] == 1.0
    assert x.ptr.numeric_data[0][1] == 2.0
    assert x.ptr.numeric_data[0][2] == 3.0
    assert x.ptr.ensemble_size == 1

    data = _create_test_series_pd_df()
    x = as_native_time_series(ut_ffi, data)
    assert x.ptr.ensemble_size == 2
    assert x.ptr.numeric_data[0][0] == 1.0
    assert x.ptr.numeric_data[0][2] == 3.0
    assert x.ptr.numeric_data[1][0] == 4.0
    assert x.ptr.numeric_data[1][2] == 6.0

    ptr = ut_dll.create_mtsd()
    tsg = marshal.as_xarray_time_series(ptr)
    blah = tsg.dims
    ut_dll.dispose_mtsd(ptr)


#   43,1: typedef struct _time_series_dimension_description
#   50,1: typedef struct _time_series_dimensions_description
#   57,1: typedef struct _statistic_definition
#   69,1: typedef struct _multi_statistic_definition

if __name__ == "__main__":
    test_as_c_double_array()
