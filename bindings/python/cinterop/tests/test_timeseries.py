import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd
import pytest
from cinterop.timeseries import (
    as_datetime64,
    as_timestamp,
    create_even_time_index,
    end_ts,
    mk_daily_xarray_series,
    start_ts,
    ts_window,
)

pkg_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, pkg_dir)


def test_ts_window():
    d = as_datetime64(datetime(2000, 1, 1))
    d_mid = as_datetime64(datetime(2000, 1, 13))
    end_date = as_datetime64(datetime(2000, 1, 31))
    x = np.arange(31)
    ts = mk_daily_xarray_series(x, d)

    sseries = [ts, ts.to_series(), ts.to_dataframe(name="test")]

    for s in sseries:
        sts = ts_window(s, from_date=None, to_date=None)
        assert sts.squeeze().values.shape == (31,)
        assert start_ts(sts) == d
        assert end_ts(sts) == end_date

        sts = ts_window(s, from_date=d_mid, to_date=None)
        assert sts.squeeze().values.shape == (31 - 13 + 1,)
        assert start_ts(sts) == d_mid
        assert end_ts(sts) == end_date

        sts = ts_window(s, from_date=None, to_date=d_mid)
        assert sts.squeeze().values.shape == (13,)
        assert start_ts(sts) == d
        assert end_ts(sts) == d_mid


def test_create_even_time_index():
    n = 7
    d = as_datetime64(datetime(2000, 1, 2, 3, 4, 5))
    tindx = create_even_time_index(d, 3600, n)
    assert tindx[0] == d
    assert len(tindx) == n
    assert tindx[n - 1] == as_datetime64(datetime(2000, 1, 2, (3 + n - 1), 4, 5))
    tindx = create_even_time_index(d, 86400, n)
    assert tindx[0] == d
    assert len(tindx) == n
    assert tindx[n - 1] == as_datetime64(datetime(2000, 1, (2 + n - 1), 3, 4, 5))

    tindx = create_even_time_index(d, 3, n)
    assert tindx[0] == d
    assert len(tindx) == n
    assert tindx[n - 1] == as_datetime64(datetime(2000, 1, 2, 3, 4, (5 + 3 * (n - 1))))


def test_as_timestamp():
    import pytz

    d = datetime(2000, 1, 2, 3, 4, 5)
    expected = pd.Timestamp(datetime(2000, 1, 2, 3, 4, 5))
    assert as_timestamp("2000-01-02 03:04:05") == expected
    assert as_timestamp(d) == expected
    assert as_timestamp(np.datetime64(d)) == expected

    test_tz = "HST"  # https://www.timeanddate.com/time/zone/usa/hawaii

    tzinfo = pytz.timezone(test_tz)
    d = datetime(2000, 1, 2, 3, 4, 5, tzinfo=tzinfo)
    with pytest.raises(ValueError):
        as_timestamp("2000-01-02 03:04:05 -10:00")
    with pytest.raises(ValueError):
        as_timestamp(pd.Timestamp("2000-01-02 03:04:05", tz=tzinfo))
    with pytest.raises(ValueError):
        as_timestamp(d)
    # Below was an attempt, but somewhat misguided; All np.datetime64 are naive, but will parse some time offsets (though deprecation looming)
    # Not worth testing against here, more confusing than helpful
    # with pytest.raises(ValueError):
    #     as_timestamp(np.datetime64("2000-01-02 03:04:05-10:00"))
    with pytest.raises(TypeError):
        as_timestamp(b"2000-01-02 03:04:05 -10:00")


if __name__ == "__main__":
    test_as_timestamp()
