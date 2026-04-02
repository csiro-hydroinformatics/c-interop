# API Reference

## cinterop

c-interop package.

cinterop - helpers for Python-C interop via CFFI

Modules:

- **`cffi`** – Init module. Mostly a legacy from python 2, may be used to expose an API in the future.
- **`timeseries`** – Python representations of multidimensional time series and interop with Python cffi.

## cffi

Init module. Mostly a legacy from python 2, may be used to expose an API in the future.

Modules:

- **`marshal`** – Module to marshal data between Python and C via cffi, with a focus on time series data. This includes functions to convert between native C structs and Python representations, as well as utilities to create and manipulate C arrays from Python data structures.

## marshal

Module to marshal data between Python and C via cffi, with a focus on time series data. This includes functions to convert between native C structs and Python representations, as well as utilities to create and manipulate C arrays from Python data structures.

Classes:

- **`CffiMarshal`** – A helper class for marshalling data to/from a native library module (i.e. DLL).
- **`TimeSeriesGeometry`** – Simplified representation of the temporal geometry of a time series.
- **`TimeSeriesGeometryNative`** – Wrapper around a cdata pointer to a new C struct regular_time_series_geometry.

Functions:

- **`as_arrayof_bytes`** – Convert a list of "strings" to a char\*\* like C array.
- **`as_bytes`** – Convert obj to bytes, if it is a type of string.
- **`as_c_double_array`** – Convert a list or array of numeric values to a cffi pointer to a C array of double precision floats.
- **`as_character_vector`** – Convert a list of "strings" to a character_vector\* native struct.
- **`as_charptr`** – Convert an object to bytes, create as C array of char and copy values to it. Equivalent to char arg[] = "world" if x is the bytes b"world".
- **`as_native_time_series`** – Convert a pure python time series to a native representation via a C struct multi_regular_time_series_data.
- **`as_native_tsgeom`** – Convert a simlified time series geometry to a native representation.
- **`as_np_array_double`** – Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats double[n].
- **`as_numeric_np_array`** – Convert if possible a cffi pointer to a C data array, into a numpy array.
- **`as_string`** – Convert obj to string/unicode if it is a bytes object.
- **`as_xarray_time_series`** – Converts a native time series structure to an xarray representation.
- **`c_charptrptr_as_string_list`** – Convert if possible a cffi pointer to a C data array char\*\* , into a list of python strings.
- **`c_string_as_py_string`** – Convert if possible a cffi pointer to an ANSI C string to a python string.
- **`convert_strings`** – Returns a wrapper that converts any str/unicode object arguments to bytes.
- **`create_values_struct`** – Convert a list or array of numeric values to a cffi pointer to a values_vector struct.
- **`datetime_to_dtts`** – Convert a python datetime to a cffi pointer to a C struct date_time_to_second.
- **`dict_to_named_values`** – Convert a dictionary to a cffi pointer to a named_values_vector struct.
- **`dict_to_string_map`** – Convert a dictionary to a cffi pointer to a string_string_map struct.
- **`dtts_as_datetime`** – Convert if possible a cffi pointer to a C data array char\*\* , into a list of python strings.
- **`geom_to_xarray_time_series`** – Converts an native time series structure to an xarray representation.
- **`get_native_tsgeom`** – Get a native representation of the geometry of a time series. A simple heuristic is used to find the time step.
- **`get_tsgeom`** – Extract a simplified representation of the geometry of a time series. A simple heuristic is used to find the time step.
- **`named_values_to_dict`** – Convert if possible a cffi pointer to a named_values_vector struct, into a dictionary.
- **`new_charptr_array`** – Creates a new C array of pointers to char: char\*[n].
- **`new_ctype_array`** – Creates a new C array of a specified type and size.
- **`new_date_time_to_second`** – Create a new cffi pointer to a C struct date_time_to_second.
- **`new_double_array`** – Creates a new C array of double precision floats double[n].
- **`new_doubleptr_array`** – Creates a new C array of pointers to double precision floats double\*[n].
- **`new_int_array`** – Creates a new C array of integers int[n].
- **`new_int_scalar_ptr`** – Creates a new C array of integers.
- **`string_map_to_dict`** – Convert if possible a cffi pointer to a string_string_map struct, into a dictionary.
- **`two_d_as_np_array_double`** – Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.
- **`two_d_np_array_double_to_native`** – Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.
- **`values_to_nparray`** – Convert if possible a cffi pointer to a values_vector struct, into a python array.

Attributes:

- **`NativePointerLike`** (`TypeAlias`) – types that can represent time series

### NativePointerLike

```
NativePointerLike: TypeAlias = Union[
    OwningCffiNativeHandle, CffiNativeHandle, CffiData
]
```

types that can represent time series

### CffiMarshal

```
CffiMarshal(ffi: FFI)
```

A helper class for marshalling data to/from a native library module (i.e. DLL).

Methods:

- **`as_arrayof_bytes`** – Convert a list of "strings" to a char\*\* like C array.
- **`as_c_double_array`** – Convert a list or array of numeric values to a cffi pointer to a C array of double precision floats.
- **`as_character_vector`** – Convert a list of "strings" to a character_vector\* native struct.
- **`as_charptr`** – Convert an object to bytes, create as C array of char and copy values to it. Equivalent to char arg[] = "world" if x is the bytes b"world".
- **`as_datetime`** – Convert if possible a cffi pointer to a C date_time_to_second struct, into a datetime.
- **`as_native_time_series`** – Convert a pure python time series to a native representation via a C struct multi_regular_time_series_data.
- **`as_native_tsgeom`** – C-compatible representation of a time series geometry.
- **`as_np_array_double`** – Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats double[n].
- **`as_numeric_np_array`** – Convert if possible a cffi pointer to a C data array, into a numpy array.
- **`as_xarray_time_series`** – Convert a native time series structure to an xarray representation.
- **`c_charptrptr_as_string_list`** – Convert if possible a cffi pointer to a C data array char\*\* , into a list of python strings.
- **`c_string_as_py_string`** – Convert if possible a cffi pointer to an ANSI C string to a python string.
- **`character_vector_as_string_list`** – Convert if possible a cffi pointer to a C character_vector , into a list of python strings.
- **`create_values_struct`** – Convert a list or array of numeric values to a cffi pointer to a values_vector struct.
- **`datetime_to_dtts`** – Convert a python datetime to a cffi pointer to a C struct date_time_to_second.
- **`dict_to_named_values`** – Convert a dictionary to a cffi pointer to a named_values_vector struct.
- **`dict_to_string_map`** – Convert a dictionary to a cffi pointer to a string_string_map struct.
- **`get_native_tsgeom`** – Get a native representation of the geometry of a time series. A simple heuristic is used to find the time step.
- **`named_values_to_dict`** – Convert if possible a cffi pointer to a named_values_vector struct, into a dictionary.
- **`new_charptr_array`** – Creates a new C array of pointers to char (strings) char\*[n].
- **`new_ctype_array`** – Creates a new C array of the specified type and size.
- **`new_date_time_to_second`** – Create a new cffi pointer to a C struct date_time_to_second.
- **`new_double_array`** – Creates a new C array of double precision floats double[n].
- **`new_doubleptr_array`** – Creates a new C array of pointers to double precision floats double\*[n].
- **`new_int_array`** – Creates a new C array of integers int[n].
- **`new_int_scalar_ptr`** – Creates a new C array of integers.
- **`new_native_struct`** – Create a new native C struct of the specified type.
- **`new_native_tsgeom`** – Create a new native time series geometry struct.
- **`string_map_to_dict`** – Convert if possible a cffi pointer to a string_string_map struct, into a dictionary.
- **`two_d_as_np_array_double`** – Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.
- **`two_d_np_array_double_to_native`** – Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.
- **`values_to_nparray`** – Convert if possible a cffi pointer to a values_vector struct, into a python array.

Attributes:

- **`nullptr`** (`Any`) – The C NULL pointer.

Source code in `src/cinterop/cffi/marshal.py`

```
def __init__(self, ffi: FFI) -> None:
    """A helper class for marshalling data to/from a native library module (i.e. DLL)."""
    self._ffi: FFI = ffi
```

#### nullptr

```
nullptr: Any
```

The C NULL pointer.

Returns:

- **`Any`** ( `Any` ) – returns FFI.NULL

#### as_arrayof_bytes

```
as_arrayof_bytes(obj: List[Any]) -> OwningCffiNativeHandle
```

Convert a list of "strings" to a char\*\* like C array.

Source code in `src/cinterop/cffi/marshal.py`

```
def as_arrayof_bytes(self, obj: List[Any]) -> OwningCffiNativeHandle:
    """Convert a list of "strings" to a char** like C array."""
    return as_arrayof_bytes(self._ffi, obj)
```

#### as_c_double_array

```
as_c_double_array(
    data: ndarray, shallow: bool = False
) -> OwningCffiNativeHandle
```

Convert a list or array of numeric values to a cffi pointer to a C array of double precision floats.

Parameters:

- **`data`** (`Union[List[float], ndarray]`) – list or array of numeric values
- **`shallow`** (`bool`, default: `False` ) – If True the resulting C array points directly to the data in the input numpy array (if it is a numpy array), otherwise a new C array is created and the data is copied to it. Defaults to False. Note that if the input data is a list, it will be converted to a numpy array and the resulting C array will not be shallow.

Returns:

- **`OwningCffiNativeHandle`** ( `OwningCffiNativeHandle` ) – A wrapper that owns the memory allocated for the resulting C array of double precision floats.

Source code in `src/cinterop/cffi/marshal.py`

```
def as_c_double_array(
    self,
    data: np.ndarray,
    shallow: bool = False,  # noqa: FBT001, FBT002
) -> OwningCffiNativeHandle:
    """Convert a list or array of numeric values to a cffi pointer to a C array of double precision floats.

    Args:
        data (Union[List[float], np.ndarray]): list or array of numeric values
        shallow (bool, optional): If True the resulting C array points directly to the data in the input numpy array (if it is a numpy array),
            otherwise a new C array is created and the data is copied to it. Defaults to False.
            Note that if the input data is a list, it will be converted to a numpy array and the resulting C array will not be shallow.

    Returns:
        OwningCffiNativeHandle: A wrapper that owns the memory allocated for the resulting C array of double precision floats.
    """
    return as_c_double_array(self._ffi, data, shallow)
```

#### as_character_vector

```
as_character_vector(
    obj: List[Any],
) -> OwningCffiNativeHandle
```

Convert a list of "strings" to a character_vector\* native struct.

Source code in `src/cinterop/cffi/marshal.py`

```
def as_character_vector(self, obj: List[Any]) -> OwningCffiNativeHandle:
    """Convert a list of "strings" to a character_vector* native struct."""
    return as_character_vector(self._ffi, obj)
```

#### as_charptr

```
as_charptr(x: str, wrap: bool = False) -> CffiData
```

Convert an object to `bytes`, create as C array of char and copy values to it. Equivalent to `char arg[] = "world"` if x is the bytes b"world".

Parameters:

- **`x`** (`str`) – a string-like object; bytes or str, or string like object that can be encoded to bytes (six.string_like)
- **`wrap`** (`bool`, default: `False` ) – return a "naked" cdata pointer object if False, or wrapped in a OwningCffiNativeHandle if True. Defaults to False.

Returns:

- `CffiData` – Union\[OwningCffiNativeHandle,CffiData\]: a (wrapper to a) cdata pointer object owning a new array of char \*s of length size

Source code in `src/cinterop/cffi/marshal.py`

```
def as_charptr(self, x: str, wrap: bool = False) -> CffiData:  # noqa: FBT001, FBT002
    """Convert an object to `bytes`, create as C array of char and copy values to it. Equivalent to `char arg[] = "world"` if x is the bytes b"world".

    Args:
        x (str): a string-like object; bytes or str, or string like object that can be encoded to bytes (six.string_like)
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of `char *`s of length `size`
    """
    return as_charptr(self._ffi, x, wrap)
```

#### as_datetime

```
as_datetime(ptr: CffiData) -> datetime
```

Convert if possible a cffi pointer to a C date_time_to_second struct, into a datetime.

Parameters:

- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData)

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- **`datetime`** ( `datetime` ) – converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def as_datetime(self, ptr: CffiData) -> datetime:
    """Convert if possible a cffi pointer to a C date_time_to_second struct, into a datetime.

    Args:
        ptr (CffiData): cffi pointer (FFI.CData)

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        datetime: converted data
    """
    return dtts_as_datetime(ptr)
```

#### as_native_time_series

```
as_native_time_series(
    data: TimeSeriesLike,
) -> OwningCffiNativeHandle
```

Convert a pure python time series to a native representation via a C struct `multi_regular_time_series_data`.

Parameters:

- **`data`** (`TimeSeriesLike`) – xarray or pandas based time series

Raises:

- `TypeError` – unexpected input type

Returns:

- **`OwningCffiNativeHandle`** ( `OwningCffiNativeHandle` ) – wrapper to a C struct multi_regular_time_series_data

Source code in `src/cinterop/cffi/marshal.py`

```
def as_native_time_series(self, data: TimeSeriesLike) -> OwningCffiNativeHandle:
    """Convert a pure python time series to a native representation via a C struct `multi_regular_time_series_data`.

    Args:
        data (TimeSeriesLike): xarray or pandas based time series

    Raises:
        TypeError: unexpected input type

    Returns:
        OwningCffiNativeHandle: wrapper to a C struct `multi_regular_time_series_data`
    """
    return as_native_time_series(self._ffi, data)
```

#### as_native_tsgeom

```
as_native_tsgeom(
    tsgeom: TimeSeriesGeometry,
) -> TimeSeriesGeometryNative
```

C-compatible representation of a time series geometry.

Returns:

- **`TimeSeriesGeometryNative`** ( `TimeSeriesGeometryNative` ) – wrapper around a cdata pointer to a new C struct regular_time_series_geometry

Source code in `src/cinterop/cffi/marshal.py`

```
def as_native_tsgeom(self, tsgeom: TimeSeriesGeometry) -> TimeSeriesGeometryNative:
    """C-compatible representation of a time series geometry.

    Returns:
        TimeSeriesGeometryNative: wrapper around a cdata pointer to a new C struct `regular_time_series_geometry`
    """
    return tsgeom.as_native(self._ffi)
