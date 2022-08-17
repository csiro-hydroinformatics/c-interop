from multiprocessing.sharedctypes import Value
import xarray as xr
import pandas as pd
import numpy as np
from datetime import datetime

from typing import Any, Union, List, Optional, Callable

TIME_DIM_NAME = "time"
TIME_DIMNAME = "time"
ENSEMBLE_DIMNAME = "ensemble"

XR_UNITS_ATTRIB_ID: str = "units"
"""key for the units attribute on xarray DataArray objects"""

TimeSeriesLike = Union[pd.Series, pd.DataFrame, xr.DataArray]
"""types that can represent time series 
"""

ConvertibleToTimestamp = Union[str, datetime, np.datetime64, pd.Timestamp]
"""types that can be converted with relative unambiguity to a pandas Timestamp 
"""


def create_even_time_index(
    start: ConvertibleToTimestamp, time_step_seconds: int, n: int
) -> pd.DatetimeIndex:
    """Creates a regular, evenly spaces time index

    Args:
        start (ConvertibleToTimestamp): first datetime in the time index
        time_step_seconds (int): time step length in seconds
        n (int): length of the index

    Returns:
        pd.DatetimeIndex: a time index suitable for a time series.
    """
    if time_step_seconds == 3600:
        return create_hourly_time_index(start, n)
    elif time_step_seconds == 86400:
        return create_daily_time_index(start, n)
    else:
        start = as_datetime64(start)
        delta_t = np.timedelta64(time_step_seconds, "s")
        # Note: below appears to be a few times faster than pd.date_range with a freq=Dateoffset for some reasons.
        return pd.DatetimeIndex([start + delta_t * i for i in range(n)])


def create_daily_time_index(start: ConvertibleToTimestamp, n: int) -> pd.DatetimeIndex:
    """Creates a daily time index

    Args:
        start (ConvertibleToTimestamp): first datetime in the time index
        n (int): length of the index

    Returns:
        pd.DatetimeIndex: a time index suitable for a time series.
    """    
    start = as_datetime64(start)
    return pd.date_range(
        start, periods=n, freq="D"
    )  # much faster than list comprehension, see https://jmp75.github.io/work-blog/c++/python/performance/runtime/2022/08/09/python-profiling-interop.html


def create_hourly_time_index(start: ConvertibleToTimestamp, n: int) -> pd.DatetimeIndex:
    """Creates an hourly time index

    Args:
        start (ConvertibleToTimestamp): first datetime in the time index
        n (int): length of the index

    Returns:
        pd.DatetimeIndex: a time index suitable for a time series.
    """
    start = as_datetime64(start)
    return pd.date_range(
        start, periods=n, freq="H"
    )  # much faster than list comprehension


def create_monthly_time_index(
    start: ConvertibleToTimestamp, n: int
) -> pd.DatetimeIndex:
    """Creates a monthly time index

    Args:
        start (ConvertibleToTimestamp): first datetime in the time index
        n (int): length of the index

    Raises:
        ValueError: day of month of the start date is more than 28

    Returns:
        pd.DatetimeIndex: a time index suitable for a time series.
    """
    pdstart = as_timestamp(start)
    if pdstart.day > 28:
        raise ValueError("Monthly time indices require a day of month less than 29. End of months indices are not yet supported.")
    start = as_datetime64(start)
    return pd.date_range(start, periods=n, freq=pd.tseries.offsets.DateOffset(months=1))


def _is_convertible_to_timestamp(t: Any) -> bool:
    return (
        isinstance(t, str)
        or isinstance(t, datetime)
        or isinstance(t, np.datetime64)
        or isinstance(t, pd.Timestamp)
    )


