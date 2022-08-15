
import numpy as np
from functools import wraps

from typing import Any, Dict, Iterable, List, Union, TYPE_CHECKING
from typing_extensions import TypeAlias 

from cffi import FFI
import six
from refcount.interop import CffiNativeHandle, OwningCffiNativeHandle
from datetime import datetime
import xarray as xr
import pandas as pd

from ..timeseries import ConvertibleToTimestamp, TimeSeriesLike, as_datetime64, as_pydatetime, as_timestamp, create_even_time_index, create_monthly_time_index

from refcount.interop import CffiData

NativePointerLike:TypeAlias = Union[OwningCffiNativeHandle, CffiNativeHandle, CffiData]
"""types that can represent time series 
"""
# if TYPE_CHECKING:


_c2dtype = dict()
"""Mapping from a C pointer type to a numpy dtypes"""

_c2dtype[ 'float *' ] = np.dtype( 'f4' )
_c2dtype[ 'double *' ] = np.dtype( 'f8' )
# _c2dtype[ 'int *' ] = np.dtype( 'i4' ) TBD

def __check_positive_size(size):
    if size < 0 : raise ValueError(f"array size must be positive, but got {size}")

def new_int_scalar_ptr(ffi:FFI, value:int=0) -> "CffiData":
    """Creates a new C array of integers

    Args:
        ffi (FFI): ffi object to the native library accessed
        value (int, optional): _description_. Defaults to 0.

    Returns:
        CffiData: a cdata pointer object owning a new pointer to a single integer valued as specified.
    """
    ptr = ffi.new('int*')
    ptr[0] = value
    return ptr

def new_ctype_array(ffi:FFI, ctype:str, size:int, wrap:bool=False) -> Union[OwningCffiNativeHandle,CffiData]:
    """_summary_

    Args:
        ffi (FFI): ffi object to the native library accessed
        ctype (str): valid C type for array creation 
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: cdata pointer or wrapper to it.
    """
    __check_positive_size(size)
    x = ffi.new('%s[%d]' % (ctype,size))
    if wrap:
        return OwningCffiNativeHandle(x)
    else:
        return x

def new_int_array(ffi:FFI, size:int, wrap:bool=False) -> Union[OwningCffiNativeHandle,CffiData]:
    """Creates a new C array of integers `int[n]`

    Args:
        ffi (FFI): ffi object to the native library accessed
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of integers of length `size`
    """
    return new_ctype_array(ffi, "int", size, wrap)

def new_double_array(ffi:FFI, size:int, wrap:bool=False) -> Union[OwningCffiNativeHandle,CffiData]:
    """Creates a new C array of double precision floats `double[n]`

    Args:
        ffi (FFI): ffi object to the native library accessed
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of `double`s of length `size`
    """    
    return new_ctype_array(ffi, "double", size, wrap)

def new_doubleptr_array(ffi:FFI, size:int, wrap:bool=False) -> Union[OwningCffiNativeHandle,CffiData]:
    """Creates a new C array of pointers to double precision floats `double*[n]`

    Args:
        ffi (FFI): ffi object to the native library accessed
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of `double *`s of length `size`
    """    
    return new_ctype_array(ffi, "double*", size, wrap)

def new_charptr_array(ffi:FFI, size:int, wrap:bool=False) -> Union[OwningCffiNativeHandle,CffiData]:
    """Creates a new C array of pointers to char:  `char*[n]`

    Args:
        ffi (FFI): ffi object to the native library accessed
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a)  cdata pointer object owning a new array of `char *`s of length `size`
    """
    return new_ctype_array(ffi, "char*", size, wrap)

def as_charptr(ffi:FFI, x:str, wrap:bool=False) -> Union[OwningCffiNativeHandle,CffiData]:
    """convert an object to `bytes`, create as C array of char and copy values to it. Equivalent to `char arg[] = "world"` if x is the bytes b"world"

    Args:
        ffi (FFI): ffi object to the native library accessed
        x (str): a string-like object; bytes or str, or string like object that can be encoded to bytes (six.string_like)
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of `char *`s of length `size`
    """
    x = ffi.new("char[]", as_bytes(x))
    if wrap:
        return OwningCffiNativeHandle(x)
    else:
        return x

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
        raise RuntimeError( "Cannot (yet)create an array for element type: %s" % t )
    dtype = _c2dtype[t]
    buffer_size = size*dtype.itemsize
    res = np.frombuffer( ffi.buffer( ptr, buffer_size ), dtype )
    if shallow:
        return res
    else:
        return res.copy()