```

#### as_np_array_double

```
as_np_array_double(
    ptr: CffiData, size: int, shallow: bool = False
) -> ndarray
```

Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats `double[n]`.

The returned numpy array may be directly pointing to the original data (faster performance), or a deep copy (memory safety - "normal" numpy array)

Parameters:

- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData)
- **`size`** (`int`) – array size
- **`shallow`** (`bool`, default: `False` ) – If True the resulting numpy array points directly to the native data array. Otherwise, return a numpy array with a deep copy of the data, managed by Python. Defaults to False.

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `ndarray` – np.ndarray: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def as_np_array_double(
    self,
    ptr: CffiData,
    size: int,
    shallow: bool = False,  # noqa: FBT001, FBT002
) -> np.ndarray:
    """Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats `double[n]`.

    The returned numpy array may be directly pointing to the original data (faster performance), or a deep copy (memory safety - "normal" numpy array)

    Args:
        ptr (CffiData): cffi pointer (FFI.CData)
        size (int): array size
        shallow (bool): If True the resulting numpy array points directly to the native data array. Otherwise, return a numpy array with a deep copy of the data, managed by Python. Defaults to False.

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        np.ndarray: converted data
    """
    return as_np_array_double(self._ffi, ptr, size, shallow)
```

#### as_numeric_np_array

```
as_numeric_np_array(
    ptr: CffiData, size: int, shallow: bool = False
) -> ndarray
```

Convert if possible a cffi pointer to a C data array, into a numpy array.

Parameters:

- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData)
- **`size`** (`int`) – array size
- **`shallow`** (`bool`, default: `False` ) – If true the array points directly to native data array. Defaults to False.

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `ndarray` – np.ndarray: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def as_numeric_np_array(
    self,
    ptr: CffiData,
    size: int,
    shallow: bool = False,  # noqa: FBT001, FBT002
) -> np.ndarray:
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
```

#### as_xarray_time_series

```
as_xarray_time_series(ptr: CffiData) -> Optional[DataArray]
```

Convert a native time series structure to an xarray representation.

Source code in `src/cinterop/cffi/marshal.py`

```
def as_xarray_time_series(self, ptr: CffiData) -> Optional[xr.DataArray]:
    """Convert a native time series structure to an xarray representation."""
    return as_xarray_time_series(self._ffi, ptr)
```

#### c_charptrptr_as_string_list

```
c_charptrptr_as_string_list(
    ptr: CffiData, size: int
) -> List[str]
```

Convert if possible a cffi pointer to a C data array char\*\* , into a list of python strings.

Parameters:

- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData)
- **`size`** (`int`) – number of character strings in the char\*\* pointer

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `List[str]` – List\[str\]: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def c_charptrptr_as_string_list(self, ptr: CffiData, size: int) -> List[str]:
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
```

#### c_string_as_py_string

```
c_string_as_py_string(ptr: CffiData) -> str
```

Convert if possible a cffi pointer to an ANSI C string to a python string.

Parameters:

- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData)

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- **`str`** ( `str` ) – converted string

Source code in `src/cinterop/cffi/marshal.py`

```
def c_string_as_py_string(self, ptr: CffiData) -> str:
    """Convert if possible a cffi pointer to an ANSI C string <char*> to a python string.

    Args:
        ptr (CffiData): cffi pointer (FFI.CData)

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        str: converted string
    """
    return c_string_as_py_string(self._ffi, ptr)
```

#### character_vector_as_string_list

```
character_vector_as_string_list(ptr: CffiData) -> List[str]
```

Convert if possible a cffi pointer to a C character_vector , into a list of python strings.

Parameters:

- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData)

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `List[str]` – List\[str\]: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def character_vector_as_string_list(self, ptr: CffiData) -> List[str]:
    """Convert if possible a cffi pointer to a C character_vector , into a list of python strings.

    Args:
        ptr (CffiData): cffi pointer (FFI.CData)

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        List[str]: converted data
    """
    return self.c_charptrptr_as_string_list(ptr.values, ptr.size)
```

#### create_values_struct

```
create_values_struct(
    data: Union[List[float], ndarray],
) -> OwningCffiNativeHandle
```

Convert a list or array of numeric values to a cffi pointer to a `values_vector` struct.

Source code in `src/cinterop/cffi/marshal.py`

```
def create_values_struct(
    self,
    data: Union[List[float], np.ndarray],
) -> OwningCffiNativeHandle:
    """Convert a list or array of numeric values to a cffi pointer to a `values_vector` struct."""
    return create_values_struct(self._ffi, data)
```

#### datetime_to_dtts

```
datetime_to_dtts(dt: datetime) -> OwningCffiNativeHandle
```

Convert a python datetime to a cffi pointer to a C struct `date_time_to_second`.

Source code in `src/cinterop/cffi/marshal.py`

```
def datetime_to_dtts(self, dt: datetime) -> OwningCffiNativeHandle:
    """Convert a python datetime to a cffi pointer to a C struct `date_time_to_second`."""
    return datetime_to_dtts(self._ffi, dt)
```

#### dict_to_named_values

```
dict_to_named_values(
    data: Dict[str, float],
) -> OwningCffiNativeHandle
```

Convert a dictionary to a cffi pointer to a `named_values_vector` struct.

Parameters:

- **`data`** (`Dict[str, float]`) – mapping from keys to numeric values

Returns:

- **`OwningCffiNativeHandle`** ( `OwningCffiNativeHandle` ) – A wrapper that owns the memory allocated for the resulting named_values_vector pointed to

Source code in `src/cinterop/cffi/marshal.py`

```
def dict_to_named_values(self, data: Dict[str, float]) -> OwningCffiNativeHandle:
    """Convert a dictionary to a cffi pointer to a `named_values_vector` struct.

    Args:
        data (Dict[str,float]): mapping from keys to numeric values

    Returns:
        OwningCffiNativeHandle: A wrapper that owns the memory allocated for the resulting `named_values_vector` pointed to
    """
    return dict_to_named_values(self._ffi, data)
```

#### dict_to_string_map

```
dict_to_string_map(
    data: Dict[str, str],
) -> OwningCffiNativeHandle
```

Convert a dictionary to a cffi pointer to a `string_string_map` struct.

Source code in `src/cinterop/cffi/marshal.py`

```
def dict_to_string_map(self, data: Dict[str, str]) -> OwningCffiNativeHandle:
    """Convert a dictionary to a cffi pointer to a `string_string_map` struct."""
    return dict_to_string_map(self._ffi, data)
```

#### get_native_tsgeom

```
get_native_tsgeom(
    pd_series: Series,
) -> OwningCffiNativeHandle
```

Get a native representation of the geometry of a time series. A simple heuristic is used to find the time step.

Source code in `src/cinterop/cffi/marshal.py`

```
def get_native_tsgeom(self, pd_series: pd.Series) -> OwningCffiNativeHandle:
    """Get a native representation of the geometry of a time series. A simple heuristic is used to find the time step."""
    return get_native_tsgeom(self._ffi, pd_series)
```

#### named_values_to_dict

```
named_values_to_dict(ptr: CffiData) -> Dict[str, float]
```

Convert if possible a cffi pointer to a `named_values_vector` struct, into a dictionary.

Parameters:

- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData) to a named_values_vector struct

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `Dict[str, float]` – Dict\[str,float\]: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def named_values_to_dict(self, ptr: CffiData) -> Dict[str, float]:
    """Convert if possible a cffi pointer to a `named_values_vector` struct, into a dictionary.

    Args:
        ptr (CffiData): cffi pointer (FFI.CData) to a `named_values_vector` struct

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        Dict[str,float]: converted data
    """
    return named_values_to_dict(self._ffi, ptr)
```

#### new_charptr_array

```
new_charptr_array(
    size: int, wrap: bool = False
) -> Union[OwningCffiNativeHandle, CffiData]
```

Creates a new C array of pointers to char (strings) `char*[n]`.

Parameters:

- **`size`** (`int`) – array size
- **`wrap`** (`bool`, default: `False` ) – return a "naked" cdata pointer object if False, or wrapped in a OwningCffiNativeHandle if True. Defaults to False.

Returns:

- `Union[OwningCffiNativeHandle, CffiData]` – Union\[OwningCffiNativeHandle,CffiData\]: a (wrapper to a) cdata pointer object owning a new array of pointers to char (strings) of length size

Source code in `src/cinterop/cffi/marshal.py`

```
def new_charptr_array(
    self,
    size: int,
    wrap: bool = False,  # noqa: FBT001, FBT002
) -> Union[OwningCffiNativeHandle, CffiData]:
    """Creates a new C array of pointers to char (strings) `char*[n]`.

    Args:
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of pointers to char (strings) of length `size`
    """
    return new_charptr_array(self._ffi, size, wrap)
```

#### new_ctype_array

```
new_ctype_array(
    ctype: str, size: int, wrap: bool = False
) -> Union[OwningCffiNativeHandle, CffiData]
```

Creates a new C array of the specified type and size.

Parameters:

- **`ctype`** (`str`) – C type of the array elements, e.g. "int", "double", "char\*"
- **`size`** (`int`) – array size
- **`wrap`** (`bool`, default: `False` ) – return a "naked" cdata pointer object if False, or wrapped in a OwningCffiNativeHandle if True. Defaults to False.

Returns:

- `Union[OwningCffiNativeHandle, CffiData]` – Union\[OwningCffiNativeHandle,CffiData\]: a (wrapper to a) cdata pointer object owning a new array of the specified type and length size

Source code in `src/cinterop/cffi/marshal.py`

```
def new_ctype_array(
    self,
    ctype: str,
    size: int,
    wrap: bool = False,  # noqa: FBT001, FBT002
) -> Union[OwningCffiNativeHandle, CffiData]:
    """Creates a new C array of the specified type and size.

    Args:
        ctype (str): C type of the array elements, e.g. "int", "double", "char*"
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of the specified type and length `size`
    """
    return new_ctype_array(self._ffi, ctype, size, wrap)
```

#### new_date_time_to_second

```
new_date_time_to_second() -> OwningCffiNativeHandle
```

Create a new cffi pointer to a C struct `date_time_to_second`.

Source code in `src/cinterop/cffi/marshal.py`

```
def new_date_time_to_second(self) -> OwningCffiNativeHandle:
    """Create a new cffi pointer to a C struct `date_time_to_second`."""
    return new_date_time_to_second(self._ffi)
```

#### new_double_array

```
new_double_array(
    size: int, wrap: bool = False
) -> Union[OwningCffiNativeHandle, CffiData]
```

Creates a new C array of double precision floats `double[n]`.

Parameters:

- **`size`** (`int`) – array size
- **`wrap`** (`bool`, default: `False` ) – return a "naked" cdata pointer object if False, or wrapped in a OwningCffiNativeHandle if True. Defaults to False.

Returns:

- `Union[OwningCffiNativeHandle, CffiData]` – Union\[OwningCffiNativeHandle,CffiData\]: a (wrapper to a) cdata pointer object owning a new array of double precision floats of length size

Source code in `src/cinterop/cffi/marshal.py`

```
def new_double_array(
    self,
    size: int,
    wrap: bool = False,  # noqa: FBT001, FBT002
) -> Union[OwningCffiNativeHandle, CffiData]:
    """Creates a new C array of double precision floats `double[n]`.

    Args:
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of double precision floats of length `size`
    """
    return new_double_array(self._ffi, size, wrap)
```

#### new_doubleptr_array

```
new_doubleptr_array(
    size: int, wrap: bool = False
) -> Union[OwningCffiNativeHandle, CffiData]
```

Creates a new C array of pointers to double precision floats `double*[n]`.

Parameters:

- **`size`** (`int`) – array size
- **`wrap`** (`bool`, default: `False` ) – return a "naked" cdata pointer object if False, or wrapped in a OwningCffiNativeHandle if True. Defaults to False.

Returns:

- `Union[OwningCffiNativeHandle, CffiData]` – Union\[OwningCffiNativeHandle,CffiData\]: a (wrapper to a) cdata pointer object owning a new array of pointers to double precision floats of length size

Source code in `src/cinterop/cffi/marshal.py`

```
def new_doubleptr_array(
    self,
    size: int,
    wrap: bool = False,  # noqa: FBT001, FBT002
) -> Union[OwningCffiNativeHandle, CffiData]:
    """Creates a new C array of pointers to double precision floats `double*[n]`.

    Args:
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of pointers to double precision floats of length `size`
    """
    return new_doubleptr_array(self._ffi, size, wrap)
```

#### new_int_array

```
new_int_array(
    size: int, wrap: bool = False
) -> Union[OwningCffiNativeHandle, CffiData]
```

Creates a new C array of integers `int[n]`.

Parameters:

- **`size`** (`int`) – array size
- **`wrap`** (`bool`, default: `False` ) – return a "naked" cdata pointer object if False, or wrapped in a OwningCffiNativeHandle if True. Defaults to False.

Returns:

- `Union[OwningCffiNativeHandle, CffiData]` – Union\[OwningCffiNativeHandle,CffiData\]: a (wrapper to a) cdata pointer object owning a new array of integers of length size

Source code in `src/cinterop/cffi/marshal.py`

```
def new_int_array(
    self,
    size: int,
    wrap: bool = False,  # noqa: FBT001, FBT002
) -> Union[OwningCffiNativeHandle, CffiData]:
    """Creates a new C array of integers `int[n]`.

    Args:
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of integers of length `size`
    """
    return new_int_array(self._ffi, size, wrap)
```

#### new_int_scalar_ptr

```
new_int_scalar_ptr(value: int = 0) -> CffiData
```

Creates a new C array of integers.

Parameters:

