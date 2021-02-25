
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

_c2dtype = dict()
_c2dtype[ 'float *' ] = np.dtype( 'f4' )
_c2dtype[ 'double *' ] = np.dtype( 'f8' )
# _c2dtype[ 'int *' ] = np.dtype( 'i4' ) TBD

def new_int_array(ffi, size) -> CffiData:
    return ffi.new('int[%d]' % (size,))

def new_int_scalar_ptr(ffi, value:int) -> CffiData:
    ptr = ffi.new('int*')
    ptr[0] = value
    return ptr

def new_double_array(ffi, size) -> CffiData:
    return ffi.new('double[%d]' % (size,))

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
    ptr.values = as_c_double_array(ffi, list(data.values()))
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
    def __init__(self, start: datetime, time_step_seconds:int, length:int, time_step_code:int):
        self.start = start
        self.time_step_seconds = time_step_seconds
        self.length = length
        self.time_step_code = time_step_code

def time_series_geometry(ffi:FFI, ptr:CffiData) -> TimeSeriesGeometry:
    return TimeSeriesGeometry(
        dtts_as_datetime(ffi, ptr.start),
        ptr.time_step_seconds, 
        ptr.length, 
        ptr.time_step_code)

def as_native_tsgeom(ffi:FFI, tsgeom:TimeSeriesGeometry) -> OwningCffiNativeHandle:
    ptr = ffi.new("regular_time_series_geometry*")
    dtts = datetime_to_dtts(ffi, tsgeom.start)
    ptr.start = dtts.obj
    ptr.time_step_seconds = tsgeom.time_step_seconds 
    ptr.length = tsgeom.length
    ptr.time_step_code = tsgeom.time_step_code
    return OwningCffiNativeHandle(ptr)

ConvertibleToTimestamp = Union[str, datetime, np.datetime64, pd.Timestamp]
"""Definition of a 'type' for type hints. 
"""

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


TIME_DIMNAME="time"
ENSEMBLE_DIMNAME="ensemble"

def as_xarray_time_series(ffi:FFI, ptr:CffiData) -> xr.DataArray:
    ts_geom = time_series_geometry(ffi, ptr.time_series_geometry)
    # npx = two_d_as_np_array_double(ffi, ptr.numeric_data, ts_geom.length, ptr.ensemble_size, True)
    npx = two_d_as_np_array_double(ffi, ptr.numeric_data, ptr.ensemble_size, ts_geom.length, True)
    start = as_timestamp(ts_geom.start)
    if ts_geom.time_step_code > 0:
        raise NotImplementedError("Can only handle conversion of regular time steps, for now")
    delta_t = np.timedelta64(ts_geom.time_step_seconds, 's')
    time_index = [start + delta_t * i for i in range(ts_geom.length)]
    ens_index = [i for i in range(ptr.ensemble_size)]
    x = xr.DataArray(npx, coords=[ens_index, time_index], dims=[ENSEMBLE_DIMNAME, TIME_DIMNAME])
    # x.name = variableIdentifier
    return x

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
    ptr.values = as_c_double_array(ffi, data)
    return OwningCffiNativeHandle(ptr)

def as_c_double_array(ffi, data):
    if isinstance(data, list):
        data = np.asfarray(data)
    elif not isinstance(data, np.ndarray):
        raise TypeError("Conversion to a c array of double requires list of np array as input")
    return ffi.cast("double *", np.ascontiguousarray(data.ctypes.data))

def as_c_char_array(ffi, data):
    if isinstance(data, list):
        data = np.asfarray(data)
    elif not isinstance(data, np.ndarray):
        raise TypeError("Conversion to a c array of double requires list of np array as input")
    return ffi.cast("double *", np.ascontiguousarray(data.ctypes.data))

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

def dtts_as_datetime(ffi:FFI, ptr:CffiData) -> datetime:
    """Convert if possible a cffi pointer to a C data array char** , into a list of python strings.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData)

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        datetime: converted data
    """
    dtts = ptr # ffi.cast('date_time_to_second*', ptr)
    return datetime(dtts.year, dtts.month, dtts.day, dtts.hour, dtts.minute, dtts.second)

def datetime_to_dtts(ffi:FFI, dt: datetime) -> OwningCffiNativeHandle:
    ptr = ffi.new("date_time_to_second*")
    ptr.year = dt.year
    ptr.month = dt.month
    ptr.day = dt.day
    ptr.hour = dt.hour
    ptr.minute = dt.minute
    ptr.second = dt.second
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
        return dtts_as_datetime(self._ffi, ptr)

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

    def as_native_tsgeom(self, tsgeom:TimeSeriesGeometry) -> OwningCffiNativeHandle:
        return as_native_tsgeom(self._ffi, tsgeom)

    def as_xarray_time_series(self, ptr:CffiData) -> xr.DataArray:
        return as_xarray_time_series(self._ffi, ptr)

    


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
