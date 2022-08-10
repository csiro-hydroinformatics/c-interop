import xarray as xr
import pandas as pd
import numpy as np
from datetime import datetime

from typing import Any, Union, List, Optional, Callable

TIME_DIM_NAME = "time"

XR_UNITS_ATTRIB_ID: str = "units"
"""key for the units attribute on xarray DataArray objects"""

TimeSeriesLike = Union[pd.Series, pd.DataFrame, xr.DataArray]
"""types that can represent time series 
"""

ConvertibleToTimestamp = Union[str, datetime, np.datetime64, pd.Timestamp]
"""types that can be converted with relative unambiguity to a pandas Timestamp 
"""


def create_even_time_index(start:ConvertibleToTimestamp, time_step_seconds:int, n:int) -> List:
    start = as_timestamp(start)
    delta_t = np.timedelta64(time_step_seconds, 's')
    return [start + delta_t * i for i in range(n)]

def create_daily_time_index(start:ConvertibleToTimestamp, n:int) -> List:
    return create_even_time_index(start, 86400, n)

def create_hourly_time_index(start:ConvertibleToTimestamp, n:int) -> List:
    return create_even_time_index(start, 3600, n)

def create_monthly_time_index(start:ConvertibleToTimestamp, n:int) -> List:
    start = as_timestamp(start)
    return [start + pd.tseries.offsets.DateOffset(months=i) for i in range(n)]


def _is_convertible_to_timestamp(t: Any):
    return isinstance(t, str) or isinstance(t, datetime) or isinstance(t, np.datetime64) or isinstance(t, pd.Timestamp)

def as_timestamp(t: ConvertibleToTimestamp, tz=None) -> pd.Timestamp:
    # work around a breaking change in pandas 1.x: "Expected unicode, got numpy.str_'
    if isinstance(t, str):
        t = str(t)
    if _is_convertible_to_timestamp(t):
        if isinstance(t, pd.Timestamp):
            if tz is None:
                return t
            elif t.tz is None:
                return pd.Timestamp(t, tz=tz)
            elif str(t.tz) == str(tz):
                return t
            else:
                raise ValueError("Not supported - Cannot pass a datetime or Timestamp with tzinfo with the tz parameter. Use tz_convert instead")
        return pd.Timestamp(t, tz=tz)
    else:
        raise TypeError(
            "Cannot convert to a timestamp the object of type" + str(type(t)))


def as_pydatetime(t: ConvertibleToTimestamp, tz=None) -> datetime:
    return as_timestamp(t, tz=tz).to_pydatetime()

def mk_xarray_series(
    data: Union[np.ndarray,TimeSeriesLike],
    dim_name: str = None,
    units: str = None,
    time_index: Optional[Union[List, pd.DatetimeIndex]] = None,
    colnames: Optional[List[str]] = None,
    fill_miss_func: Optional[Callable] = None,
) -> xr.DataArray:
    if len(data.shape) > 2:
        raise NotImplementedError("data must be at most of dimension 2")
    if len(data.shape) > 1 and dim_name is None:
        raise NotImplementedError(
            "data has more than one dimension, so the name of the second dimension 'dim_name' must be provided"
        )
    if time_index is None:
        if not isinstance(data, pd.Series):
            raise NotImplementedError(
                "if time_index is None data must be a pandas Series"
            )
        else:
            time_index = data.index
    if colnames is None and len(data.shape) > 1:
        if not isinstance(data, pd.Series):
            raise NotImplementedError(
                "if colnames is None and data of shape 2, data must be a pandas Series"
            )
        else:
            colnames = data.columns
    if fill_miss_func is not None:
        data = fill_miss_func(data)
    if len(data.shape) > 1:
        x = xr.DataArray(
            data, coords=[time_index, colnames], dims=[TIME_DIM_NAME, dim_name]
        )
    else:
        x = xr.DataArray(data, coords=[time_index], dims=[TIME_DIM_NAME])
    if units is not None:
        set_xr_units(x, units)
    return x


def mk_daily_xarray_series(
    data: Union[np.ndarray,TimeSeriesLike],
    start_date: ConvertibleToTimestamp,
    dim_name: str = None,
    units: str = None,
    colnames: Optional[List[str]] = None,
    fill_miss_func: Optional[Callable] = None,
) -> xr.DataArray:
    if len(data.shape) > 2:
        raise NotImplementedError("data must be at most of dimension 2")
    if len(data.shape) > 1 and dim_name is None:
        raise NotImplementedError(
            "data has more than one dimension, so the name of the second dimension 'dim_name' must be provided"
        )
    n = data.shape[0]
    time_index = create_daily_time_index(start_date, n)
    return mk_xarray_series( data, dim_name, units, time_index, colnames, fill_miss_func)

def mk_hourly_xarray_series(
    data: Union[np.ndarray,TimeSeriesLike],
    start_date: ConvertibleToTimestamp,
    dim_name: str = None,
    units: str = None,
    colnames: Optional[List[str]] = None,
    fill_miss_func: Optional[Callable] = None,
) -> xr.DataArray:
    if len(data.shape) > 2:
        raise NotImplementedError("data must be at most of dimension 2")
    if len(data.shape) > 1 and dim_name is None:
        raise NotImplementedError(
            "data has more than one dimension, so the name of the second dimension 'dim_name' must be provided"
        )
    n = data.shape[0]
    time_index = create_hourly_time_index(start_date, n)
    return mk_xarray_series( data, dim_name, units, time_index, colnames, fill_miss_func)

def set_xr_units(x: xr.DataArray, units: str):
    """Sets the units attribute of an xr.DataArray. No effect if x is not a dataarray

    Args:
        x (xr.DataArray): data array
        units (str): units descriptor
    """
    if units is None:
        return
    if isinstance(x, xr.DataArray):
        x.attrs[XR_UNITS_ATTRIB_ID] = units