- **`value`** (`int`, default: `0` ) – description. Defaults to 0.

Returns:

- **`CffiData`** ( `CffiData` ) – a cdata pointer object owning a new pointer to a single integer valued as specified.

Source code in `src/cinterop/cffi/marshal.py`

```
def new_int_scalar_ptr(self, value: int = 0) -> "CffiData":
    """Creates a new C array of integers.

    Args:
        value (int, optional): _description_. Defaults to 0.

    Returns:
        CffiData: a cdata pointer object owning a new pointer to a single integer valued as specified.
    """
    return new_int_scalar_ptr(self._ffi, value)
```

#### new_native_struct

```
new_native_struct(
    type_of_struct: str,
) -> OwningCffiNativeHandle
```

Create a new native C struct of the specified type.

Source code in `src/cinterop/cffi/marshal.py`

```
def new_native_struct(self, type_of_struct: str) -> OwningCffiNativeHandle:
    """Create a new native C struct of the specified type."""
    return OwningCffiNativeHandle(self._ffi.new(type_of_struct), type_of_struct)
```

#### new_native_tsgeom

```
new_native_tsgeom() -> TimeSeriesGeometryNative
```

Create a new native time series geometry struct.

Source code in `src/cinterop/cffi/marshal.py`

```
def new_native_tsgeom(self) -> TimeSeriesGeometryNative:
    """Create a new native time series geometry struct."""
    return TimeSeriesGeometryNative(self._ffi)
```

#### string_map_to_dict

```
string_map_to_dict(ptr: CffiData) -> Dict[str, str]
```

Convert if possible a cffi pointer to a `string_string_map` struct, into a dictionary.

Parameters:

- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData) to a string_string_map struct

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `Dict[str, str]` – Dict\[str,str\]: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def string_map_to_dict(self, ptr: CffiData) -> Dict[str, str]:
    """Convert if possible a cffi pointer to a `string_string_map` struct, into a dictionary.

    Args:
        ptr (CffiData): cffi pointer (FFI.CData) to a `string_string_map` struct

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        Dict[str,str]: converted data
    """
    return string_map_to_dict(self._ffi, ptr)
```

#### two_d_as_np_array_double

```
two_d_as_np_array_double(
    ptr: CffiData, nrow: int, ncol: int
) -> ndarray
```

Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.

Parameters:

- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData)
- **`nrow`** (`int`) – number of rows
- **`ncol`** (`int`) – number of columns

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `ndarray` – np.ndarray: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def two_d_as_np_array_double(
    self,
    ptr: CffiData,
    nrow: int,
    ncol: int,
) -> np.ndarray:
    """Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.

    Args:
        ptr (CffiData): cffi pointer (FFI.CData)
        nrow (int): number of rows
        ncol (int): number of columns

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        np.ndarray: converted data
    """
    return two_d_as_np_array_double(self._ffi, ptr, nrow, ncol)
```

#### two_d_np_array_double_to_native

```
two_d_np_array_double_to_native(
    data: ndarray,
) -> OwningCffiNativeHandle
```

Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.

Parameters:

- **`data`** (`ndarray`) – data

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- **`OwningCffiNativeHandle`** ( `OwningCffiNativeHandle` ) – wrapper to a C array of pointers to double precision floats of length nrow

Source code in `src/cinterop/cffi/marshal.py`

```
def two_d_np_array_double_to_native(
    self,
    data: np.ndarray,
) -> OwningCffiNativeHandle:
    """Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.

    Args:
        data (np.ndarray): data

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        OwningCffiNativeHandle: wrapper to a C array of pointers to double precision floats of length `nrow`
    """
    return two_d_np_array_double_to_native(self._ffi, data)
```

#### values_to_nparray

```
values_to_nparray(ptr: CffiData) -> ndarray
```

Convert if possible a cffi pointer to a `values_vector` struct, into a python array.

Parameters:

- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData) to a values_vector struct

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `ndarray` – Dict\[str,float\]: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def values_to_nparray(self, ptr: CffiData) -> np.ndarray:
    """Convert if possible a cffi pointer to a `values_vector` struct, into a python array.

    Args:
        ptr (CffiData): cffi pointer (FFI.CData) to a `values_vector` struct

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        Dict[str,float]: converted data
    """
    return values_to_nparray(self._ffi, ptr)
```

### TimeSeriesGeometry

```
TimeSeriesGeometry(
    start: ConvertibleToTimestamp = None,
    time_step_seconds: int = 3600,
    length: int = 1,
    time_step_code: int = 0,
)
```

Simplified representation of the temporal geometry of a time series.

Suitable for interop with the C struct `regular_time_series_geometry`

Suitable for interop with the C struct `regular_time_series_geometry`

Parameters:

- **`start`** (`ConvertibleToTimestamp`, default: `None` ) – Start date of a time series. Defaults to None.
- **`time_step_seconds`** (`int`, default: `3600` ) – time step length in seconds, used if this is a regular time step. Defaults to 3600.
- **`length`** (`int`, default: `1` ) – number of items in the time series. Defaults to 1.
- **`time_step_code`** (`int`, default: `0` ) – type of time step: 0 for even time steps, or 1 for monthly, in which case time_step_seconds is overriden. Defaults to 0.

Methods:

- **`as_native`** – C-compatible representation of a time series geometry.
- **`from_native`** – Create a simplified time series geometry from a native representation.

Source code in `src/cinterop/cffi/marshal.py`

```
def __init__(
    self,
    start: ConvertibleToTimestamp = None,
    time_step_seconds: int = 3600,
    length: int = 1,
    time_step_code: int = 0,
):
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
```

#### as_native

```
as_native(ffi: FFI) -> TimeSeriesGeometryNative
```

C-compatible representation of a time series geometry.

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory

Returns:

- **`TimeSeriesGeometryNative`** ( `TimeSeriesGeometryNative` ) – wrapper around a cdata pointer to a new C struct regular_time_series_geometry

Source code in `src/cinterop/cffi/marshal.py`

```
def as_native(self, ffi: FFI) -> "TimeSeriesGeometryNative":
    """C-compatible representation of a time series geometry.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory

    Returns:
        TimeSeriesGeometryNative: wrapper around a cdata pointer to a new C struct `regular_time_series_geometry`
    """
    return TimeSeriesGeometryNative(
        ffi,
        self.start,
        self.time_step_seconds,
        self.length,
        self.time_step_code,
    )
```

#### from_native

```
from_native(
    ts_geom: TimeSeriesGeometryNative,
) -> TimeSeriesGeometry
```

Create a simplified time series geometry from a native representation.

Source code in `src/cinterop/cffi/marshal.py`

```
@staticmethod
def from_native(ts_geom: "TimeSeriesGeometryNative") -> "TimeSeriesGeometry":
    """Create a simplified time series geometry from a native representation."""
    return TimeSeriesGeometry(
        ts_geom.start,
        ts_geom.time_step_seconds,
        ts_geom.length,
        ts_geom.time_step_code,
    )
```

### TimeSeriesGeometryNative

```
TimeSeriesGeometryNative(
    ffi: Union[FFI, CffiData],
    start: ConvertibleToTimestamp = None,
    time_step_seconds: int = 3600,
    length: int = 1,
    time_step_code: int = 0,
)
```

Bases: `OwningCffiNativeHandle`

Wrapper around a cdata pointer to a new C struct `regular_time_series_geometry`.

Parameters:

- **`ffi`** (`Union[FFI, CffiData]`) – FFI instance, or a preexisting cdata pointer to a regular_time_series_geometry struct
- **`start`** (`ConvertibleToTimestamp`, default: `None` ) – Start date of a time series. Defaults to None.
- **`time_step_seconds`** (`int`, default: `3600` ) – time step length in seconds, used if this is a regular time step. Defaults to 3600.
- **`length`** (`int`, default: `1` ) – number of items in the time series. Defaults to 1.
- **`time_step_code`** (`int`, default: `0` ) – type of time step: 0 for even time steps, or 1 for monthly, in which case time_step_seconds is overriden. Defaults to 0.

Methods:

- **`time_index`** – Get the time index corresponding to this time series geometry.

Attributes:

- **`length`** (`int`) – Number of items in the time series.
- **`start`** (`datetime`) – Start date of the time series.
- **`time_step_code`** (`int`) – Type of time step: 0 for even time steps, or 1 for monthly, in which case time_step_seconds is overriden.
- **`time_step_seconds`** (`int`) – Time step length in seconds, used if this is a regular time step.

Source code in `src/cinterop/cffi/marshal.py`

```
def __init__(
    self,
    ffi: Union[FFI, CffiData],
    start: ConvertibleToTimestamp = None,
    time_step_seconds: int = 3600,
    length: int = 1,
    time_step_code: int = 0,
):
    """Wrapper around a cdata pointer to a new C struct `regular_time_series_geometry`.

    Args:
        ffi (Union[FFI, CffiData]): FFI instance, or a preexisting cdata pointer to a `regular_time_series_geometry` struct
        start (ConvertibleToTimestamp, optional): Start date of a time series. Defaults to None.
        time_step_seconds (int, optional): time step length in seconds, used if this is a regular time step. Defaults to 3600.
        length (int, optional): number of items in the time series. Defaults to 1.
        time_step_code (int, optional): type of time step: 0 for even time steps, or 1 for monthly, in which case `time_step_seconds` is overriden. Defaults to 0.
    """
    if isinstance(ffi, FFI.CData):  # HACK? rethink
        super(TimeSeriesGeometryNative, self).__init__(  # noqa: UP008
            ffi,
            "regular_time_series_geometry*",
            0,
        )
    else:
        ptr = ffi.new("regular_time_series_geometry*")
        super(TimeSeriesGeometryNative, self).__init__(  # noqa: UP008
            ptr,
            "regular_time_series_geometry*",
            0,
        )
        self.start = start if start is not None else as_pydatetime("1970-01-01")
        self.time_step_seconds = time_step_seconds
        self.length = length
        self.time_step_code = time_step_code
```

#### length

```
length: int
```

Number of items in the time series.

#### start

```
start: datetime
```

Start date of the time series.

#### time_step_code

```
time_step_code: int
```

Type of time step: 0 for even time steps, or 1 for monthly, in which case `time_step_seconds` is overriden.

#### time_step_seconds

```
time_step_seconds: int
```

Time step length in seconds, used if this is a regular time step.

#### time_index

```
time_index() -> Union[List, DatetimeIndex]
```

Get the time index corresponding to this time series geometry.

Source code in `src/cinterop/cffi/marshal.py`

```
def time_index(self) -> Union[List, pd.DatetimeIndex]:
    """Get the time index corresponding to this time series geometry."""
    return _ts_geom_to_time_index(self)
```

### as_arrayof_bytes

```
as_arrayof_bytes(
    ffi: FFI, obj: List[Any]
) -> OwningCffiNativeHandle
```

Convert a list of "strings" to a char\*\* like C array.

Parameters:

- **`obj`** (`List`) – list of objects (strings) to convert

Returns:

- **`List`** ( `OwningCffiNativeHandle` ) – objects converted to bytes if it was a type of string

Source code in `src/cinterop/cffi/marshal.py`

```
def as_arrayof_bytes(ffi: FFI, obj: List[Any]) -> OwningCffiNativeHandle:
    """Convert a list of "strings" to a char** like C array.

    Args:
        obj (List): list of objects (strings) to convert

    Returns:
        List: objects converted to bytes if it was a type of string
    """
    ptr: CffiData = new_charptr_array(ffi, len(obj), wrap=False)
    items = [ffi.new("char[]", as_bytes(obj[i])) for i in range(len(obj))]
    for i in range(len(obj)):
        ptr[i] = items[i]
    result = OwningCffiNativeHandle(ptr)
    result.keepalive = items # type: ignore[attr-defined]
    return result
```

### as_bytes

```
as_bytes(obj: Any) -> Union[bytes, Any]
```

Convert obj to bytes, if it is a type of string.

This function is mostly a legacy for python2/3 compatibility, though python 2 in practice is probably not supported anymore by the package. In python3, it converts str to bytes, and leaves bytes unchanged. In python2, it converts unicode to bytes, and leaves str unchanged.

Parameters:

- **`obj`** (`Any`) – object to convert

Returns:

- `Union[bytes, Any]` – Union\[bytes, Any\]: object converted to bytes if it was a type of string. If unknown type, returns the object unchanged.

Source code in `src/cinterop/cffi/marshal.py`

```
def as_bytes(obj: Any) -> Union[bytes, Any]:
    """Convert obj to bytes, if it is a type of string.

    This function is mostly a legacy for python2/3 compatibility, though python 2 in practice is probably not supported anymore by the package.
    In python3, it converts str to bytes, and leaves bytes unchanged.
    In python2, it converts unicode to bytes, and leaves str unchanged.

    Args:
        obj (Any): object to convert

    Returns:
        Union[bytes, Any]: object converted to bytes if it was a type of string. If unknown type, returns the object unchanged.
    """
    if isinstance(obj, bytes):
        return obj
    if isinstance(obj, six.string_types):
        return obj.encode("utf-8")
    return obj
