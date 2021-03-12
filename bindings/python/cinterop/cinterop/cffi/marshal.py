
import numpy as np
from functools import wraps

from typing import Any, Dict, Iterable, List, Union
from cffi import FFI
import six
from refcount.interop import OwningCffiNativeHandle
from datetime import datetime
import xarray as xr
import pandas as pd

# This is a Hack. I cannot use FFI.CData in type hints.
CffiData = Any
"""dummy type hint for FFI.CData"""

ConvertibleToTimestamp = Union[str, datetime, np.datetime64, pd.Timestamp]
"""Definition of a 'type' for type hints. 
"""

TimeSeriesLike = Union[pd.Series, pd.DataFrame, xr.DataArray]

_c2dtype = dict()
_c2dtype[ 'float *' ] = np.dtype( 'f4' )
_c2dtype[ 'double *' ] = np.dtype( 'f8' )
# _c2dtype[ 'int *' ] = np.dtype( 'i4' ) TBD

def new_int_array(ffi, size) -> CffiData:
    return ffi.new('int[%d]' % (size,))

def new_int_scalar_ptr(ffi, value:int=0) -> CffiData:
    ptr = ffi.new('int*')
    ptr[0] = value
    return ptr

def new_double_array(ffi, size) -> CffiData:
    return ffi.new('double[%d]' % (size,))

def new_doubleptr_array(ffi, size) -> CffiData:
    return ffi.new('double*[%d]' % (size,))

def new_charptr_array(ffi, size) -> CffiData:
    return ffi.new('char*[%d]' % (size,))

def as_charptr(ffi, x:str) -> CffiData:
    return ffi.new("char[]", as_bytes(x))

def as_numeric_np_array(ffi:FFI, ptr:CffiData, size:int, shallow:bool=False) -> np.ndarray:
    """Convert if possible a cffi pointer to a C data array, into a numpy array.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData)
        size (int): array size
        shallow (bool): If true the array points directly to native data array. Defaults to False.

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        np.ndarray: converted data
    """    
    t = ffi.typeof(ptr).cname # e.g. 'double *'
    if t not in _c2dtype:
        raise RuntimeError( "Cannot create an array for element type: %s" % t )
    dtype = _c2dtype[t]
    buffer_size = size*dtype.itemsize
    res = np.frombuffer( ffi.buffer( ptr, buffer_size ), dtype )
    if shallow:
        return res
    else:
        return res.copy()

def as_np_array_double(ffi:FFI, ptr:CffiData, size:int, shallow:bool=False) -> np.ndarray:
    """Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData)
        size (int): array size
        shallow (bool): If true the array points directly to native data array. Defaults to False.

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        np.ndarray: converted data
    """    
    res = np.frombuffer(ffi.buffer(
        ffi.cast('double[%d]' % (size,),
                    ptr))
    )
    if shallow:
        return res
    else:
        return res.copy()

def named_values_to_dict(ffi:FFI, ptr:CffiData) -> Dict[str,float]:
    """Convert if possible a cffi pointer to a named_values_vector struct, into a dictionary

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData) to a named_values_vector struct

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        Dict[str,float]: converted data
    """
    size = int(ptr.size)
    values = as_np_array_double(ffi, ptr.values, size, shallow=False)
    names = c_charptrptr_as_string_list(ffi, ptr.names, size)
    # checks on names being unique
    if len(set(names)) < len(names):
        raise KeyError("Names of the values are not unique; cannot use as keys to make a dictionary")
    return dict ([(names[i],values[i]) for i in range(len(names))])


def dict_to_named_values(ffi:FFI, data:Dict[str,float]) -> OwningCffiNativeHandle:
    ptr = ffi.new("named_values_vector*")
    ptr.size = len(data)
    ptr.values = as_c_double_array(ffi, list(data.values())).ptr
    names = as_arrayof_bytes(ffi, list(data.keys()))
    ptr.names = names.ptr
    result = OwningCffiNativeHandle(ptr)
    result.keepalive = names
    return result

def string_map_to_dict(ffi:FFI, ptr:CffiData) -> Dict[str,str]:
    """Convert if possible a cffi pointer to a string_string_map struct, into a dictionary

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData) to a string_string_map struct

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        Dict[str,str]: converted data
    """
    size = int(ptr.size)
    keys = c_charptrptr_as_string_list(ffi, ptr.keys, size)
    values = c_charptrptr_as_string_list(ffi, ptr.values, size)
    # checks on names being unique
    if len(set(keys)) < len(keys):
        raise KeyError("Names of the values are not unique; cannot use as keys to make a dictionary")
    return dict ([(keys[i],values[i]) for i in range(len(keys))])

