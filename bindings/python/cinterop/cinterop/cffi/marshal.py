
import numpy as np
from functools import wraps

from typing import Any, List, Union
from cffi import FFI
import six

# This is a Hack. I cannot use FFI.CData in type hints.
CffiData = Any
"""dummy type hint for FFI.CData"""

_c2dtype = dict()
_c2dtype[ 'float *' ] = np.dtype( 'f4' )
_c2dtype[ 'double *' ] = np.dtype( 'f8' )
# _c2dtype[ 'int *' ] = np.dtype( 'i4' ) TBD

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
    res = np.vstack([as_numeric_np_array(ffi, rows[i], size=ncol, shallow=True) for i in range(nrow)])
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

def character_vector_as_string_list(ffi:FFI, ptr:CffiData, size:int) -> List[str]:
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

from datetime import datetime

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

from refcount.interop import OwningCffiNativeHandle

def datetime_to_dtts(ffi:FFI, dt: datetime) -> OwningCffiNativeHandle:
    ptr = ffi.new("date_time_to_second*")
    ptr.year = dt.year
    ptr.month = dt.month
    ptr.day = dt.day
    ptr.hour = dt.hour
    ptr.minute = dt.minute
    ptr.second = dt.second
    return OwningCffiNativeHandle(ptr)

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

    def character_vector_as_string_list(self, ptr:CffiData, size:int) -> List[str]:
        """Convert if possible a cffi pointer to a C data array char** , into a list of python strings.

        Args:
            ptr (CffiData): cffi pointer (FFI.CData)
            size (int): number of character strings in the char** pointer

        Raises:
            RuntimeError: conversion is not supported

        Returns:
            List[str]: converted data
        """
        return character_vector_as_string_list(self._ffi, ptr, size)


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