```

### as_c_double_array

```
as_c_double_array(
    ffi: FFI,
    data: Union[List[float], ndarray],
    shallow: bool = False,
) -> OwningCffiNativeHandle
```

Convert a list or array of numeric values to a cffi pointer to a C array of double precision floats.

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory
- **`data`** (`Union[List[float], ndarray]`) – list or array of numeric values
- **`shallow`** (`bool`, default: `False` ) – If True the resulting C array points directly to the data in the input numpy array (if it is a numpy array), otherwise a new C array is created and the data is copied to it. Defaults to False. Note that if the input data is a list, it will be converted to a numpy array and the resulting C array will not be shallow.

Raises:

- `RuntimeError` – conversion is not supported

Returns: OwningCffiNativeHandle: A wrapper that owns the memory allocated for the resulting C array of double precision floats.

Source code in `src/cinterop/cffi/marshal.py`

```
def as_c_double_array(
    ffi: FFI,
    data: Union[List[float], np.ndarray],
    shallow: bool = False,  # noqa: FBT001, FBT002
) -> OwningCffiNativeHandle:
    """Convert a list or array of numeric values to a cffi pointer to a C array of double precision floats.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        data (Union[List[float], np.ndarray]): list or array of numeric values
        shallow (bool, optional): If True the resulting C array points directly to the data in the input numpy array (if it is a numpy array),
            otherwise a new C array is created and the data is copied to it. Defaults to False.
            Note that if the input data is a list, it will be converted to a numpy array and the resulting C array will not be shallow.

    Raises:
        RuntimeError: conversion is not supported
    Returns:
        OwningCffiNativeHandle: A wrapper that owns the memory allocated for the resulting C array of double precision floats.
    """
    if isinstance(data, list):
        # Nov 2024 adapt to numpy 2.0 breaking changes
        # https://jira.csiro.au/browse/WIRADA-704
        data = np.asarray(data, dtype=float)
        shallow = False
    elif isinstance(data, xr.DataArray):
        data = data.values
        # shallow = False # really needed??
    elif not isinstance(data, np.ndarray):
        raise TypeError(
            "Conversion to a c array of double requires list or np array as input",
        )
    if len(data.shape) > 1:
        data = data.squeeze()
        shallow = False
        if len(data.shape) > 1:
            raise TypeError(
                "Conversion to a double* array: input data must be of dimension one, and the python array cannot be squeezed to dimension one",
            )
    # Nov 2024 adapt to numpy 2.0 breaking changes
    # https://jira.csiro.au/browse/WIRADA-704
    # `np.float_` was removed in the NumPy 2.0 release
    # https://numpy.org/devdocs/release/1.20.0-notes.html#deprecations
    if data.dtype not in (np.float64, float, np.double):
        # TODO: is this wise to override the shallow parameter
        shallow = False
        data = data.astype(np.float64)
    if shallow and data.flags["C_CONTIGUOUS"]:
        native_d = ffi.cast("double *", data.ctypes.data)
    else:
        native_d = new_double_array(ffi, data.shape[0])
        data_c = np.ascontiguousarray(data) if not data.flags["C_CONTIGUOUS"] else data
        ffi.buffer(native_d)[:] = data_c
    return OwningCffiNativeHandle(native_d)
```

### as_character_vector

```
as_character_vector(
    ffi: FFI, obj: List[Any]
) -> OwningCffiNativeHandle
```

Convert a list of "strings" to a character_vector\* native struct.

Source code in `src/cinterop/cffi/marshal.py`

```
def as_character_vector(ffi: FFI, obj: List[Any]) -> OwningCffiNativeHandle:
    """Convert a list of "strings" to a character_vector* native struct."""
    cv = ffi.new("character_vector*")
    cv.size = len(obj)
    names = as_arrayof_bytes(ffi, obj)
    cv.values = names.ptr
    result = OwningCffiNativeHandle(cv)
    result.keepalive = names # type: ignore[attr-defined]
    return result
```

### as_charptr

```
as_charptr(
    ffi: FFI, x: str, wrap: bool = False
) -> Union[OwningCffiNativeHandle, CffiData]
```

Convert an object to `bytes`, create as C array of char and copy values to it. Equivalent to `char arg[] = "world"` if x is the bytes b"world".

Parameters:

- **`ffi`** (`FFI`) – ffi object to the native library accessed
- **`x`** (`str`) – a string-like object; bytes or str, or string like object that can be encoded to bytes (six.string_like)
- **`wrap`** (`bool`, default: `False` ) – return a "naked" cdata pointer object if False, or wrapped in a OwningCffiNativeHandle if True. Defaults to False.

Returns:

- `Union[OwningCffiNativeHandle, CffiData]` – Union\[OwningCffiNativeHandle,CffiData\]: a (wrapper to a) cdata pointer object owning a new array of char \*s of length size

Source code in `src/cinterop/cffi/marshal.py`

```
def as_charptr(
    ffi: FFI,
    x: str,
    wrap: bool = False,  # noqa: FBT001, FBT002
) -> Union[OwningCffiNativeHandle, CffiData]:
    """Convert an object to `bytes`, create as C array of char and copy values to it. Equivalent to `char arg[] = "world"` if x is the bytes b"world".

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
    return x
```

### as_native_time_series

```
as_native_time_series(
    ffi: FFI, data: TimeSeriesLike
) -> OwningCffiNativeHandle
```

Convert a pure python time series to a native representation via a C struct `multi_regular_time_series_data`.

Parameters:

- **`ffi`** (`FFI`) – description
- **`data`** (`TimeSeriesLike`) – xarray or pandas based time series

Raises:

- `TypeError` – unexpected input type

Returns:

- **`OwningCffiNativeHandle`** ( `OwningCffiNativeHandle` ) – wrapper to a C struct multi_regular_time_series_data

Source code in `src/cinterop/cffi/marshal.py`

```
def as_native_time_series(ffi: FFI, data: TimeSeriesLike) -> OwningCffiNativeHandle:
    """Convert a pure python time series to a native representation via a C struct `multi_regular_time_series_data`.

    Args:
        ffi (FFI): _description_
        data (TimeSeriesLike): xarray or pandas based time series

    Raises:
        TypeError: unexpected input type

    Returns:
        OwningCffiNativeHandle: wrapper to a C struct `multi_regular_time_series_data`
    """
    ptr = ffi.new("multi_regular_time_series_data*")
    tsg = get_native_tsgeom(ffi, data)
    ptr.time_series_geometry = tsg.obj
    if isinstance(data, xr.DataArray):
        np_data = data.values
        if len(data.shape) == 1:
            ensemble_size = 1
        elif len(data.shape) == 2:  # noqa: PLR2004
            if not set(data.variable.dims) == {ENSEMBLE_DIMNAME, TIME_DIMNAME}:
                raise ValueError(
                    "Expected dimensions of the data array to be exactly 'ensemble' and 'time', but got: "
                    + str(data.variable.dims),
                )
            ensemble_size = len(data.coords[ENSEMBLE_DIMNAME].values)
            if data.variable.dims[0] != ENSEMBLE_DIMNAME:
                np_data = data.values.transpose()
        else:
            raise ValueError("Cannot convert data with more than 2 dimensions")
    elif isinstance(data, pd.Series):
        ensemble_size = 1
        np_data = data.values
    elif isinstance(data, pd.DataFrame):
        ensemble_size = data.shape[1]
        np_data = data.values.transpose()
    else:
        raise TypeError("Not recognised as a type of time series: " + str(type(data)))
    ptr.ensemble_size = ensemble_size
    num_data = two_d_np_array_double_to_native(ffi, np_data)
    ptr.numeric_data = num_data.ptr
    result = OwningCffiNativeHandle(ptr)
    result.keepalive = [tsg, num_data] # type: ignore[attr-defined]
    return result
```

### as_native_tsgeom

```
as_native_tsgeom(
    ffi: FFI, tsgeom: TimeSeriesGeometry
) -> TimeSeriesGeometryNative
```

Convert a simlified time series geometry to a native representation.

Parameters:

- **`ffi`** (`Union[FFI, CffiData]`) – FFI instance, or a preexisting cdata pointer to a regular_time_series_geometry struct
- **`tsgeom`** (`TimeSeriesGeometry`) – simplified representation

Returns:

- **`TimeSeriesGeometryNative`** ( `TimeSeriesGeometryNative` ) – Wrapper around a cdata pointer to a new C struct regular_time_series_geometry

Source code in `src/cinterop/cffi/marshal.py`

```
def as_native_tsgeom(ffi: FFI, tsgeom: TimeSeriesGeometry) -> TimeSeriesGeometryNative:
    """Convert a simlified time series geometry to a native representation.

    Args:
        ffi (Union[FFI, CffiData]): FFI instance, or a preexisting cdata pointer to a `regular_time_series_geometry` struct
        tsgeom (TimeSeriesGeometry): simplified representation

    Returns:
        TimeSeriesGeometryNative: Wrapper around a cdata pointer to a new C struct `regular_time_series_geometry`
    """
    return tsgeom.as_native(ffi)
```

### as_np_array_double

```
as_np_array_double(
    ffi: FFI,
    ptr: CffiData,
    size: int,
    shallow: bool = False,
) -> ndarray
```

Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats `double[n]`.

The returned numpy array may be directly pointing to the original data (faster performance), or a deep copy (memory safety - "normal" numpy array)

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory
- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData)
- **`size`** (`int`) – array size
- **`shallow`** (`bool`, default: `False` ) – If True the resulting numpy array points directly to the native data array. Otherwise, return a numpy array with a deep copy of the data, managed by Python. Defaults to False.

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `ndarray` – np.ndarray: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def as_np_array_double(
    ffi: FFI,
    ptr: CffiData,
    size: int,
    shallow: bool = False,  # noqa: FBT001, FBT002
) -> np.ndarray:
    """Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats `double[n]`.

    The returned numpy array may be directly pointing to the original data (faster performance), or a deep copy (memory safety - "normal" numpy array)

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData)
        size (int): array size
        shallow (bool): If True the resulting numpy array points directly to the native data array. Otherwise, return a numpy array with a deep copy of the data, managed by Python. Defaults to False.

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        np.ndarray: converted data
    """
    res = np.frombuffer(ffi.buffer(ffi.cast("double[%d]" % (size,), ptr)))  # noqa: UP031
    if shallow:
        return res
    return res.copy()
```

### as_numeric_np_array

```
as_numeric_np_array(
    ffi: FFI,
    ptr: CffiData,
    size: int,
    shallow: bool = False,
) -> ndarray
```

Convert if possible a cffi pointer to a C data array, into a numpy array.

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory
- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData)
- **`size`** (`int`) – array size
- **`shallow`** (`bool`, default: `False` ) – If true the array points directly to native data array. Defaults to False.

Raises:

- `TypeError` – conversion is not supported

Returns:

- `ndarray` – np.ndarray: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def as_numeric_np_array(
    ffi: FFI,
    ptr: CffiData,
    size: int,
    shallow: bool = False,  # noqa: FBT001, FBT002
) -> np.ndarray:
    """Convert if possible a cffi pointer to a C data array, into a numpy array.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData)
        size (int): array size
        shallow (bool): If true the array points directly to native data array. Defaults to False.

    Raises:
        TypeError: conversion is not supported

    Returns:
        np.ndarray: converted data
    """
    t = ffi.typeof(ptr).cname  # e.g. 'double *'
    if t not in _c2dtype:
        raise TypeError("Cannot (yet)create an array for element type: %s" % t)  # noqa: UP031
    dtype = _c2dtype[t]
    buffer_size = size * dtype.itemsize
    res = np.frombuffer(ffi.buffer(ptr, buffer_size), dtype)
    if shallow:
        return res
    return res.copy()
```

### as_string

```
as_string(obj: Any) -> Union[str, Any]
```

Convert obj to string/unicode if it is a bytes object.

Mostly a legacy for python2/3 compatibility.

Parameters:

- **`obj`** (`Any`) – object to convert

Returns:

- `Union[str, Any]` – Union\[str, Any\]: result converted (or not) to unicode string

Source code in `src/cinterop/cffi/marshal.py`

```
def as_string(obj: Any) -> Union[str, Any]:
    """Convert obj to string/unicode if it is a bytes object.

    Mostly a legacy for python2/3 compatibility.

    Args:
        obj (Any): object to convert

    Returns:
        Union[str, Any]: result converted (or not) to unicode string
    """
    if isinstance(obj, bytes):
        return obj.decode("utf-8")
    return obj
```

### as_xarray_time_series

```
as_xarray_time_series(
    ffi: FFI,
    ptr: CffiData,
    name: Optional[str] = None,
    allow_empty: bool = True,
) -> Optional[DataArray]
```

Converts a native time series structure to an xarray representation.

Parameters:

- **`ffi`** (`FFI`) – ffi object to the library
- **`ptr`** (`CffiData`) – pointer to the native struct multi_regular_time_series_data
- **`name`** (`str`, default: `None` ) – name of the returned series. Defaults to None.

Returns:

- `Optional[DataArray]` – xr.DataArray: xarray time series

Source code in `src/cinterop/cffi/marshal.py`

```
def as_xarray_time_series(
    ffi: FFI,
    ptr: CffiData,
    name: Optional[str] = None,
    allow_empty: bool = True,  # noqa: FBT001, FBT002
) -> Optional[xr.DataArray]:
    """Converts a native time series structure to an xarray representation.

    Args:
        ffi (FFI): ffi object to the library
        ptr (CffiData): pointer to the native struct `multi_regular_time_series_data`
        name (str, optional): name of the returned series. Defaults to None.

    Returns:
        xr.DataArray: xarray time series
    """
    if allow_empty and ptr.ensemble_size < 0:
        return None
    ts_geom = TimeSeriesGeometryNative(ptr.time_series_geometry)
    npx = two_d_as_np_array_double(
        ffi,
        ptr.numeric_data,
        ptr.ensemble_size,
        ts_geom.length,
    )
    time_index = _ts_geom_to_time_index(ts_geom)
    ens_index = list(range(ptr.ensemble_size))
    x = create_ensemble_series(npx, ens_index, time_index)
    if name is not None:
        x.name = name
    return x
```

### c_charptrptr_as_string_list

```
c_charptrptr_as_string_list(
    ffi: FFI, ptr: CffiData, size: int
) -> List[str]
```

Convert if possible a cffi pointer to a C data array char\*\* , into a list of python strings.

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory
- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData)
- **`size`** (`int`) – number of character strings in the char\*\* pointer

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `List[str]` – List\[str\]: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def c_charptrptr_as_string_list(ffi: FFI, ptr: CffiData, size: int) -> List[str]:
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
    strings = ffi.cast("char*[%d]" % (size,), ptr)  # noqa: UP031
    return [as_string(ffi.string(strings[i])) for i in range(size)]
```

### c_string_as_py_string

```
c_string_as_py_string(ffi: FFI, ptr: CffiData) -> str
```

Convert if possible a cffi pointer to an ANSI C string to a python string.

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory
- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData)

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- **`str`** ( `str` ) – converted string

Source code in `src/cinterop/cffi/marshal.py`

```
def c_string_as_py_string(ffi: FFI, ptr: CffiData) -> str:
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
```

### convert_strings

```
convert_strings(func: Callable) -> Callable
```

Returns a wrapper that converts any str/unicode object arguments to bytes.

Source code in `src/cinterop/cffi/marshal.py`

```
def convert_strings(func: Callable) -> Callable:
    """Returns a wrapper that converts any str/unicode object arguments to bytes."""

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> Any:
        """Convert args.

        :param func func: Python function wrapping a lakeoned function.
        """
        new_args = []
        for arg in args:
            new_args.append(as_bytes(arg))
        new_kwargs = {}
        for key in kwargs:  # noqa: PLC0206
            new_kwargs[key] = as_bytes(kwargs[key])

        # Call the function
        return_value = func(*new_args, **new_kwargs)
        if isinstance(return_value, (list, tuple)):
            return [as_string(obj) for obj in return_value]
        return as_string(return_value)

    return wrapper
```

### create_values_struct

```
create_values_struct(
    ffi: FFI, data: Union[List[float], ndarray]
) -> OwningCffiNativeHandle
```

Convert a list or array of numeric values to a cffi pointer to a `values_vector` struct.

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory
- **`data`** (`Union[List[float], ndarray]`) – list or array of numeric values

Returns:

- **`OwningCffiNativeHandle`** ( `OwningCffiNativeHandle` ) – A wrapper that owns the memory allocated for the resulting values_vector pointed to.

Source code in `src/cinterop/cffi/marshal.py`

```
def create_values_struct(
    ffi: FFI,
    data: Union[List[float], np.ndarray],
) -> OwningCffiNativeHandle:
    """Convert a list or array of numeric values to a cffi pointer to a `values_vector` struct.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        data (Union[List[float], np.ndarray]): list or array of numeric values

    Returns:
        OwningCffiNativeHandle: A wrapper that owns the memory allocated for the resulting `values_vector` pointed to.
    """
    ptr = ffi.new("values_vector*")
    ptr.size = len(data)
    ptr.values = as_c_double_array(ffi, data).ptr
    return OwningCffiNativeHandle(ptr)
```

### datetime_to_dtts

```
datetime_to_dtts(
    ffi: FFI, dt: datetime
) -> OwningCffiNativeHandle
```

Convert a python datetime to a cffi pointer to a C struct `date_time_to_second`.

Source code in `src/cinterop/cffi/marshal.py`

```
def datetime_to_dtts(ffi: FFI, dt: datetime) -> OwningCffiNativeHandle:
    """Convert a python datetime to a cffi pointer to a C struct `date_time_to_second`."""
    ptr = ffi.new("date_time_to_second*")
    _copy_datetime_to_dtts(dt, ptr)
    return OwningCffiNativeHandle(ptr)
```

### dict_to_named_values

```
dict_to_named_values(
    ffi: FFI, data: Dict[str, float]
) -> OwningCffiNativeHandle
```

Convert a dictionary to a cffi pointer to a `named_values_vector` struct.

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory
- **`data`** (`Dict[str, float]`) – mapping from keys to numeric values

Returns:

- **`OwningCffiNativeHandle`** ( `OwningCffiNativeHandle` ) – A wrapper that owns the memory allocated for the resulting named_values_vector pointed to

Source code in `src/cinterop/cffi/marshal.py`

```
def dict_to_named_values(ffi: FFI, data: Dict[str, float]) -> OwningCffiNativeHandle:
    """Convert a dictionary to a cffi pointer to a `named_values_vector` struct.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        data (Dict[str,float]): mapping from keys to numeric values

    Returns:
        OwningCffiNativeHandle: A wrapper that owns the memory allocated for the resulting `named_values_vector` pointed to
    """
    ptr = ffi.new("named_values_vector*")
    ptr.size = len(data)
    values = as_c_double_array(ffi, list(data.values()))
    names = as_arrayof_bytes(ffi, list(data.keys()))
    ptr.values = values.ptr
    ptr.names = names.ptr
    result = OwningCffiNativeHandle(ptr)
    result.keepalive = [names, values] # type: ignore[attr-defined]
    return result
```

### dict_to_string_map

```
dict_to_string_map(
    ffi: FFI, data: Dict[str, str]
) -> OwningCffiNativeHandle
```

Convert a dictionary to a cffi pointer to a `string_string_map` struct.

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory
- **`data`** (`Dict[str, float]`) – mapping from keys to (str) values

Returns:

- **`OwningCffiNativeHandle`** ( `OwningCffiNativeHandle` ) – A wrapper that owns the memory allocated for the resulting string_string_map pointed to.

Source code in `src/cinterop/cffi/marshal.py`

```
def dict_to_string_map(ffi: FFI, data: Dict[str, str]) -> OwningCffiNativeHandle:
    """Convert a dictionary to a cffi pointer to a `string_string_map` struct.

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
    result.keepalive = [keys, values] # type: ignore[attr-defined]
    return result