def dict_to_string_map(ffi:FFI, data:Dict[str,str]) -> OwningCffiNativeHandle:
    ptr = ffi.new("string_string_map*")
    ptr.size = len(data)
    keys = as_arrayof_bytes(ffi, list(data.keys()))
    ptr.keys = keys.ptr
    values = as_arrayof_bytes(ffi, list(data.values()))
    ptr.values = values.ptr
    result = OwningCffiNativeHandle(ptr)
    result.keepalive = [keys, values]
    return result

class TimeSeriesGeometry:
    def __init__(self, start:ConvertibleToTimestamp=None, time_step_seconds:int=0, length:int=1, time_step_code:int=0):
        self.start = start if start is not None else as_pydatetime("1970-01-01")
        self.time_step_seconds = time_step_seconds
        self.length = length
        self.time_step_code = time_step_code

    def as_native(self, ffi:FFI):
        return TimeSeriesGeometryNative(ffi, self.start, self.time_step_seconds, self.length, self.time_step_code)

class TimeSeriesGeometryNative(OwningCffiNativeHandle):
    def __init__(self, ffi:FFI, start:ConvertibleToTimestamp=None, time_step_seconds:int=0, length:int=1, time_step_code:int=0):
        if isinstance(ffi, FFI.CData): # HACK? rethink
            super(TimeSeriesGeometryNative, self).__init__(
                ffi, "regular_time_series_geometry*", 0 
            )
        else:
            ptr = ffi.new("regular_time_series_geometry*")
            super(TimeSeriesGeometryNative, self).__init__(
                ptr, "regular_time_series_geometry*", 0 
            )
            self.start = start if start is not None else as_pydatetime("1970-01-01")
            self.time_step_seconds = time_step_seconds
            self.length = length
            self.time_step_code = time_step_code

    @property
    def start(self) -> datetime:
        return dtts_as_datetime(self._handle.start)

    @start.setter
    def start(self, value):
        dt = as_pydatetime(value)
        _copy_datetime_to_dtts(dt, self._handle.start)

    @property
    def time_step_seconds(self) -> int:
        return self._handle.time_step_seconds

    @time_step_seconds.setter
    def time_step_seconds(self, value:int):
        self._handle.time_step_seconds = value

    @property
    def length(self) -> int:
        return self._handle.length

    @length.setter
    def length(self, value:int):
        self._handle.length = value

    @property
    def time_step_code(self) -> int:
        return self._handle.time_step_code

    @time_step_code.setter
    def time_step_code(self, value:int):
        self._handle.time_step_code = value

# def time_series_geometry(ffi:FFI, ptr:CffiData) -> TimeSeriesGeometry:
#     return TimeSeriesGeometry(
#         dtts_as_datetime(ffi, ptr.start),
#         ptr.time_step_seconds, 
#         ptr.length, 
#         ptr.time_step_code)

def as_native_tsgeom(ffi:FFI, tsgeom:TimeSeriesGeometry) -> TimeSeriesGeometryNative:
    return tsgeom.as_native(ffi)

def get_tsgeom(data:TimeSeriesLike) -> TimeSeriesGeometry:
    if isinstance(data, xr.DataArray):
        indx = data.coords[TIME_DIMNAME].values
    elif isinstance(data, pd.Series):
        indx = data.index
    elif isinstance(data, pd.DataFrame):
        indx = data.index
    else:
        raise TypeError(
            "Not recognised as a type of time series: " + str(type(data)))
    a = as_timestamp(indx[0])
    b = as_timestamp(indx[1])
    firstDelta = b-a
    tStepCode = 0
    tStep = int(firstDelta.total_seconds())
    if tStep > 86400 * 27: # HACK: assume monthly
        tStepCode = 1
        tStep = -1
    return TimeSeriesGeometry(a, tStep, len(indx), tStepCode)

def get_native_tsgeom(ffi:FFI, pd_series:pd.Series) -> OwningCffiNativeHandle:
    # stopifnot(xts::is.xts(pd_series))
    return as_native_tsgeom(ffi, get_tsgeom(pd_series))


