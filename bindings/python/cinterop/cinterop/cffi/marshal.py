
import numpy as np
from functools import wraps

from typing import Any, Union
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

"""Convert obj to string/unicode if it is a bytes object."""

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