def as_timestamp(t: ConvertibleToTimestamp) -> pd.Timestamp:
    """Converts, if possible, a value to a pandas `Timestamp`

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
    tz = None

    if _is_convertible_to_timestamp(t):
        if isinstance(t, pd.Timestamp):
            if t.tz is not None:
                raise ValueError(
                    "Not supported - Cannot pass a datetime or Timestamp with tzinfo with the tz parameter. Use tz_convert instead"
                )
            else:
                return t
        elif isinstance(t, datetime):
            if t.tzinfo is not None:
                raise ValueError(
                    "Not supported - Cannot pass a datetime or Timestamp with tzinfo with the tz parameter. Use tz_convert instead"
                )
        parsed = pd.Timestamp(t)
        if parsed.tz is not None:
            raise ValueError("To avoid ambiguities time zones are not supported. All date times must be 'naive'")
        else:
            return parsed
    else:
        raise TypeError(
            "Cannot convert to a timestamp the object of type" + str(type(t))
        )


def as_datetime64(t: ConvertibleToTimestamp) -> np.datetime64:
    """Convert, if possible, to a numpy datetime64

    Args:
        t (ConvertibleToTimestamp): date time value to convert

    Raises:
        ValueError: input value is not supported, notably values with time zone informations are excluded
        TypeError: unexpected input type

    Returns:
        np.datetime64: value as a datetime64
    """
    return as_timestamp(t).to_datetime64()


def as_pydatetime(t: ConvertibleToTimestamp) -> datetime:
    """Convert, if possible, to a datetime

    Args:
        t (ConvertibleToTimestamp): date time value to convert

    Raises:
        ValueError: input value is not supported, notably values with time zone informations are excluded
        TypeError: unexpected input type

    Returns:
        datetime: value as a datetime
    """
    return as_timestamp(t).to_pydatetime()


def mk_xarray_series(
    data: Union[np.ndarray, TimeSeriesLike],
    dim_name: str = None,
    units: str = None,
    time_index: Optional[Union[List, pd.DatetimeIndex]] = None,
    colnames: Optional[List[str]] = None,
    fill_miss_func: Optional[Callable] = None,
) -> xr.DataArray:
    """TODO mk_xarray_series"""
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
    data: Union[np.ndarray, TimeSeriesLike],
    start_date: ConvertibleToTimestamp,
    dim_name: str = None,
    units: str = None,
    colnames: Optional[List[str]] = None,
    fill_miss_func: Optional[Callable] = None,
) -> xr.DataArray:
    """TODO mk_daily_xarray_series"""
    if len(data.shape) > 2:
        raise NotImplementedError("data must be at most of dimension 2")
    if len(data.shape) > 1 and dim_name is None:
        raise NotImplementedError(
            "data has more than one dimension, so the name of the second dimension 'dim_name' must be provided"
        )
    n = data.shape[0]
    time_index = create_daily_time_index(start_date, n)
    return mk_xarray_series(data, dim_name, units, time_index, colnames, fill_miss_func)


def mk_hourly_xarray_series(
    data: Union[np.ndarray, TimeSeriesLike],
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
    return mk_xarray_series(data, dim_name, units, time_index, colnames, fill_miss_func)


def set_xr_units(x: xr.DataArray, units: str) -> None:
    """Sets the units attribute of an xr.DataArray. No effect if x is not a dataarray

    Args:
        x (xr.DataArray): data array
        units (str): units descriptor
    """
    if units is None:
        return
    if isinstance(x, xr.DataArray):
        x.attrs[XR_UNITS_ATTRIB_ID] = units


def create_ensemble_series(
    npx: np.ndarray, ens_index: List, time_index: Union[List, pd.DatetimeIndex]
) -> xr.DataArray:
    """Create an ensemble (i.e. special type of multi-variate) time series"""
    return xr.DataArray(
        npx, coords=[ens_index, time_index], dims=[ENSEMBLE_DIMNAME, TIME_DIMNAME]
    )


def create_single_series(
    npx: np.ndarray, time_index: Union[List, pd.DatetimeIndex]
) -> xr.DataArray:
    """Create an uni-variate time series"""
    npx = npx.squeeze()
    assert len(npx.shape) == 1
    return xr.DataArray(npx, coords=[time_index], dims=[TIME_DIMNAME])


def pd_series_to_xr_series(series: pd.Series) -> xr.DataArray:
    """Converts a pandas series to an xarray"""
    assert isinstance(series, pd.Series)
    return create_single_series(series.values, series.index)


def _pd_index(x:TimeSeriesLike) -> pd.DatetimeIndex:
    if not isinstance(x.index, pd.DatetimeIndex):
        raise TypeError("pandas structure; but the index is not an DatetimeIndex")
    return x.index


def __ts_index(x: TimeSeriesLike) -> pd.DatetimeIndex:
    if isinstance(x, pd.Series) or isinstance(x, pd.DataFrame):
        return _pd_index(x)
    elif isinstance(x, xr.DataArray):
        return x.coords[TIME_DIMNAME].values
    else:
        raise TypeError(
            "Not supported as a representation of a time series: " + str(type(x))
        )


def start_ts(x: TimeSeriesLike) -> np.datetime64:
    """Gets the starting date of a time series

    Args:
        x (TimeSeriesLike): time series

    Returns:
        Any: start of the series
    """
    return __ts_index(x)[0]


def end_ts(x: TimeSeriesLike) -> np.datetime64:
    """Gets the ending date of a time series

    Args:
        x (TimeSeriesLike): time series

    Returns:
        Any: end of the series
    """
    return __ts_index(x)[-1]


# TODO: legacy, I think.
def xr_ts_start(x:TimeSeriesLike) -> np.datetime64:
    """Deprecated: use start_ts"""
    return start_ts(x)

def xr_ts_end(x:TimeSeriesLike) -> np.datetime64:
    """Deprecated: use end_ts"""
    return end_ts(x)

def _time_interval_indx(
    dt: np.ndarray,
    from_date: ConvertibleToTimestamp = None,
    to_date: ConvertibleToTimestamp = None,
) -> np.ndarray:
    tt = np.empty_like(dt, bool)
    tt[:] = True
    if from_date is not None:
        tt = np.logical_and(tt, (dt >= as_datetime64(from_date)))
    if to_date is not None:
        tt = np.logical_and(tt, (dt <= as_datetime64(to_date)))
    return tt


def slice_xr_time_series(
    data: xr.DataArray,
    from_date: ConvertibleToTimestamp = None,
    to_date: ConvertibleToTimestamp = None,
) -> xr.DataArray:
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


def slice_pd_time_series(
    data: pd.Series,
    from_date: ConvertibleToTimestamp = None,
    to_date: ConvertibleToTimestamp = None,
) -> pd.Series:
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


def ts_window(
    ts: TimeSeriesLike,
    from_date: ConvertibleToTimestamp = None,
    to_date: ConvertibleToTimestamp = None,
) -> "TimeSeriesLike":
    """Gets a temporal window of a time series

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
    if isinstance(ts, xr.DataArray):
        return slice_xr_time_series(ts, from_date, to_date)
    elif isinstance(ts, pd.Series) or isinstance(ts, pd.DataFrame):
        return slice_pd_time_series(ts, from_date, to_date)
    else:
        raise TypeError("Not supported: " + str(type(ts)))