def _is_convertible_to_timestamp(t: Any):
    return isinstance(t, str) or isinstance(t, datetime) or isinstance(t, np.datetime64) or isinstance(t, pd.Timestamp)


def as_timestamp(t: ConvertibleToTimestamp) -> pd.Timestamp:
    # work around a breaking change in pandas 1.x: "Expected unicode, got numpy.str_'
    if isinstance(t, np.str):
        t = str(t)
    if _is_convertible_to_timestamp(t):
        return pd.Timestamp(t)
    else:
        raise TypeError(
            "Cannot convert to a timestamp the object of type" + str(type(t)))


def as_pydatetime(t: ConvertibleToTimestamp) -> datetime:
    return as_timestamp(t).to_pydatetime()

## TODO: Generic, non interop time series functions should go "elsewhere"

TIME_DIMNAME="time"
ENSEMBLE_DIMNAME="ensemble"

def xr_ts_start(x:xr.DataArray):
    return x.coords[TIME_DIMNAME].values[0]

def xr_ts_end(x:xr.DataArray):
    return x.coords[TIME_DIMNAME].values[-1]

def _time_interval_indx(dt:np.ndarray, from_date: pd.Timestamp = None, to_date: pd.Timestamp = None) -> np.ndarray:
    tt = np.empty_like(dt, np.bool)
    tt[:] = True
    if from_date is not None:
        tt = np.logical_and(tt, (dt >= np.datetime64(from_date)))
    if to_date is not None:
        tt = np.logical_and(tt, (dt <= np.datetime64(to_date)))
    return tt

def slice_xr_time_series(data: xr.DataArray, from_date: pd.Timestamp = None, to_date: pd.Timestamp = None) -> xr.DataArray:
    """Subset a time series to a period

    Args:
        data (xr.DataArray): input xarray time series
        from_date (pd.Timestamp, optional): date, convertible to a timestamp. Defaults to None.
        to_date (pd.Timestamp, optional): end date of the slice. Inclusive. Defaults to None.

    Returns:
        xr.DataArray: a subset time series

    Examples:
        slice_xr_time_series(unaccounted_indus, from_date='1980-04-01', to_date='2000-04-01')
    """
    dt = data.time.values
    tt = _time_interval_indx(dt, from_date, to_date)
    return data.sel(time=tt)

def slice_pd_time_series(data: pd.Series, from_date: pd.Timestamp = None, to_date: pd.Timestamp = None) -> pd.Series:
    """Subset a time series to a period

    Args:
        data (pd.Series): input xarray time series
        from_date (pd.Timestamp, optional): date, convertible to a timestamp. Defaults to None.
        to_date (pd.Timestamp, optional): end date of the slice. Inclusive. Defaults to None.

    Returns:
        pd.Series: a subset time series

    Examples:
        slice_pd_time_series(unaccounted_indus, from_date='1980-04-01', to_date='2000-04-01')
    """
    dt = data.index
    tt = _time_interval_indx(dt, from_date, to_date)
    return data[tt]

def ts_window(ts:Union[xr.DataArray, pd.Series], from_date: pd.Timestamp = None, to_date: pd.Timestamp = None):
    if isinstance(ts, xr.DataArray):
        return slice_xr_time_series(ts, from_date, to_date)
    elif isinstance(ts, pd.Series):
        return slice_pd_time_series(ts, from_date, to_date)
    else:
        raise TypeError("Not supported: " + str(type(ts)))

def start_ts(ts:Union[xr.DataArray, pd.Series]):
    if isinstance(ts, xr.DataArray):
        return xr_ts_start(ts)
    elif isinstance(ts, pd.Series):
        return ts.index[0]
    else:
        raise TypeError("Not supported: " + str(type(ts)))

def end_ts(ts:Union[xr.DataArray, pd.Series]):
    if isinstance(ts, xr.DataArray):
        return xr_ts_end(ts)
    elif isinstance(ts, pd.Series):
        return ts.index[-1]
    else:
        raise TypeError("Not supported: " + str(type(ts)))

def create_ensemble_series(npx:np.ndarray, ens_index:List, time_index:List) -> xr.DataArray:
    return xr.DataArray(npx, coords=[ens_index, time_index], dims=[ENSEMBLE_DIMNAME, TIME_DIMNAME])