```

### dtts_as_datetime

```
dtts_as_datetime(ptr: CffiData) -> datetime
```

Convert if possible a cffi pointer to a C data array char\*\* , into a list of python strings.

Parameters:

- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData)

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- **`datetime`** ( `datetime` ) – converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def dtts_as_datetime(ptr: CffiData) -> datetime:
    """Convert if possible a cffi pointer to a C data array char** , into a list of python strings.

    Args:
        ptr (CffiData): cffi pointer (FFI.CData)

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        datetime: converted data
    """
    dtts = ptr  # ffi.cast('date_time_to_second*', ptr)
    return datetime(  # noqa: DTZ001
        dtts.year,
        dtts.month,
        dtts.day,
        dtts.hour,
        dtts.minute,
        dtts.second,
        tzinfo=None,
    )
```

### geom_to_xarray_time_series

```
geom_to_xarray_time_series(
    ts_geom: TimeSeriesGeometryNative,
    data: ndarray,
    name: Optional[str] = None,
) -> DataArray
```

Converts an native time series structure to an xarray representation.

Parameters:

- **`ts_geom`** (`TimeSeriesGeometryNative`) – time series geometry
- **`data`** (`ndarray`) – time series data, with one dimension
- **`name`** (`str`, default: `None` ) – name of the returned series. Defaults to None.

Returns:

- `DataArray` – xr.DataArray: xarray time series

Source code in `src/cinterop/cffi/marshal.py`

```
def geom_to_xarray_time_series(
    ts_geom: TimeSeriesGeometryNative,
    data: np.ndarray,
    name: Optional[str] = None,
) -> xr.DataArray:
    """Converts an native time series structure to an xarray representation.

    Args:
        ts_geom (TimeSeriesGeometryNative): time series geometry
        data (np.ndarray): time series data, with one dimension
        name (str, optional): name of the returned series. Defaults to None.

    Returns:
        xr.DataArray: xarray time series
    """
    if len(data.shape) != 1:
        raise ValueError("Expected data to be a 1D array, but got shape " + str(data.shape))
    data = data.reshape((1, len(data)))
    time_index = _ts_geom_to_time_index(ts_geom)
    ens_index = [0]
    x = create_ensemble_series(data, ens_index, time_index)
    if name is not None:
        x.name = name
    return x
```

### get_native_tsgeom

```
get_native_tsgeom(
    ffi: FFI, pd_series: TimeSeriesLike
) -> OwningCffiNativeHandle
```

Get a native representation of the geometry of a time series. A simple heuristic is used to find the time step.

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory
- **`pd_series`** (`TimeSeriesLike`) – A pandas or xarray representation of a time series, with the pandas index or "time" dimension expected.

Raises:

- `TypeError` – Unexpected type of data

Returns:

- **`OwningCffiNativeHandle`** ( `OwningCffiNativeHandle` ) – wrapper to a cdata pointer to a new C struct regular_time_series_geometry

Source code in `src/cinterop/cffi/marshal.py`

```
def get_native_tsgeom(ffi: FFI, pd_series: "TimeSeriesLike") -> OwningCffiNativeHandle:
    """Get a native representation of the geometry of a time series. A simple heuristic is used to find the time step.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        pd_series (TimeSeriesLike): A pandas or xarray representation of a time series, with the pandas index or "time" dimension expected.

    Raises:
        TypeError: Unexpected type of data

    Returns:
        OwningCffiNativeHandle: wrapper to a cdata pointer to a new C struct `regular_time_series_geometry`
    """
    # stopifnot(xts::is.xts(pd_series))
    return as_native_tsgeom(ffi, get_tsgeom(pd_series))
```

### get_tsgeom

```
get_tsgeom(data: TimeSeriesLike) -> TimeSeriesGeometry
```

Extract a simplified representation of the geometry of a time series. A simple heuristic is used to find the time step.

Parameters:

- **`data`** (`TimeSeriesLike`) – A pandas or xarray representation of a time series, with the pandas index or "time" dimension expected.

Raises:

- `TypeError` – Unexpected type of data

Returns:

- **`TimeSeriesGeometry`** ( `TimeSeriesGeometry` ) – simplified time series geometry

Source code in `src/cinterop/cffi/marshal.py`

```
def get_tsgeom(data: TimeSeriesLike) -> TimeSeriesGeometry:
    """Extract a simplified representation of the geometry of a time series. A simple heuristic is used to find the time step.

    Args:
        data (TimeSeriesLike): A pandas or xarray representation of a time series, with the pandas index or "time" dimension expected.

    Raises:
        TypeError: Unexpected type of data

    Returns:
        TimeSeriesGeometry: simplified time series geometry
    """
    if isinstance(data, xr.DataArray):
        indx = data.coords[TIME_DIMNAME].values
    elif isinstance(data, (pd.Series, pd.DataFrame)):
        indx = _pd_index(data)
    else:
        raise TypeError("Not recognised as a type of time series: " + str(type(data)))
    if len(indx) < 2:  # noqa: PLR2004
        raise ValueError(
            "There must be at least two entries in the time series to guess the time step length",
        )
    a = as_timestamp(indx[0])
    b = as_timestamp(indx[1])
    first_delta = b - a
    time_step_code = 0
    time_step = int(first_delta.total_seconds())
    if time_step > 86400 * 27:  # HACK: assume monthly
        time_step_code = 1
        time_step = -1
    return TimeSeriesGeometry(a, time_step, len(indx), time_step_code)
```

### named_values_to_dict

```
named_values_to_dict(
    ffi: FFI, ptr: CffiData
) -> Dict[str, float]
```