def as_np_array_double(ffi:FFI, ptr:CffiData, size:int, shallow:bool=False) -> np.ndarray:
    """Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats `double[n]`.
        The returned numpy array may be directly pointing to the original data (faster performance), or a deep copy (memory safety - "normal" numpy array)

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData)
        size (int): array size
        shallow (bool): If True the resulting numpy array points directly to the native data array. 
        Otherwise, return a numpy array with a deep copy of the data, managed by Python. 
        Defaults to False.

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
    """Convert if possible a cffi pointer to a `named_values_vector` struct, into a dictionary

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData) to a `named_values_vector` struct

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
    """Convert a dictionary to a cffi pointer to a `named_values_vector` struct

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        data (Dict[str,float]): mapping from keys to numeric values

    Returns:
        OwningCffiNativeHandle: A wrapper that owns the memory allocated for the resulting `named_values_vector` pointed to
    """
    ptr = ffi.new("named_values_vector*")
    ptr.size = len(data)
    ptr.values = as_c_double_array(ffi, list(data.values())).ptr
    names = as_arrayof_bytes(ffi, list(data.keys()))
    ptr.names = names.ptr
    result = OwningCffiNativeHandle(ptr)
    result.keepalive = names
    return result

def string_map_to_dict(ffi:FFI, ptr:CffiData) -> Dict[str,str]:
    """Convert if possible a cffi pointer to a `string_string_map` struct, into a dictionary

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData) to a `string_string_map` struct

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
    """Convert a dictionary to a cffi pointer to a `string_string_map` struct

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        data (Dict[str,float]): mapping from keys to (str) values

    Returns:
        OwningCffiNativeHandle: A wrapper that owns the memory allocated for the resulting `string_string_map` pointed to.
    """
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
    """Simplified representation of the temporal geometry of a time series. 
    Suitable for interop with the C struct `regular_time_series_geometry`
    """    
    def __init__(self, start:ConvertibleToTimestamp=None, time_step_seconds:int=3600, length:int=1, time_step_code:int=0):
        """Simplified representation of the temporal geometry of a time series.
        Suitable for interop with the C struct `regular_time_series_geometry`

        Args:
            start (ConvertibleToTimestamp, optional): Start date of a time series. Defaults to None.
            time_step_seconds (int, optional): time step length in seconds, used if this is a regular time step. Defaults to 3600.
            length (int, optional): number of items in the time series. Defaults to 1.
            time_step_code (int, optional): type of time step: 0 for even time steps, or 1 for monthly, in which case `time_step_seconds` is overriden. Defaults to 0.
        """        
        self.start = start if start is not None else as_pydatetime("1970-01-01")
        self.time_step_seconds = time_step_seconds
        self.length = length
        self.time_step_code = time_step_code

    def as_native(self, ffi:FFI):
        """C-compatible representation of a time series geometry

        Args:
            ffi (FFI): FFI instance wrapping the native compilation module owning the native memory

        Returns:
            TimeSeriesGeometryNative: wrapper around a cdata pointer to a new C struct `regular_time_series_geometry`
        """
        return TimeSeriesGeometryNative(ffi, self.start, self.time_step_seconds, self.length, self.time_step_code)

class TimeSeriesGeometryNative(OwningCffiNativeHandle):
    """Wrapper around a cdata pointer to a new C struct `regular_time_series_geometry`"""
    def __init__(self, ffi:Union[FFI, CffiData], start:ConvertibleToTimestamp=None, time_step_seconds:int=3600, length:int=1, time_step_code:int=0):
        """Wrapper around a cdata pointer to a new C struct `regular_time_series_geometry`

        Args:
            ffi (Union[FFI, CffiData]): FFI instance, or a preexisting cdata pointer to a `regular_time_series_geometry` struct
            start (ConvertibleToTimestamp, optional): Start date of a time series. Defaults to None.
            time_step_seconds (int, optional): time step length in seconds, used if this is a regular time step. Defaults to 3600.
            length (int, optional): number of items in the time series. Defaults to 1.
            time_step_code (int, optional): type of time step: 0 for even time steps, or 1 for monthly, in which case `time_step_seconds` is overriden. Defaults to 0.
        """        
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

def as_native_tsgeom(ffi:FFI, tsgeom:TimeSeriesGeometry) -> TimeSeriesGeometryNative:
    """convert a simlified time series geometry to a native representation

    Args:
        ffi (Union[FFI, CffiData]): FFI instance, or a preexisting cdata pointer to a `regular_time_series_geometry` struct
        tsgeom (TimeSeriesGeometry): simplified representation

    Returns:
        TimeSeriesGeometryNative: Wrapper around a cdata pointer to a new C struct `regular_time_series_geometry`
    """    
    return tsgeom.as_native(ffi)

def _pd_index(x):
    if not isinstance(x.index, pd.DatetimeIndex):
        raise TypeError("pandas structure; but the index is not an DatetimeIndex")
    return x.index

def get_tsgeom(data:TimeSeriesLike) -> TimeSeriesGeometry:
    """Extract a simplified representation of the geometry of a time series. A simple heuristic is used to find the time step

    Args:
        data (TimeSeriesLike): A pandas or xarray representation of a time series, with the pandas index or "time" dimension expected. 

    Raises:
        TypeError: Unexpected type of data

    Returns:
        TimeSeriesGeometry: simplified time series geometry
    """    
    if isinstance(data, xr.DataArray):
        indx = data.coords[TIME_DIMNAME].values
    elif isinstance(data, pd.Series):
        indx = _pd_index(data)
    elif isinstance(data, pd.DataFrame):
        indx = _pd_index(data)
    else:
        raise TypeError(
            "Not recognised as a type of time series: " + str(type(data)))
    if len(indx) < 2:
        raise ValueError("There must be at least two entries in the time series to guess the time step length")
    a = as_timestamp(indx[0])
    b = as_timestamp(indx[1])
    first_delta = b-a
    time_step_code = 0
    time_step = int(first_delta.total_seconds())
    if time_step > 86400 * 27: # HACK: assume monthly
        time_step_code = 1
        time_step = -1
    return TimeSeriesGeometry(a, time_step, len(indx), time_step_code)

def get_native_tsgeom(ffi:FFI, pd_series:"TimeSeriesLike") -> OwningCffiNativeHandle:
    # stopifnot(xts::is.xts(pd_series))
    return as_native_tsgeom(ffi, get_tsgeom(pd_series))

## TODO: Generic, non interop time series functions should go "elsewhere"

TIME_DIMNAME="time"
ENSEMBLE_DIMNAME="ensemble"


def __ts_index(x:TimeSeriesLike):
    if isinstance(x, pd.Series) or isinstance(x, pd.DataFrame):
        return _pd_index(x)
    elif isinstance(x, xr.DataArray):
        return x.coords[TIME_DIMNAME].values
    else:
        raise TypeError("Not supported as a representation of a time series: " + str(type(x)))

def start_ts(x:TimeSeriesLike):
    """Gets the starting date of a time series

    Args:
        x (TimeSeriesLike): time series

    Returns:
        Any: start of the series
    """    
    return __ts_index(x)[0]

def end_ts(x:TimeSeriesLike):
    """Gets the ending date of a time series

    Args:
        x (TimeSeriesLike): time series

    Returns:
        Any: end of the series
    """
    return __ts_index(x)[-1]

# TODO: legacy, I think.
xr_ts_start = start_ts
xr_ts_end = end_ts

def _time_interval_indx(dt:np.ndarray, from_date: ConvertibleToTimestamp = None, to_date: ConvertibleToTimestamp = None) -> np.ndarray:
    tt = np.empty_like(dt, bool)
    tt[:] = True
    if from_date is not None:
        tt = np.logical_and(tt, (dt >= as_datetime64(from_date)))
    if to_date is not None:
        tt = np.logical_and(tt, (dt <= as_datetime64(to_date)))
    return tt

def slice_xr_time_series(data: xr.DataArray, from_date: ConvertibleToTimestamp = None, to_date: ConvertibleToTimestamp = None) -> xr.DataArray:
    """Subset a time series to a period

    Args:
        data (xr.DataArray): input xarray time series
        from_date (ConvertibleToTimestamp, optional): date, convertible to a timestamp. Defaults to None.
        to_date (ConvertibleToTimestamp, optional): end date of the slice. Inclusive. Defaults to None.

    Returns:
        xr.DataArray: a subset time series

    Examples:
        slice_xr_time_series(unaccounted_indus, from_date='1980-04-01', to_date='2000-04-01')
    """
    dt = data.time.values
    tt = _time_interval_indx(dt, from_date, to_date)
    return data.sel(time=tt)

def slice_pd_time_series(data: pd.Series, from_date: ConvertibleToTimestamp = None, to_date: ConvertibleToTimestamp = None) -> pd.Series:
    """Subset a time series to a period

    Args:
        data (pd.Series): input xarray time series
        from_date (ConvertibleToTimestamp, optional): date, convertible to a timestamp. Defaults to None.
        to_date (ConvertibleToTimestamp, optional): end date of the slice. Inclusive. Defaults to None.

    Returns:
        pd.Series: a subset time series

    Examples:
        slice_pd_time_series(unaccounted_indus, from_date='1980-04-01', to_date='2000-04-01')
    """
    dt = data.index
    tt = _time_interval_indx(dt, from_date, to_date)
    return data[tt]

def ts_window(ts:TimeSeriesLike, from_date: ConvertibleToTimestamp = None, to_date: ConvertibleToTimestamp = None) -> Any:
    """Gets a temporal window of a time series 

    Args:
        ts (TimeSeriesLike): pandas dataframe, series, or xarray DataArray
        from_date (ConvertibleToTimestamp, optional): start date of the window. Defaults to None.
        to_date (ConvertibleToTimestamp, optional): end date of the window. Defaults to None.

    Raises:
        TypeError: _description_

    Returns:
        TimeSeriesLike: Subset window of the full time series

    Examples:
        ts_window(unaccounted_indus, from_date='1980-04-01', to_date='2000-04-01')
    """    
    if isinstance(ts, xr.DataArray):
        return slice_xr_time_series(ts, from_date, to_date)
    elif isinstance(ts, pd.Series):
        return slice_pd_time_series(ts, from_date, to_date)
    else:
        raise TypeError("Not supported: " + str(type(ts)))


def create_ensemble_series(npx:np.ndarray, ens_index:List, time_index:Union[List,pd.DatetimeIndex]) -> xr.DataArray:
    """Create an ensemble (i.e. special type of multi-variate) time series"""
    return xr.DataArray(npx, coords=[ens_index, time_index], dims=[ENSEMBLE_DIMNAME, TIME_DIMNAME])

def create_single_series(npx:np.ndarray, time_index:Union[List,pd.DatetimeIndex]) -> xr.DataArray:
    """Create an uni-variate time series"""
    npx = npx.squeeze()
    assert len(npx.shape) == 1
    return xr.DataArray(npx, coords=[time_index], dims=[TIME_DIMNAME])

def pd_series_to_xr_series(series:pd.Series) -> xr.DataArray:
    """Converts a pandas series to an xarray"""
    assert isinstance(series, pd.Series)
    return create_single_series(series.values, series.index)

def _ts_geom_to_time_index(ts_geom:TimeSeriesGeometryNative) -> Union[List, pd.DatetimeIndex]:
    start = as_timestamp(ts_geom.start)
    if ts_geom.time_step_code == 0:
        return create_even_time_index(start, ts_geom.time_step_seconds, ts_geom.length)
    if ts_geom.time_step_code == 1:
        return create_monthly_time_index(start, ts_geom.length)
    else:
        raise NotImplementedError("Unrecognised time step code '{}'".format(ts_geom.time_step_code))

def as_xarray_time_series(ffi:FFI, ptr:CffiData) -> xr.DataArray:
    """as_xarray_time_series"""
    ts_geom = TimeSeriesGeometryNative(ptr.time_series_geometry)
    # npx = two_d_as_np_array_double(ffi, ptr.numeric_data, ts_geom.length, ptr.ensemble_size, True)
    npx = two_d_as_np_array_double(ffi, ptr.numeric_data, ptr.ensemble_size, ts_geom.length, True)
    time_index = _ts_geom_to_time_index(ts_geom)
    ens_index = [i for i in range(ptr.ensemble_size)]
    x = create_ensemble_series(npx, ens_index, time_index)
    # x.name = variableIdentifier
    return x

def geom_to_xarray_time_series(ts_geom:TimeSeriesGeometryNative, data:np.ndarray) -> xr.DataArray:
    """geom_to_xarray_time_series"""
    assert len(data.shape) == 1
    data = data.reshape((1, len(data)))
    time_index = _ts_geom_to_time_index(ts_geom)
    ens_index = [0]
    x = create_ensemble_series(data, ens_index, time_index)
    # x.name = variableIdentifier
    return x


def as_native_time_series(ffi:FFI, data:TimeSeriesLike) -> OwningCffiNativeHandle:
    """as_native_time_series"""
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

def is_cffi_c_data(ptr:NativePointerLike) -> bool:
    """is_cffi_c_data"""
    return isinstance(ptr, FFI.CData)

def is_native_time_series(ptr:NativePointerLike) -> bool:
    """is_native_time_series"""
    if is_cffi_c_data(ptr):
        ptr.type_id


def values_to_nparray(ffi:FFI, ptr:CffiData) -> np.ndarray:
    """Convert if possible a cffi pointer to a `values_vector` struct, into a python array

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData) to a `values_vector` struct

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        Dict[str,float]: converted data
    """
    return as_np_array_double(ffi, ptr.values, ptr.size, shallow=False)

def create_values_struct(ffi:FFI, data:np.ndarray) -> OwningCffiNativeHandle:
    """create_values_struct"""
    ptr = ffi.new("values_vector*")
    ptr.size = len(data)
    ptr.values = as_c_double_array(ffi, data).ptr
    return OwningCffiNativeHandle(ptr)

def as_c_double_array(ffi:FFI, data:np.ndarray, shallow:bool=False) -> OwningCffiNativeHandle:
    if isinstance(data, list):
        data = np.asfarray(data)
        shallow = False
    elif isinstance(data, xr.DataArray):
        data = data.values
        # shallow = False # really needed??
    elif not isinstance(data, np.ndarray):
        raise TypeError("Conversion to a c array of double requires list or np array as input")
    if len(data.shape) > 1:
        data = data.squeeze()
        shallow = False
        if len(data.shape) > 1:
            raise TypeError("Conversion to a double* array: input data must be of dimension one, and the python array cannot be squeezed to dimension one")
    if not (data.dtype == np.float64 or data.dtype == float or data.dtype == np.double or data.dtype == np.float_):
        # https://numpy.org/devdocs/release/1.20.0-notes.html#deprecations
        # TODO: is this wise to override the shallow parameter
        shallow = False
        data = data.astype(np.float64)
    if shallow and data.flags['C_CONTIGUOUS']:
        native_d = ffi.cast("double *", data.ctypes.data)
    else:
        native_d = new_double_array(ffi, data.shape[0])
        if not data.flags['C_CONTIGUOUS']:
            data_c = np.ascontiguousarray(data)
        else:
            data_c = data
        ffi.buffer(native_d)[:] = data_c
    return OwningCffiNativeHandle(native_d)

def as_c_char_array(ffi, data, shallow:bool=False) -> OwningCffiNativeHandle:
    """as_c_char_array"""
    if isinstance(data, list):
        data = np.asfarray(data)
        shallow = False
    elif not isinstance(data, np.ndarray):
        raise TypeError("Conversion to a c array of double requires list or np array as input")
    if shallow and data.flags['C_CONTIGUOUS']:
        native_d = ffi.cast("char *", data.ctypes.data)
    else:
        native_d = new_charptr_array(ffi, data.shape[0])
        if not data.flags['C_CONTIGUOUS']:
            data_c = np.ascontiguousarray(data.ctypes.data)
        else:
            data_c = data
        ffi.buffer(native_d)[:] = data_c
    return OwningCffiNativeHandle(native_d)

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
    if nrow == 0 or ncol == 0: # do not cast a native ptr that is likely nullptr or worse. Following works thankfully as an edge case.
        return np.ndarray(shape=(nrow, ncol))
    else:
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
    """datetime_to_dtts"""
    ptr = ffi.new("date_time_to_second*")
    _copy_datetime_to_dtts(dt, ptr)
    return OwningCffiNativeHandle(ptr)

def new_date_time_to_second(ffi:FFI) -> OwningCffiNativeHandle:
    """new_date_time_to_second"""
    ptr = ffi.new("date_time_to_second*")
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

    @property
    def nullptr(self):
        return FFI.NULL

    def as_np_array_double(self, ptr:CffiData, size:int, shallow:bool=False) -> np.ndarray:
        """Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats `double[n]`.
            The returned numpy array may be directly pointing to the original data (faster performance), or a deep copy (memory safety - "normal" numpy array)

        Args:
            ptr (CffiData): cffi pointer (FFI.CData)
            size (int): array size
            shallow (bool): If True the resulting numpy array points directly to the native data array. 
            Otherwise, return a numpy array with a deep copy of the data, managed by Python. 
            Defaults to False.

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            np.ndarray: converted data
        """    
        return as_np_array_double(self._ffi, ptr, size, shallow)

    def two_d_as_np_array_double(self, ptr:CffiData, nrow:int, ncol:int, shallow:bool=False) -> np.ndarray:
        """Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.

        Args:
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
        """Convert a dictionary to a cffi pointer to a `named_values_vector` struct

        Args:
            data (Dict[str,float]): mapping from keys to numeric values

        Returns:
            OwningCffiNativeHandle: A wrapper that owns the memory allocated for the resulting `named_values_vector` pointed to
        """
        return dict_to_named_values(self._ffi, data)

    def new_int_array(self, size:int) -> "CffiData":
        """Creates a new C array of integers `int[n]`

        Args:
            size (int): array size
            wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

        Returns:
            Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of integers of length `size`
        """
        return new_int_array(self._ffi, size)

    def new_int_scalar_ptr(self, value:int=0) -> "CffiData":
        """Creates a new C array of integers

        Args:
            value (int, optional): _description_. Defaults to 0.

        Returns:
            CffiData: a cdata pointer object owning a new pointer to a single integer valued as specified.
        """
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
        """Convert if possible a cffi pointer to a `named_values_vector` struct, into a dictionary

        Args:
            ptr (CffiData): cffi pointer (FFI.CData) to a `named_values_vector` struct

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            Dict[str,float]: converted data
        """
        return named_values_to_dict(self._ffi, ptr)

    def string_map_to_dict(self, ptr:CffiData) -> Dict[str,str]:
        """Convert if possible a cffi pointer to a `string_string_map` struct, into a dictionary

        Args:
            ptr (CffiData): cffi pointer (FFI.CData) to a `string_string_map` struct

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            Dict[str,str]: converted data
        """
        return string_map_to_dict(self._ffi, ptr)

    def dict_to_string_map(self, data:Dict[str,str]) -> OwningCffiNativeHandle:
        return dict_to_string_map(self._ffi, data)

    def as_charptr(self, x:str, wrap=False) -> "CffiData":
        """convert an object to `bytes`, create as C array of char and copy values to it. Equivalent to `char arg[] = "world"` if x is the bytes b"world"

        Args:
            x (str): a string-like object; bytes or str, or string like object that can be encoded to bytes (six.string_like)
            wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

        Returns:
            Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of `char *`s of length `size`
        """
        return as_charptr(self._ffi, x, wrap)

    def values_to_nparray(self, ptr:CffiData) -> Dict[str,float]:
        """Convert if possible a cffi pointer to a `values_vector` struct, into a python array

        Args:
            ptr (CffiData): cffi pointer (FFI.CData) to a `values_vector` struct

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            Dict[str,float]: converted data
        """
        return values_to_nparray(self._ffi, ptr)

    def create_values_struct(self, data:Iterable[float]) -> OwningCffiNativeHandle:
        return create_values_struct(self._ffi, data)

    # def time_series_geometry(self, ptr:CffiData) -> TimeSeriesGeometry:
    #     return time_series_geometry(self._ffi, ptr)

    def as_native_tsgeom(self, tsgeom:TimeSeriesGeometry) -> TimeSeriesGeometryNative:
        """C-compatible representation of a time series geometry

        Returns:
            TimeSeriesGeometryNative: wrapper around a cdata pointer to a new C struct `regular_time_series_geometry`
        """
        return tsgeom.as_native(self._ffi)

    def as_xarray_time_series(self, ptr:CffiData) -> xr.DataArray:
        return as_xarray_time_series(self._ffi, ptr)

    def get_native_tsgeom(self, pd_series:pd.Series) -> OwningCffiNativeHandle:
        return get_native_tsgeom(self._ffi, pd_series)

    def new_native_tsgeom(self) -> TimeSeriesGeometryNative:
        return TimeSeriesGeometryNative(self._ffi)

    def new_date_time_to_second(self) -> OwningCffiNativeHandle:
        return new_date_time_to_second(self._ffi)

    def new_native_struct(self, type) -> OwningCffiNativeHandle:
        return OwningCffiNativeHandle(self._ffi.new(type), type)

    def new_ctype_array(self, ctype:str, size:int, wrap=False) -> Union[OwningCffiNativeHandle,CffiData]:
        return new_ctype_array(self._ffi, ctype, size, wrap)

    def as_c_double_array(self, data:np.ndarray, shallow:bool=False) -> OwningCffiNativeHandle:
        return as_c_double_array(self._ffi, data, shallow)
    
    def as_c_char_array(self, data:np.ndarray, shallow:bool=False) -> OwningCffiNativeHandle:
        return as_c_char_array(self._ffi, data, shallow)

    def as_native_time_series(self, data:TimeSeriesLike) -> OwningCffiNativeHandle:
        return as_native_time_series(self._ffi, data)