def create_single_series(npx:np.ndarray, time_index:List) -> xr.DataArray:
    npx = npx.squeeze()
    assert len(npx.shape) == 1
    return xr.DataArray(npx, coords=[time_index], dims=[TIME_DIMNAME])

def pd_series_to_xr_series(series:pd.Series) -> xr.DataArray:
    return create_single_series(series.values, series.index)

def create_even_time_index(start:ConvertibleToTimestamp, time_step_seconds:int, n:int) -> List:
    start = as_timestamp(start)
    delta_t = np.timedelta64(time_step_seconds, 's')
    return [start + delta_t * i for i in range(n)]

def ts_geom_to_even_time_index(ts_geom:TimeSeriesGeometryNative) -> List:
    start = as_timestamp(ts_geom.start)
    if ts_geom.time_step_code > 0:
        raise NotImplementedError("Can only handle conversion of regular time steps, for now")
    return create_even_time_index(start, ts_geom.time_step_seconds, ts_geom.length)

def as_xarray_time_series(ffi:FFI, ptr:CffiData) -> xr.DataArray:
    ts_geom = TimeSeriesGeometryNative(ptr.time_series_geometry)
    # npx = two_d_as_np_array_double(ffi, ptr.numeric_data, ts_geom.length, ptr.ensemble_size, True)
    npx = two_d_as_np_array_double(ffi, ptr.numeric_data, ptr.ensemble_size, ts_geom.length, True)
    time_index = ts_geom_to_even_time_index(ts_geom)
    ens_index = [i for i in range(ptr.ensemble_size)]
    x = create_ensemble_series(npx, ens_index, time_index)
    # x.name = variableIdentifier
    return x

def geom_to_xarray_time_series(ts_geom:TimeSeriesGeometryNative, data:np.ndarray) -> xr.DataArray:
    assert len(data.shape) == 1
    data = data.reshape((1, len(data)))
    time_index = ts_geom_to_even_time_index(ts_geom)
    ens_index = [0]
    x = create_ensemble_series(data, ens_index, time_index)
    # x.name = variableIdentifier
    return x


def as_native_time_series(ffi:FFI, data:TimeSeriesLike) -> OwningCffiNativeHandle:
    ptr = ffi.new("multi_regular_time_series_data*")
    tsg = get_native_tsgeom(ffi, data)
    ptr.time_series_geometry = tsg.obj
    if isinstance(data, xr.DataArray):
        ensemble_size = len(data.coords[ENSEMBLE_DIMNAME].values)
        np_data = data.values
    elif isinstance(data, pd.Series):
        ensemble_size = 1
        np_data = data.values
    elif isinstance(data, pd.DataFrame):
        ensemble_size = data.shape[1]
        np_data = data.values.transpose()
    else:
        raise TypeError(
            "Not recognised as a type of time series: " + str(type(data)))
    ptr.ensemble_size = ensemble_size
    num_data = two_d_np_array_double_to_native(ffi, np_data)
    ptr.numeric_data = num_data.ptr
    result = OwningCffiNativeHandle(ptr)
    result.keepalive = [tsg, num_data]
    return result


def values_to_nparray(ffi:FFI, ptr:CffiData) -> np.ndarray:
    """Convert if possible a cffi pointer to a values_vector struct, into a python array

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData) to a values_vector struct

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        Dict[str,float]: converted data
    """
    return as_np_array_double(ffi, ptr.values, ptr.size, shallow=False)

def create_values_struct(ffi:FFI, data:np.ndarray) -> OwningCffiNativeHandle:
    ptr = ffi.new("values_vector*")
    ptr.size = len(data)
    ptr.values = as_c_double_array(ffi, data).ptr
    return OwningCffiNativeHandle(ptr)

def as_c_double_array(ffi:FFI, data:np.ndarray) -> OwningCffiNativeHandle:
    if isinstance(data, list):
        data = np.asfarray(data)
    elif isinstance(data, xr.DataArray):
        data = data.values
    elif not isinstance(data, np.ndarray):
        raise TypeError("Conversion to a c array of double requires list or np array as input")
    return OwningCffiNativeHandle(ffi.cast("double *", np.ascontiguousarray(data.ctypes.data)))

def as_c_char_array(ffi, data) -> OwningCffiNativeHandle:
    if isinstance(data, list):
        data = np.asfarray(data)
    elif not isinstance(data, np.ndarray):
        raise TypeError("Conversion to a c array of double requires list or np array as input")
    return OwningCffiNativeHandle(ffi.cast("char *", np.ascontiguousarray(data.ctypes.data)))