Convert if possible a cffi pointer to a `named_values_vector` struct, into a dictionary.

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory
- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData) to a named_values_vector struct

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `Dict[str, float]` – Dict\[str,float\]: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def named_values_to_dict(ffi: FFI, ptr: CffiData) -> Dict[str, float]:
    """Convert if possible a cffi pointer to a `named_values_vector` struct, into a dictionary.

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
        raise KeyError(
            "Names of the values are not unique; cannot use as keys to make a dictionary",
        )
    return {names[i]: values[i] for i in range(len(names))}
```

### new_charptr_array

```
new_charptr_array(
    ffi: FFI, size: int, wrap: bool = False
) -> Union[OwningCffiNativeHandle, CffiData]
```

Creates a new C array of pointers to char: `char*[n]`.

Parameters:

- **`ffi`** (`FFI`) – ffi object to the native library accessed
- **`size`** (`int`) – array size
- **`wrap`** (`bool`, default: `False` ) – return a "naked" cdata pointer object if False, or wrapped in a OwningCffiNativeHandle if True. Defaults to False.

Returns:

- `Union[OwningCffiNativeHandle, CffiData]` – Union\[OwningCffiNativeHandle,CffiData\]: a (wrapper to a) cdata pointer object owning a new array of char \*s of length size

Source code in `src/cinterop/cffi/marshal.py`

```
def new_charptr_array(
    ffi: FFI,
    size: int,
    wrap: bool = False,  # noqa: FBT001, FBT002
) -> Union[OwningCffiNativeHandle, CffiData]:
    """Creates a new C array of pointers to char:  `char*[n]`.

    Args:
        ffi (FFI): ffi object to the native library accessed
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a)  cdata pointer object owning a new array of `char *`s of length `size`
    """
    return new_ctype_array(ffi, "char*", size, wrap)
```

### new_ctype_array

```
new_ctype_array(
    ffi: FFI, ctype: str, size: int, wrap: bool = False
) -> Union[OwningCffiNativeHandle, CffiData]
```

Creates a new C array of a specified type and size.

Parameters:

- **`ffi`** (`FFI`) – ffi object to the native library accessed
- **`ctype`** (`str`) – valid C type for array creation
- **`size`** (`int`) – array size
- **`wrap`** (`bool`, default: `False` ) – return a "naked" cdata pointer object if False, or wrapped in a OwningCffiNativeHandle if True. Defaults to False.

Returns:

- `Union[OwningCffiNativeHandle, CffiData]` – Union\[OwningCffiNativeHandle,CffiData\]: cdata pointer or wrapper to it.

Source code in `src/cinterop/cffi/marshal.py`

```
def new_ctype_array(
    ffi: FFI,
    ctype: str,
    size: int,
    wrap: bool = False,  # noqa: FBT001, FBT002
) -> Union[OwningCffiNativeHandle, CffiData]:
    """Creates a new C array of a specified type and size.

    Args:
        ffi (FFI): ffi object to the native library accessed
        ctype (str): valid C type for array creation
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: cdata pointer or wrapper to it.
    """
    __check_positive_size(size)
    x = ffi.new("%s[%d]" % (ctype, size))  # noqa: UP031
    if wrap:
        return OwningCffiNativeHandle(x)
    return x
```

### new_date_time_to_second

```
new_date_time_to_second(ffi: FFI) -> OwningCffiNativeHandle
```

Create a new cffi pointer to a C struct `date_time_to_second`.

Source code in `src/cinterop/cffi/marshal.py`

```
def new_date_time_to_second(ffi: FFI) -> OwningCffiNativeHandle:
    """Create a new cffi pointer to a C struct `date_time_to_second`."""
    ptr = ffi.new("date_time_to_second*")
    return OwningCffiNativeHandle(ptr)
```

### new_double_array

```
new_double_array(
    ffi: FFI, size: int, wrap: bool = False
) -> Union[OwningCffiNativeHandle, CffiData]
```

Creates a new C array of double precision floats `double[n]`.

Parameters:

- **`ffi`** (`FFI`) – ffi object to the native library accessed
- **`size`** (`int`) – array size
- **`wrap`** (`bool`, default: `False` ) – return a "naked" cdata pointer object if False, or wrapped in a OwningCffiNativeHandle if True. Defaults to False.

Returns:

- `Union[OwningCffiNativeHandle, CffiData]` – Union\[OwningCffiNativeHandle,CffiData\]: a (wrapper to a) cdata pointer object owning a new array of doubles of length size

Source code in `src/cinterop/cffi/marshal.py`

```
def new_double_array(
    ffi: FFI,
    size: int,
    wrap: bool = False,  # noqa: FBT001, FBT002
) -> Union[OwningCffiNativeHandle, CffiData]:
    """Creates a new C array of double precision floats `double[n]`.

    Args:
        ffi (FFI): ffi object to the native library accessed
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of `double`s of length `size`
    """
    return new_ctype_array(ffi, "double", size, wrap)
```

### new_doubleptr_array

```
new_doubleptr_array(
    ffi: FFI, size: int, wrap: bool = False
) -> Union[OwningCffiNativeHandle, CffiData]
```

Creates a new C array of pointers to double precision floats `double*[n]`.

Parameters:

- **`ffi`** (`FFI`) – ffi object to the native library accessed
- **`size`** (`int`) – array size
- **`wrap`** (`bool`, default: `False` ) – return a "naked" cdata pointer object if False, or wrapped in a OwningCffiNativeHandle if True. Defaults to False.

Returns:

- `Union[OwningCffiNativeHandle, CffiData]` – Union\[OwningCffiNativeHandle,CffiData\]: a (wrapper to a) cdata pointer object owning a new array of double \*s of length size

Source code in `src/cinterop/cffi/marshal.py`

```
def new_doubleptr_array(
    ffi: FFI,
    size: int,
    wrap: bool = False,  # noqa: FBT001, FBT002
) -> Union[OwningCffiNativeHandle, CffiData]:
    """Creates a new C array of pointers to double precision floats `double*[n]`.

    Args:
        ffi (FFI): ffi object to the native library accessed
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of `double *`s of length `size`
    """
    return new_ctype_array(ffi, "double*", size, wrap)
```

### new_int_array

```
new_int_array(
    ffi: FFI, size: int, wrap: bool = False
) -> Union[OwningCffiNativeHandle, CffiData]
```

Creates a new C array of integers `int[n]`.

Parameters:

- **`ffi`** (`FFI`) – ffi object to the native library accessed
- **`size`** (`int`) – array size
- **`wrap`** (`bool`, default: `False` ) – return a "naked" cdata pointer object if False, or wrapped in a OwningCffiNativeHandle if True. Defaults to False.

Returns:

- `Union[OwningCffiNativeHandle, CffiData]` – Union\[OwningCffiNativeHandle,CffiData\]: a (wrapper to a) cdata pointer object owning a new array of integers of length size

Source code in `src/cinterop/cffi/marshal.py`

```
def new_int_array(
    ffi: FFI,
    size: int,
    wrap: bool = False,  # noqa: FBT001, FBT002
) -> Union[OwningCffiNativeHandle, CffiData]:
    """Creates a new C array of integers `int[n]`.

    Args:
        ffi (FFI): ffi object to the native library accessed
        size (int): array size
        wrap (bool, optional): return a "naked" cdata pointer object if False, or wrapped in a `OwningCffiNativeHandle` if True. Defaults to False.

    Returns:
        Union[OwningCffiNativeHandle,CffiData]: a (wrapper to a) cdata pointer object owning a new array of integers of length `size`
    """
    return new_ctype_array(ffi, "int", size, wrap)
```

### new_int_scalar_ptr

```
new_int_scalar_ptr(ffi: FFI, value: int = 0) -> CffiData
```

Creates a new C array of integers.

Parameters:

- **`ffi`** (`FFI`) – ffi object to the native library accessed
- **`value`** (`int`, default: `0` ) – description. Defaults to 0.

Returns:

- **`CffiData`** ( `CffiData` ) – a cdata pointer object owning a new pointer to a single integer valued as specified.

Source code in `src/cinterop/cffi/marshal.py`

```
def new_int_scalar_ptr(ffi: FFI, value: int = 0) -> "CffiData":
    """Creates a new C array of integers.

    Args:
        ffi (FFI): ffi object to the native library accessed
        value (int, optional): _description_. Defaults to 0.

    Returns:
        CffiData: a cdata pointer object owning a new pointer to a single integer valued as specified.
    """
    ptr = ffi.new("int*")
    ptr[0] = value
    return ptr
```

### string_map_to_dict

```
string_map_to_dict(
    ffi: FFI, ptr: CffiData
) -> Dict[str, str]
```

Convert if possible a cffi pointer to a `string_string_map` struct, into a dictionary.

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory
- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData) to a string_string_map struct

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `Dict[str, str]` – Dict\[str,str\]: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def string_map_to_dict(ffi: FFI, ptr: CffiData) -> Dict[str, str]:
    """Convert if possible a cffi pointer to a `string_string_map` struct, into a dictionary.

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
        raise KeyError(
            "Names of the values are not unique; cannot use as keys to make a dictionary",
        )
    return {keys[i]: values[i] for i in range(len(keys))}
```

### two_d_as_np_array_double

```
two_d_as_np_array_double(
    ffi: FFI, ptr: CffiData, nrow: int, ncol: int
) -> ndarray
```

Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory
- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData)
- **`nrow`** (`int`) – number of rows
- **`ncol`** (`int`) – number of columns

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `ndarray` – np.ndarray: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def two_d_as_np_array_double(
    ffi: FFI,
    ptr: CffiData,
    nrow: int,
    ncol: int,
) -> np.ndarray:
    """Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData)
        nrow (int): number of rows
        ncol (int): number of columns

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        np.ndarray: converted data
    """
    # TODO check type
    if (
        nrow == 0 or ncol == 0
    ):  # do not cast a native ptr that is likely nullptr or worse. Following works thankfully as an edge case.
        return np.ndarray(shape=(nrow, ncol))
    rows = ffi.cast("double*[%d]" % (nrow,), ptr)  # noqa: UP031
    # We can use a shallow creation for as_numeric_np_array: np.vstack does a copy anyway.
    res = np.vstack(
        [as_numeric_np_array(ffi, rows[i], size=ncol, shallow=True) for i in range(nrow)],
    )
    return res  # noqa: RET504
```

### two_d_np_array_double_to_native

```
two_d_np_array_double_to_native(
    ffi: FFI, data: ndarray
) -> OwningCffiNativeHandle
```

Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory
- **`data`** (`ndarray`) – data

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `OwningCffiNativeHandle` – np.ndarray: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def two_d_np_array_double_to_native(
    ffi: FFI,
    data: np.ndarray,
) -> OwningCffiNativeHandle:
    """Convert if possible a cffi pointer to a C data array, into a numpy array of double precision floats.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        data (np.ndarray): data

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        np.ndarray: converted data
    """
    if not isinstance(data, np.ndarray):
        raise TypeError("Expected np.ndarray, got " + str(type(data)))
    if len(data.shape) > 2:  # noqa: PLR2004
        raise TypeError(
            "Expected an array of dimension 1 or 2, got " + str(len(data.shape)),
        )

    if len(data.shape) == 1:
        data = data.reshape((1, len(data)))

    nrow = data.shape[0]
    ptr: CffiData = new_doubleptr_array(ffi, nrow, wrap=False)
    items = [as_c_double_array(ffi, data[i, :]).ptr for i in range(nrow)]
    for i in range(nrow):
        ptr[i] = items[i]
    result = OwningCffiNativeHandle(ptr)
    result.keepalive = items # type: ignore[attr-defined]
    return result
```

### values_to_nparray

```
values_to_nparray(ffi: FFI, ptr: CffiData) -> ndarray
```

Convert if possible a cffi pointer to a `values_vector` struct, into a python array.

Parameters:

- **`ffi`** (`FFI`) – FFI instance wrapping the native compilation module owning the native memory
- **`ptr`** (`CffiData`) – cffi pointer (FFI.CData) to a values_vector struct

Raises:

- `RuntimeError` – conversion is not supported

Returns:

- `ndarray` – np.ndarray: converted data

Source code in `src/cinterop/cffi/marshal.py`

```
def values_to_nparray(ffi: FFI, ptr: CffiData) -> np.ndarray:
    """Convert if possible a cffi pointer to a `values_vector` struct, into a python array.

    Args:
        ffi (FFI): FFI instance wrapping the native compilation module owning the native memory
        ptr (CffiData): cffi pointer (FFI.CData) to a `values_vector` struct

    Raises:
        RuntimeError: conversion is not supported

    Returns:
        np.ndarray: converted data
    """
    return as_np_array_double(ffi, ptr.values, ptr.size, shallow=False)
```

## timeseries

Python representations of multidimensional time series and interop with Python cffi.

Functions:

- **`as_datetime64`** – Convert, if possible, to a numpy datetime64.
- **`as_pydatetime`** – Convert, if possible, to a datetime.
- **`as_timestamp`** – Converts, if possible, a value to a pandas Timestamp.
- **`create_daily_time_index`** – Creates a daily time index.
- **`create_ensemble_forecasts_series`** – Create an ensemble forecasts time series (i.e. a series of ensembles of series).
- **`create_ensemble_series`** – Create an ensemble (i.e. special type of multi-variate) time series.
- **`create_even_time_index`** – Creates a regular, evenly spaces time index.
- **`create_hourly_time_index`** – Creates an hourly time index.
- **`create_monthly_time_index`** – Creates a monthly time index.
- **`create_single_series`** – Create an uni-variate time series.
- **`end_ts`** – Gets the ending date of a time series.
- **`mk_daily_xarray_series`** – Create a daily xarray time series.
- **`mk_even_step_xarray_series`** – Create an xarray time series with an even time step.
- **`mk_hourly_xarray_series`** – Create an hourly xarray time series.
- **`mk_xarray_series`** – Create an xarray time series.
- **`pd_series_to_xr_series`** – Converts a pandas series to an xarray.
- **`set_xr_units`** – Sets the units attribute of an xr.DataArray. No effect if x is not a dataarray.
- **`slice_pd_time_series`** – Subset a time series to a period.
- **`slice_xr_time_series`** – Subset a time series to a period.
- **`start_ts`** – Gets the starting date of a time series.
- **`ts_window`** – Gets a temporal window of a time series.
- **`xr_ts_end`** – Deprecated: use end_ts.
- **`xr_ts_start`** – Deprecated: use start_ts.

Attributes:

- **`ConvertibleToTimestamp`** – types that can be converted with relative unambiguity to a pandas Timestamp
- **`TimeSeriesLike`** – types that can represent time series
- **`XR_UNITS_ATTRIB_ID`** (`str`) – key for the units attribute on xarray DataArray objects

### ConvertibleToTimestamp

```
ConvertibleToTimestamp = Union[
    str, datetime, datetime64, Timestamp
]
```

types that can be converted with relative unambiguity to a pandas Timestamp

### TimeSeriesLike

```
TimeSeriesLike = Union[Series, DataFrame, DataArray]
```

types that can represent time series

### XR_UNITS_ATTRIB_ID

```
XR_UNITS_ATTRIB_ID: str = 'units'
```

key for the units attribute on xarray DataArray objects

### as_datetime64

```
as_datetime64(t: ConvertibleToTimestamp) -> datetime64
```

Convert, if possible, to a numpy datetime64.

Parameters:

- **`t`** (`ConvertibleToTimestamp`) – date time value to convert

Raises:

- `ValueError` – input value is not supported, notably values with time zone informations are excluded
- `TypeError` – unexpected input type

Returns:

- `datetime64` – np.datetime64: value as a datetime64

Source code in `src/cinterop/timeseries.py`

```
def as_datetime64(t: ConvertibleToTimestamp) -> np.datetime64:
    """Convert, if possible, to a numpy datetime64.

    Args:
        t (ConvertibleToTimestamp): date time value to convert

    Raises:
        ValueError: input value is not supported, notably values with time zone informations are excluded
        TypeError: unexpected input type

    Returns:
        np.datetime64: value as a datetime64
    """
    return as_timestamp(t).to_datetime64()
```

### as_pydatetime

```
as_pydatetime(t: ConvertibleToTimestamp) -> datetime
```

Convert, if possible, to a datetime.

Parameters:

- **`t`** (`ConvertibleToTimestamp`) – date time value to convert

Raises:

- `ValueError` – input value is not supported, notably values with time zone informations are excluded
- `TypeError` – unexpected input type

Returns:

- **`datetime`** ( `datetime` ) – value as a datetime

Source code in `src/cinterop/timeseries.py`

```
def as_pydatetime(t: ConvertibleToTimestamp) -> datetime:
    """Convert, if possible, to a datetime.

    Args:
        t (ConvertibleToTimestamp): date time value to convert

    Raises:
        ValueError: input value is not supported, notably values with time zone informations are excluded
        TypeError: unexpected input type

    Returns:
        datetime: value as a datetime
    """
    return as_timestamp(t).to_pydatetime()
