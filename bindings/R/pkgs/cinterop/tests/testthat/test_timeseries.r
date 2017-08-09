context("data")

# library(lubridate)
# library(cinterop)
# library(testthat)

test_that("conversion between xts and regulartimeseries", {
  d <- matrix(1:18, ncol=2)
  x <- xts::xts(d, lubridate::origin + lubridate::days(0:8))
  y <- asInteropRegularTimeSeries(x)
  geom <- y@TsGeom
  expect_equal(2, y@EnsembleSize)
  expect_equal(86400, geom@TimeStepSeconds)
  expect_equal(9, geom@Length)
  expect_true(all(d == y@NumericData))

  hourlyAxis <- lubridate::origin + lubridate::hours(0:8)
  x <- xts::xts(d, hourlyAxis)
  y <- asInteropRegularTimeSeries(x)
  geom <- y@TsGeom
  expect_equal(3600, geom@TimeStepSeconds)

  x <- asXtsTimeSeries(y)
  expect_equal(2, ncol(x))
  expect_true(all(hourlyAxis == xts:::index.xts(x)))
  expect_equal(9, nrow(x))
  expect_true(all(d == x))

})