def two_d_as_np_array_double(ffi:FFI, ptr:CffiData, nrow:int, ncol:int, shallow:bool=False) -> np.ndarray:
    """Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData)
        nrow (int): number of rows
        ncol (int): number of columns 
        shallow (bool): If true the array points directly to native data array. Defaults to False.

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        np.ndarray: converted data
    """
    # TODO check type
    rows = ffi.cast('double*[%d]' % (nrow,), ptr)
    res = np.vstack([as_numeric_np_array(ffi, rows[i], size=ncol, shallow=False) for i in range(nrow)])
    if shallow:
        return res
    else:
        return res.copy()

def two_d_np_array_double_to_native(ffi:FFI, data:np.ndarray, shallow:bool=False) -> OwningCffiNativeHandle:
    """Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        data (np.ndarray): data
        shallow (bool): If true the array points directly to native data array. Defaults to False.

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        np.ndarray: converted data
    """
    if not isinstance(data, np.ndarray):
        raise TypeError(
            "Expected np.ndarray, got " + str(type(data)))
    if not len(data.shape) < 3:
        raise TypeError("Expected an array of dimension 1 or 2, got " + str(len(data.shape)))

    if len(data.shape) == 1:
        data = data.reshape((1, len(data)))

    nrow = data.shape[0]
    ptr = new_doubleptr_array(ffi, nrow)
    items = [as_c_double_array(ffi, data[i,:]).ptr for i in range(nrow)]
    for i in range(nrow):
        ptr[i] = items[i]
    result = OwningCffiNativeHandle(ptr)
    result.keepalive = items
    return result

def c_string_as_py_string(ffi:FFI, ptr:CffiData) -> str:
    """Convert if possible a cffi pointer to an ANSI C string <char*> to a python string.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData)

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        str: converted string
    """
    return as_string(ffi.string(ptr))

def c_charptrptr_as_string_list(ffi:FFI, ptr:CffiData, size:int) -> List[str]:
    """Convert if possible a cffi pointer to a C data array char** , into a list of python strings.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData)
        size (int): number of character strings in the char** pointer

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        List[str]: converted data
    """
    # TODO check type
    strings = ffi.cast('char*[%d]' % (size,), ptr)
    res = [as_string(ffi.string(strings[i])) for i in range(size)]
    return res

def dtts_as_datetime(ptr:CffiData) -> datetime:
    """Convert if possible a cffi pointer to a C data array char** , into a list of python strings.

    Args:
        ptr (CffiData): cffi pointer (FFI.CData)

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        datetime: converted data
    """
    dtts = ptr # ffi.cast('date_time_to_second*', ptr)
    return datetime(dtts.year, dtts.month, dtts.day, dtts.hour, dtts.minute, dtts.second)

def _copy_datetime_to_dtts(dt: datetime, ptr):
    ptr.year = dt.year
    ptr.month = dt.month
    ptr.day = dt.day
    ptr.hour = dt.hour
    ptr.minute = dt.minute
    ptr.second = dt.second

def datetime_to_dtts(ffi:FFI, dt: datetime) -> OwningCffiNativeHandle:
    ptr = ffi.new("date_time_to_second*")
    _copy_datetime_to_dtts(dt, ptr)
    return OwningCffiNativeHandle(ptr)

def as_bytes(obj:Any) -> Union[bytes, Any]:
    """Convert obj to bytes if it is a string type

    Args:
        obj (Any): object to convert

    Returns:
        Union[bytes, Any]: object converted to bytes if it was a type of string
    """    
    if isinstance(obj, bytes):
        return obj
    elif isinstance(obj, six.string_types):
        return obj.encode('utf-8')
    else:
        return obj

def as_arrayof_bytes(ffi:FFI, obj:List[Any]) -> OwningCffiNativeHandle:
    """Convert a list of "strings" to a char** like C array

    Args:
        obj (List): list of objects (strings) to convert

    Returns:
        List: objects converted to bytes if it was a type of string
    """
    ptr = new_charptr_array(ffi, len(obj))
    items = [ffi.new("char[]", as_bytes(obj[i])) for i in range(len(obj))]
    for i in range(len(obj)):
        ptr[i] = items[i]
    result = OwningCffiNativeHandle(ptr)
    result.keepalive = items
    return result