```

### as_timestamp

```
as_timestamp(t: ConvertibleToTimestamp) -> Timestamp
```

Converts, if possible, a value to a pandas `Timestamp`.

Parameters:

- **`t`** (`ConvertibleToTimestamp`) – date time value to convert

Raises:

- `ValueError` – input value is not supported, notably values with time zone informations are excluded
- `TypeError` – unexpected input type

Returns:

- `Timestamp` – pd.Timestamp: date time as a pandas Timestamp

Source code in `src/cinterop/timeseries.py`

```
def as_timestamp(t: ConvertibleToTimestamp) -> pd.Timestamp:
    """Converts, if possible, a value to a pandas `Timestamp`.

    Args:
        t (ConvertibleToTimestamp): date time value to convert

    Raises:
        ValueError: input value is not supported, notably values with time zone informations are excluded
        TypeError: unexpected input type

    Returns:
        pd.Timestamp: date time as a pandas Timestamp
    """
    # initially work around a breaking change in pandas 1.x: "Expected unicode, got numpy.str_'

    # In the future we may support time zones. This is a typically fraught thing, so by default let's stay away from it
    if _is_convertible_to_timestamp(t):
        if isinstance(t, pd.Timestamp):
            if t.tz is not None:
                raise ValueError(
                    "Not supported - Cannot pass a datetime or Timestamp with tzinfo with the tz parameter. Use tz_convert instead",
                )
            return t
        if isinstance(t, datetime) and t.tzinfo is not None:
            raise ValueError(
                "Not supported - Cannot pass a datetime or Timestamp with tzinfo with the tz parameter. Use tz_convert instead",
            )
        parsed = pd.Timestamp(t)
        if parsed.tz is not None:
            raise ValueError(
                "To avoid ambiguities time zones are not supported. All date times must be 'naive'",
            )
        return parsed
    raise TypeError(
        "Cannot convert to a timestamp the object of type" + str(type(t)),
    )
```

### create_daily_time_index

```
create_daily_time_index(
    start: ConvertibleToTimestamp, n: int
) -> DatetimeIndex
```

Creates a daily time index.

Parameters:

- **`start`** (`ConvertibleToTimestamp`) – first datetime in the time index
- **`n`** (`int`) – length of the index

Returns:

- `DatetimeIndex` – pd.DatetimeIndex: a time index suitable for a time series.

Source code in `src/cinterop/timeseries.py`

```
def create_daily_time_index(start: ConvertibleToTimestamp, n: int) -> pd.DatetimeIndex:
    """Creates a daily time index.

    Args:
        start (ConvertibleToTimestamp): first datetime in the time index
        n (int): length of the index

    Returns:
        pd.DatetimeIndex: a time index suitable for a time series.
    """
    start = as_datetime64(start)
    return pd.date_range(
        start,
        periods=n,
        freq="D",
    )  # much faster than list comprehension, see https://jmp75.github.io/work-blog/c++/python/performance/runtime/2022/08/09/python-profiling-interop.html
```

### create_ensemble_forecasts_series

```
create_ensemble_forecasts_series(
    npx: ndarray,
    ens_index: List,
    lead_time_index: List,
    time_index: Union[List, DatetimeIndex],
) -> DataArray
```

Create an ensemble forecasts time series (i.e. a series of ensembles of series).

Source code in `src/cinterop/timeseries.py`

```
def create_ensemble_forecasts_series(
    npx: np.ndarray,
    ens_index: List,
    lead_time_index: List,
    time_index: Union[List, pd.DatetimeIndex],
) -> xr.DataArray:
    """Create an ensemble forecasts time series (i.e. a series of ensembles of series)."""
    if npx is None:
        npx = np.empty(
            shape=(len(ens_index), len(lead_time_index), len(time_index)),
            dtype=float,
        )
        npx[:] = np.nan
    return xr.DataArray(
        npx,
        coords=[ens_index, lead_time_index, time_index],
        dims=[ENSEMBLE_DIMNAME, LEADTIME_DIMNAME, TIME_DIMNAME],
    )
```

### create_ensemble_series

```
create_ensemble_series(
    npx: ndarray,
    ens_index: List,
    time_index: Union[List, DatetimeIndex],
) -> DataArray
```

Create an ensemble (i.e. special type of multi-variate) time series.

Source code in `src/cinterop/timeseries.py`

```
def create_ensemble_series(
    npx: np.ndarray,
    ens_index: List,
    time_index: Union[List, pd.DatetimeIndex],
) -> xr.DataArray:
    """Create an ensemble (i.e. special type of multi-variate) time series."""
    return xr.DataArray(
        npx,
        coords=[ens_index, time_index],
        dims=[ENSEMBLE_DIMNAME, TIME_DIMNAME],
    )
```

### create_even_time_index

```
create_even_time_index(
    start: ConvertibleToTimestamp,
    time_step_seconds: int,
    n: int,
) -> DatetimeIndex
```

Creates a regular, evenly spaces time index.

Parameters:

- **`start`** (`ConvertibleToTimestamp`) – first datetime in the time index
- **`time_step_seconds`** (`int`) – time step length in seconds
- **`n`** (`int`) – length of the index

Returns:

- `DatetimeIndex` – pd.DatetimeIndex: a time index suitable for a time series.

Source code in `src/cinterop/timeseries.py`

```
def create_even_time_index(
    start: ConvertibleToTimestamp,
    time_step_seconds: int,
    n: int,
) -> pd.DatetimeIndex:
    """Creates a regular, evenly spaces time index.

    Args:
        start (ConvertibleToTimestamp): first datetime in the time index
        time_step_seconds (int): time step length in seconds
        n (int): length of the index

    Returns:
        pd.DatetimeIndex: a time index suitable for a time series.
    """
    if time_step_seconds == _SECONDS_IN_HOUR:
        return create_hourly_time_index(start, n)
    if time_step_seconds == _SECONDS_IN_DAY:
        return create_daily_time_index(start, n)
    start = as_datetime64(start)
    delta_t = np.timedelta64(time_step_seconds, "s")
    # Note: below appears to be a few times faster than pd.date_range with a freq=Dateoffset for some reasons.
    return pd.DatetimeIndex([start + delta_t * i for i in range(n)])
```

### create_hourly_time_index

```
create_hourly_time_index(
    start: ConvertibleToTimestamp, n: int
) -> DatetimeIndex
```

Creates an hourly time index.

Parameters:

- **`start`** (`ConvertibleToTimestamp`) – first datetime in the time index
- **`n`** (`int`) – length of the index

Returns:

- `DatetimeIndex` – pd.DatetimeIndex: a time index suitable for a time series.

Source code in `src/cinterop/timeseries.py`

```
def create_hourly_time_index(start: ConvertibleToTimestamp, n: int) -> pd.DatetimeIndex:
    """Creates an hourly time index.

    Args:
        start (ConvertibleToTimestamp): first datetime in the time index
        n (int): length of the index

    Returns:
        pd.DatetimeIndex: a time index suitable for a time series.
    """
    start = as_datetime64(start)
    return pd.date_range(
        start,
        periods=n,
        freq="h",
    )  # much faster than list comprehension
```

### create_monthly_time_index

```
create_monthly_time_index(
    start: ConvertibleToTimestamp, n: int
) -> DatetimeIndex
```

Creates a monthly time index.

Parameters:

- **`start`** (`ConvertibleToTimestamp`) – first datetime in the time index
- **`n`** (`int`) – length of the index

Raises:

- `ValueError` – day of month of the start date is more than 28

Returns:

- `DatetimeIndex` – pd.DatetimeIndex: a time index suitable for a time series.

Source code in `src/cinterop/timeseries.py`

```
def create_monthly_time_index(
    start: ConvertibleToTimestamp,
    n: int,
) -> pd.DatetimeIndex:
    """Creates a monthly time index.

    Args:
        start (ConvertibleToTimestamp): first datetime in the time index
        n (int): length of the index

    Raises:
        ValueError: day of month of the start date is more than 28

    Returns:
        pd.DatetimeIndex: a time index suitable for a time series.
    """
    pdstart = as_timestamp(start)
    if pdstart.day > 28:  # noqa: PLR2004
        raise ValueError(
            "Monthly time indices require a day of month less than 29. End of months indices are not yet supported.",
        )
    start = as_datetime64(start)
    return pd.date_range(start, periods=n, freq=pd.tseries.offsets.DateOffset(months=1))
```

### create_single_series

```
create_single_series(
    npx: ndarray, time_index: Union[List, DatetimeIndex]
) -> DataArray
```

Create an uni-variate time series.

Source code in `src/cinterop/timeseries.py`

```
def create_single_series(
    npx: np.ndarray,
    time_index: Union[List, pd.DatetimeIndex],
) -> xr.DataArray:
    """Create an uni-variate time series."""
    npx = npx.squeeze()
    if len(npx.shape) != 1:
        raise ValueError("data must be uni-variate")
    return xr.DataArray(npx, coords=[time_index], dims=[TIME_DIMNAME])
```

### end_ts

```
end_ts(x: TimeSeriesLike) -> datetime64
```

Gets the ending date of a time series.

Parameters:

- **`x`** (`TimeSeriesLike`) – time series

Returns:

- **`Any`** ( `datetime64` ) – end of the series

Source code in `src/cinterop/timeseries.py`

```
def end_ts(x: TimeSeriesLike) -> np.datetime64:
    """Gets the ending date of a time series.

    Args:
        x (TimeSeriesLike): time series

    Returns:
        Any: end of the series
    """
    return __ts_index(x)[-1]
```

### mk_daily_xarray_series

```
mk_daily_xarray_series(
    data: Union[ndarray, TimeSeriesLike],
    start_date: ConvertibleToTimestamp,
    dim_name: Optional[str] = None,
    units: Optional[str] = None,
    colnames: Optional[List[str]] = None,
    fill_miss_func: Optional[
        Callable[[TsArrayLike], TsArrayLike]
    ] = None,
) -> DataArray
```

Create a daily xarray time series.

Parameters:

- **`data`** (`Union[ndarray, TimeSeriesLike]`) – data from which to create the xarray series
- **`start_date`** (`ConvertibleToTimestamp`) – start date of the daily time series
- **`dim_name`** (`str`, default: `None` ) – the name of the dimension for a multivariate series. Ignored if univariate. Defaults to None.
- **`units`** (`str`, default: `None` ) – units in the time series. Defaults to None.
- **`colnames`** (`Optional[List[str]]`, default: `None` ) – names of the columns in a multivariate series. Defaults to None.
- **`fill_miss_func`** (`Optional[Callable[[TsArrayLike], TsArrayLike]]`, default: `None` ) – optional function that fills in missing values (np.nan). Defaults to None.

Raises:

- `NotImplementedError` – Input arguments are not consistent.

Returns:

- `DataArray` – xr.DataArray: output xarray time series with at least a dimension "time"

Source code in `src/cinterop/timeseries.py`

```
def mk_daily_xarray_series(
    data: Union[np.ndarray, TimeSeriesLike],
    start_date: ConvertibleToTimestamp,
    dim_name: Optional[str] = None,
    units: Optional[str] = None,
    colnames: Optional[List[str]] = None,
    fill_miss_func: Optional[Callable[[TsArrayLike], TsArrayLike]] = None,
) -> xr.DataArray:
    """Create a daily xarray time series.

    Args:
        data (Union[np.ndarray, TimeSeriesLike]): data from which to create the xarray series
        start_date (ConvertibleToTimestamp): start date of the daily time series
        dim_name (str, optional): the name of the dimension for a multivariate series. Ignored if univariate. Defaults to None.
        units (str, optional): units in the time series. Defaults to None.
        colnames (Optional[List[str]], optional): names of the columns in a multivariate series. Defaults to None.
        fill_miss_func (Optional[Callable[[TsArrayLike], TsArrayLike]], optional): optional function that fills in missing values (np.nan). Defaults to None.

    Raises:
        NotImplementedError: Input arguments are not consistent.

    Returns:
        xr.DataArray: output xarray time series with at least a dimension "time"
    """
    _check_series_data(data, dim_name)
    n = data.shape[0]
    time_index = create_daily_time_index(start_date, n)
    return mk_xarray_series(data, dim_name, units, time_index, colnames, fill_miss_func)
```

### mk_even_step_xarray_series

```
mk_even_step_xarray_series(
    data: Union[ndarray, TimeSeriesLike],
    start_date: ConvertibleToTimestamp,
    time_step_seconds: int,
    dim_name: Optional[str] = None,
    units: Optional[str] = None,
    colnames: Optional[List[str]] = None,
    fill_miss_func: Optional[
        Callable[[TsArrayLike], TsArrayLike]
    ] = None,
) -> DataArray
```

Create an xarray time series with an even time step.

Parameters:

- **`data`** (`Union[ndarray, TimeSeriesLike]`) – data from which to create the xarray series
- **`start_date`** (`ConvertibleToTimestamp`) – start date of the daily time series
- **`time_step_seconds`** (`int`) – time step length in seconds
- **`dim_name`** (`str`, default: `None` ) – the name of the dimension for a multivariate series. Ignored if univariate. Defaults to None.
- **`units`** (`str`, default: `None` ) – units in the time series. Defaults to None.
- **`colnames`** (`Optional[List[str]]`, default: `None` ) – names of the columns in a multivariate series. Defaults to None.
- **`fill_miss_func`** (`Optional[Callable[[TsArrayLike], TsArrayLike]]`, default: `None` ) – optional function that fills in missing values (np.nan). Defaults to None.

Raises:

- `NotImplementedError` – Input arguments are not consistent.

Returns:

- `DataArray` – xr.DataArray: output xarray time series with at least a dimension "time"

Source code in `src/cinterop/timeseries.py`

```
def mk_even_step_xarray_series(
    data: Union[np.ndarray, TimeSeriesLike],
    start_date: ConvertibleToTimestamp,
    time_step_seconds: int,
    dim_name: Optional[str] = None,
    units: Optional[str] = None,
    colnames: Optional[List[str]] = None,
    fill_miss_func: Optional[Callable[[TsArrayLike], TsArrayLike]] = None,
) -> xr.DataArray:
    """Create an xarray time series with an even time step.

    Args:
        data (Union[np.ndarray, TimeSeriesLike]): data from which to create the xarray series
        start_date (ConvertibleToTimestamp): start date of the daily time series
        time_step_seconds (int): time step length in seconds
        dim_name (str, optional): the name of the dimension for a multivariate series. Ignored if univariate. Defaults to None.
        units (str, optional): units in the time series. Defaults to None.
        colnames (Optional[List[str]], optional): names of the columns in a multivariate series. Defaults to None.
        fill_miss_func (Optional[Callable[[TsArrayLike], TsArrayLike]], optional): optional function that fills in missing values (np.nan). Defaults to None.

    Raises:
        NotImplementedError: Input arguments are not consistent.

    Returns:
        xr.DataArray: output xarray time series with at least a dimension "time"
    """
    _check_series_data(data, dim_name)
    n = data.shape[0]
    time_index = create_even_time_index(start_date, time_step_seconds, n)
    return mk_xarray_series(data, dim_name, units, time_index, colnames, fill_miss_func)