def as_character_vector(ffi:FFI, obj:List[Any]) -> OwningCffiNativeHandle:
    """Convert a list of "strings" to a character_vector* native struct"""
    cv = ffi.new("character_vector*")
    cv.size = len(obj)
    names = as_arrayof_bytes(ffi, obj)
    cv.values = names.ptr
    result = OwningCffiNativeHandle(cv)
    result.keepalive = names
    return result

def as_string(obj:Any) -> Union[str, Any]:
    """Convert obj to string/unicode if it is a bytes object.

    Args:
        obj (Any): object to convert

    Returns:
        Union[str, Any]: result converted (or not) to unicode string
    """
    if isinstance(obj, bytes):
        return obj.decode('utf-8')
    return obj


def convert_strings(func):
    """Returns a wrapper that converts any str/unicode object arguments to
       bytes.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Convert args.

           :param func func: Python function wrapping a lakeoned function.
        """
        new_args = []
        for arg in args:
            new_args.append(as_bytes(arg))
        new_kwargs = {}
        for key in kwargs:
            new_kwargs[key] = as_bytes(kwargs[key])

        # Call the function
        return_value = func(*new_args, **new_kwargs)
        if isinstance(return_value, (list, tuple)):
            return [as_string(obj) for obj in return_value]
        else:
            return as_string(return_value)

    return wrapper


class CffiMarshal:
    """A helper class for marshalling data to/from a native library module (i.e. DLL)
    """    
    def __init__(self, ffi:FFI) -> None:
        self._ffi:FFI = ffi

    def as_numeric_np_array(self, ptr:CffiData, size:int, shallow:bool=False) -> np.ndarray:
        """Convert if possible a cffi pointer to a C data array, into a numpy array.

        Args:
            ptr (CffiData): cffi pointer (FFI.CData)
            size (int): array size
            shallow (bool): If true the array points directly to native data array. Defaults to False.

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            np.ndarray: converted data
        """    
        return as_numeric_np_array(self._ffi, ptr, size, shallow)

    def as_np_array_double(self, ptr:CffiData, size:int, shallow:bool=False) -> np.ndarray:
        """Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.

        Args:
            ptr (CffiData): cffi pointer (FFI.CData)
            size (int): array size
            shallow (bool): If true the array points directly to native data array. Defaults to False.

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            np.ndarray: converted data
        """    
        return as_np_array_double(self._ffi, ptr, size, shallow)

    def two_d_as_np_array_double(self, ptr:CffiData, nrow:int, ncol:int, shallow:bool=False) -> np.ndarray:
        """Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.

        Args:
            ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
            ptr (CffiData): cffi pointer (FFI.CData)
            nrow (int): number of rows
            ncol (int): number of columns 
            shallow (bool): If true the array points directly to native data array. Defaults to False.

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            np.ndarray: converted data
        """
        return two_d_as_np_array_double(self._ffi, ptr, nrow, ncol, shallow)

    def c_string_as_py_string(self, ptr:CffiData) -> str:
        """Convert if possible a cffi pointer to an ANSI C string <char*> to a python string.

        Args:
            ptr (CffiData): cffi pointer (FFI.CData)

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            str: converted string
        """
        return c_string_as_py_string(self._ffi, ptr)

    def dict_to_named_values(self, data:Dict[str,float]) -> OwningCffiNativeHandle:
        return dict_to_named_values(self._ffi, data)

    def new_int_array(self, size) -> CffiData:
        return new_int_array(self._ffi, size)

    def new_int_scalar_ptr(self, value:int=0) -> CffiData:
        return new_int_scalar_ptr(self._ffi, value)

    def c_charptrptr_as_string_list(self, ptr:CffiData, size:int) -> List[str]:
        """Convert if possible a cffi pointer to a C data array char** , into a list of python strings.

        Args:
            ptr (CffiData): cffi pointer (FFI.CData)
            size (int): number of character strings in the char** pointer

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            List[str]: converted data
        """
        return c_charptrptr_as_string_list(self._ffi, ptr, size)

    def character_vector_as_string_list(self, ptr:CffiData) -> List[str]:
        """Convert if possible a cffi pointer to a C character_vector , into a list of python strings.

        Args:
            ptr (CffiData): cffi pointer (FFI.CData)

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            List[str]: converted data
        """
        return self.c_charptrptr_as_string_list( ptr.values, ptr.size)

    def as_datetime(self, ptr:CffiData) -> datetime:
        """Convert if possible a cffi pointer to a C date_time_to_second struct, into a datetime

        Args:
            ptr (CffiData): cffi pointer (FFI.CData)

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            datetime: converted data
        """
        return dtts_as_datetime(ptr)

    def datetime_to_dtts(self, dt: datetime) -> OwningCffiNativeHandle:
        return datetime_to_dtts(self._ffi, dt)

    def as_arrayof_bytes(self, obj:List[Any]) -> OwningCffiNativeHandle:
        """Convert a list of "strings" to a char** like C array"""
        return as_arrayof_bytes(self._ffi, obj)

    def as_character_vector(self, obj:List[Any]) -> OwningCffiNativeHandle:
        """Convert a list of "strings" to a character_vector* native struct"""
        return as_character_vector(self._ffi, obj)

    def named_values_to_dict(self, ptr:CffiData) -> Dict[str,float]:
        """Convert if possible a cffi pointer to a named_values_vector struct, into a dictionary

        Args:
            ptr (CffiData): cffi pointer (FFI.CData) to a named_values_vector struct

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            Dict[str,float]: converted data
        """
        return named_values_to_dict(self._ffi, ptr)

    def string_map_to_dict(self, ptr:CffiData) -> Dict[str,str]:
        """Convert if possible a cffi pointer to a string_string_map struct, into a dictionary

        Args:
            ptr (CffiData): cffi pointer (FFI.CData) to a string_string_map struct

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            Dict[str,str]: converted data
        """
        return string_map_to_dict(self._ffi, ptr)

    def dict_to_string_map(self, data:Dict[str,str]) -> OwningCffiNativeHandle:
        return dict_to_string_map(self._ffi, data)

    def as_charptr(self, x:str) -> CffiData:
        return as_charptr(self._ffi, x)

    def values_to_nparray(self, ptr:CffiData) -> Dict[str,float]:
        """Convert if possible a cffi pointer to a values_vector struct, into a python array

        Args:
            ptr (CffiData): cffi pointer (FFI.CData) to a values_vector struct

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            Dict[str,float]: converted data
        """
        return values_to_nparray(self._ffi, ptr)

    def create_values_struct(self, data:Iterable[float]) -> OwningCffiNativeHandle:
        return create_values_struct(self._ffi, data)

    def time_series_geometry(self, ptr:CffiData) -> TimeSeriesGeometry:
        return time_series_geometry(self._ffi, ptr)

    def as_native_tsgeom(self, tsgeom:TimeSeriesGeometry) -> TimeSeriesGeometryNative:
        return tsgeom.as_native(self._ffi)

    def as_xarray_time_series(self, ptr:CffiData) -> xr.DataArray:
        return as_xarray_time_series(self._ffi, ptr)

    def get_native_tsgeom(self, pd_series:pd.Series) -> OwningCffiNativeHandle:
        return get_native_tsgeom(self._ffi, pd_series)

    def new_native_tsgeom(self) -> TimeSeriesGeometryNative:
        return TimeSeriesGeometryNative(self._ffi)

    def new_native_struct(self, type) -> OwningCffiNativeHandle:
        return OwningCffiNativeHandle(self._ffi.new(type), type)

    def as_c_double_array(self, data:np.ndarray) -> OwningCffiNativeHandle:
        return as_c_double_array(self._ffi, data)
    
    def as_c_char_array(self, data:np.ndarray) -> OwningCffiNativeHandle:
        return as_c_char_array(self._ffi, data)

    def as_native_time_series(self, data:TimeSeriesLike) -> OwningCffiNativeHandle:
        return as_native_time_series(self._ffi, data)



def as_bytes(obj:Any) -> Union[bytes, Any]:
    """Convert obj to bytes if it is a string type

    Args:
        obj (Any): object to convert

    Returns:
        Union[bytes, Any]: object converted to bytes if it was a type of string
    """    
    if isinstance(obj, bytes):
        return obj
    elif isinstance(obj, six.string_types):
        return obj.encode('utf-8')
    else:
        return obj

def as_string(obj:Any) -> Union[str, Any]:
    """Convert obj to string/unicode if it is a bytes object.

    Args:
        obj (Any): object to convert

    Returns:
        Union[str, Any]: result converted (or not) to unicode string
    """
    if isinstance(obj, bytes):
        return obj.decode('utf-8')
    return obj