```

### mk_hourly_xarray_series

```
mk_hourly_xarray_series(
    data: Union[ndarray, TimeSeriesLike],
    start_date: ConvertibleToTimestamp,
    dim_name: Optional[str] = None,
    units: Optional[str] = None,
    colnames: Optional[List[str]] = None,
    fill_miss_func: Optional[
        Callable[[TsArrayLike], TsArrayLike]
    ] = None,
) -> DataArray
```

Create an hourly xarray time series.

Parameters:

- **`data`** (`Union[ndarray, TimeSeriesLike]`) – Data from which to create the xarray series
- **`dim_name`** (`str`, default: `None` ) – the name of the dimension for a multivariate series. Ignored if univariate. Defaults to None.
- **`units`** (`str`, default: `None` ) – units in the time series. Defaults to None.
- **`colnames`** (`Optional[List[str]]`, default: `None` ) – names of the columns in a multivariate series. Defaults to None.
- **`fill_miss_func`** (`Optional[Callable[[TsArrayLike], TsArrayLike]]`, default: `None` ) – optional function that fills in missing values (np.nan). Defaults to None.

Raises:

- `NotImplementedError` – Input arguments are not consistent.

Returns:

- `DataArray` – xr.DataArray: output xarray time series with at least a dimension "time"

Source code in `src/cinterop/timeseries.py`

```
def mk_hourly_xarray_series(
    data: Union[np.ndarray, TimeSeriesLike],
    start_date: ConvertibleToTimestamp,
    dim_name: Optional[str] = None,
    units: Optional[str] = None,
    colnames: Optional[List[str]] = None,
    fill_miss_func: Optional[Callable[[TsArrayLike], TsArrayLike]] = None,
) -> xr.DataArray:
    """Create an hourly xarray time series.

    Args:
        data (Union[np.ndarray, TimeSeriesLike]): Data from which to create the xarray series
        dim_name (str, optional): the name of the dimension for a multivariate series. Ignored if univariate. Defaults to None.
        units (str, optional): units in the time series. Defaults to None.
        colnames (Optional[List[str]], optional): names of the columns in a multivariate series. Defaults to None.
        fill_miss_func (Optional[Callable[[TsArrayLike], TsArrayLike]], optional): optional function that fills in missing values (np.nan). Defaults to None.

    Raises:
        NotImplementedError: Input arguments are not consistent.

    Returns:
        xr.DataArray: output xarray time series with at least a dimension "time"
    """
    _check_series_data(data, dim_name)
    n = data.shape[0]
    time_index = create_hourly_time_index(start_date, n)
    return mk_xarray_series(data, dim_name, units, time_index, colnames, fill_miss_func)
```

### mk_xarray_series

```
mk_xarray_series(
    data: Union[ndarray, TimeSeriesLike],
    dim_name: Optional[str] = None,
    units: Optional[str] = None,
    time_index: Optional[Union[List, DatetimeIndex]] = None,
    colnames: Optional[List[str]] = None,
    fill_miss_func: Optional[
        Callable[[TsArrayLike], TsArrayLike]
    ] = None,
) -> DataArray
```

Create an xarray time series.

Parameters:

- **`data`** (`Union[ndarray, TimeSeriesLike]`) – data from which to create the xarray series
- **`dim_name`** (`str`, default: `None` ) – the name of the dimension for a multivariate series. Ignored if univariate. Defaults to None.
- **`units`** (`str`, default: `None` ) – units in the time series. Defaults to None.
- **`time_index`** (`Optional[Union[List, DatetimeIndex]]`, default: `None` ) – the time index of the series. Optional if the input data already has a time index, such as a pandas series. Defaults to None.
- **`colnames`** (`Optional[List[str]]`, default: `None` ) – names of the columns in a multivariate series. Defaults to None.
- **`fill_miss_func`** (`Optional[Callable[[TsArrayLike], TsArrayLike]]`, default: `None` ) – optional function that fills in missing values (np.nan). Defaults to None.

Raises:

- `NotImplementedError` – Input arguments are not consistent.

Returns:

- `DataArray` – xr.DataArray: output xarray time series with at least a dimension "time"

Source code in `src/cinterop/timeseries.py`

```
def mk_xarray_series(
    data: Union[np.ndarray, TimeSeriesLike],
    dim_name: Optional[str] = None,
    units: Optional[str] = None,
    time_index: Optional[Union[List, pd.DatetimeIndex]] = None,
    colnames: Optional[List[str]] = None,
    fill_miss_func: Optional[Callable[[TsArrayLike], TsArrayLike]] = None,
) -> xr.DataArray:
    """Create an xarray time series.

    Args:
        data (Union[np.ndarray, TimeSeriesLike]): data from which to create the xarray series
        dim_name (str, optional): the name of the dimension for a multivariate series. Ignored if univariate. Defaults to None.
        units (str, optional): units in the time series. Defaults to None.
        time_index (Optional[Union[List, pd.DatetimeIndex]], optional): the time index of the series. Optional if the input data already has a time index, such as a pandas series. Defaults to None.
        colnames (Optional[List[str]], optional): names of the columns in a multivariate series. Defaults to None.
        fill_miss_func (Optional[Callable[[TsArrayLike], TsArrayLike]], optional): optional function that fills in missing values (np.nan). Defaults to None.

    Raises:
        NotImplementedError: Input arguments are not consistent.

    Returns:
        xr.DataArray: output xarray time series with at least a dimension "time"
    """
    if len(data.shape) > 2:  # noqa: PLR2004
        raise NotImplementedError("data must be at most of dimension 2")
    if len(data.shape) > 1 and dim_name is None:
        raise NotImplementedError(
            "data has more than one dimension, so the name of the second dimension 'dim_name' must be provided",
        )
    if time_index is None:
        if not isinstance(data, pd.Series):
            raise NotImplementedError(
                "if time_index is None data must be a pandas Series",
            )
        time_index = data.index
    if colnames is None and len(data.shape) > 1:
        if not isinstance(data, pd.Series):
            raise NotImplementedError(
                "if colnames is None and data of shape 2, data must be a pandas Series",
            )
        colnames = data.columns
    if fill_miss_func is not None:
        data = fill_miss_func(data)
    if len(data.shape) > 1:
        x = xr.DataArray(
            data,
            coords=[time_index, colnames],
            dims=[TIME_DIM_NAME, dim_name],
        )
    else:
        x = xr.DataArray(data, coords=[time_index], dims=[TIME_DIM_NAME])
    if units is not None:
        set_xr_units(x, units)
    return x
```

### pd_series_to_xr_series

```
pd_series_to_xr_series(series: Series) -> DataArray
```

Converts a pandas series to an xarray.

Source code in `src/cinterop/timeseries.py`

```
def pd_series_to_xr_series(series: pd.Series) -> xr.DataArray:
    """Converts a pandas series to an xarray."""
    if not isinstance(series, pd.Series):
        raise TypeError(f"Input must be a pandas Series, but got {type(series)}")
    return create_single_series(series.values, series.index)
```

### set_xr_units

```
set_xr_units(x: DataArray, units: str) -> None
```

Sets the units attribute of an xr.DataArray. No effect if x is not a dataarray.

Parameters:

- **`x`** (`DataArray`) – data array
- **`units`** (`str`) – units descriptor

Source code in `src/cinterop/timeseries.py`

```
def set_xr_units(x: xr.DataArray, units: str) -> None:
    """Sets the units attribute of an xr.DataArray. No effect if x is not a dataarray.

    Args:
        x (xr.DataArray): data array
        units (str): units descriptor
    """
    if units is None:
        return
    if isinstance(x, xr.DataArray):
        x.attrs[XR_UNITS_ATTRIB_ID] = units
```

### slice_pd_time_series

```
slice_pd_time_series(
    data: Series,
    from_date: ConvertibleToTimestamp = None,
    to_date: ConvertibleToTimestamp = None,
) -> Series
```

Subset a time series to a period.

Parameters:

- **`data`** (`Series`) – input xarray time series
- **`from_date`** (`ConvertibleToTimestamp`, default: `None` ) – date, convertible to a timestamp. Defaults to None.
- **`to_date`** (`ConvertibleToTimestamp`, default: `None` ) – end date of the slice. Inclusive. Defaults to None.

Returns:

- `Series` – pd.Series: a subset time series

Examples:

slice_pd_time_series(unaccounted_indus, from_date='1980-04-01', to_date='2000-04-01')

Source code in `src/cinterop/timeseries.py`

```
def slice_pd_time_series(
    data: pd.Series,
    from_date: ConvertibleToTimestamp = None,
    to_date: ConvertibleToTimestamp = None,
) -> pd.Series:
    """Subset a time series to a period.

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
```

### slice_xr_time_series

```
slice_xr_time_series(
    data: DataArray,
    from_date: ConvertibleToTimestamp = None,
    to_date: ConvertibleToTimestamp = None,
) -> DataArray
```

Subset a time series to a period.

Parameters:

- **`data`** (`DataArray`) – input xarray time series
- **`from_date`** (`ConvertibleToTimestamp`, default: `None` ) – date, convertible to a timestamp. Defaults to None.
- **`to_date`** (`ConvertibleToTimestamp`, default: `None` ) – end date of the slice. Inclusive. Defaults to None.

Returns:

- `DataArray` – xr.DataArray: a subset time series

Examples:

slice_xr_time_series(unaccounted_indus, from_date='1980-04-01', to_date='2000-04-01')

Source code in `src/cinterop/timeseries.py`

```
def slice_xr_time_series(
    data: xr.DataArray,
    from_date: ConvertibleToTimestamp = None,
    to_date: ConvertibleToTimestamp = None,
) -> xr.DataArray:
    """Subset a time series to a period.

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
```

### start_ts

```
start_ts(x: TimeSeriesLike) -> datetime64
```

Gets the starting date of a time series.

Parameters:

- **`x`** (`TimeSeriesLike`) – time series

Returns:

- **`Any`** ( `datetime64` ) – start of the series

Source code in `src/cinterop/timeseries.py`

```
def start_ts(x: TimeSeriesLike) -> np.datetime64:
    """Gets the starting date of a time series.

    Args:
        x (TimeSeriesLike): time series

    Returns:
        Any: start of the series
    """
    return __ts_index(x)[0]
```

### ts_window

```
ts_window(
    ts: TimeSeriesLike,
    from_date: ConvertibleToTimestamp = None,
    to_date: ConvertibleToTimestamp = None,
) -> TimeSeriesLike
```

Gets a temporal window of a time series.

Parameters:

- **`ts`** (`TimeSeriesLike`) – pandas dataframe, series, or xarray DataArray
- **`from_date`** (`ConvertibleToTimestamp`, default: `None` ) – start date of the window. Defaults to None.
- **`to_date`** (`ConvertibleToTimestamp`, default: `None` ) – end date of the window. Defaults to None.

Raises:

- `TypeError` – unhandled input time for ts

Returns:

- **`TimeSeriesLike`** ( `TimeSeriesLike` ) – Subset window of the full time series

Examples:

ts_window(unaccounted_indus, from_date='1980-04-01', to_date='2000-04-01')

Source code in `src/cinterop/timeseries.py`

```
def ts_window(
    ts: TimeSeriesLike,
    from_date: ConvertibleToTimestamp = None,
    to_date: ConvertibleToTimestamp = None,
) -> "TimeSeriesLike":
    """Gets a temporal window of a time series.

    Args:
        ts (TimeSeriesLike): pandas dataframe, series, or xarray DataArray
        from_date (ConvertibleToTimestamp, optional): start date of the window. Defaults to None.
        to_date (ConvertibleToTimestamp, optional): end date of the window. Defaults to None.

    Raises:
        TypeError: unhandled input time for `ts`

    Returns:
        TimeSeriesLike: Subset window of the full time series

    Examples:
        ts_window(unaccounted_indus, from_date='1980-04-01', to_date='2000-04-01')
    """
    if from_date is not None:
        from_date = as_timestamp(from_date)
    if to_date is not None:
        to_date = as_timestamp(to_date)
    if isinstance(ts, xr.DataArray):
        return slice_xr_time_series(ts, from_date, to_date)
    if isinstance(ts, (pd.Series, pd.DataFrame)):
        return slice_pd_time_series(ts, from_date, to_date)
    raise TypeError("Not supported: " + str(type(ts)))
```

### xr_ts_end

```
xr_ts_end(x: TimeSeriesLike) -> datetime64
```

Deprecated: use end_ts.

Source code in `src/cinterop/timeseries.py`

```
def xr_ts_end(x: TimeSeriesLike) -> np.datetime64:
    """Deprecated: use end_ts."""
    return end_ts(x)
```

### xr_ts_start

```
xr_ts_start(x: TimeSeriesLike) -> datetime64
```

Deprecated: use start_ts.

Source code in `src/cinterop/timeseries.py`

```
def xr_ts_start(x: TimeSeriesLike) -> np.datetime64:
    """Deprecated: use start_ts."""
    return start_ts(x)
```
