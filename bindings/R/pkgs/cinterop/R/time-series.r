createTsGeometry <- function(startTime, size, tStepSec, tStepCode=0L) {
  return(new('RegularTimeSeriesGeometry',
      Start=startTime, # POSIXct
      Length=size,
      TimeStepSeconds=tStepSec,
      TimeStepCode=tStepCode))
}

#' Convert an xts object to a cinterop RegularTimeSeries object to be passed to a C API
#'
#' Convert an xts object to a cinterop RegularTimeSeries object to be passed to a C API
#'
#' @param xts_mts the uni- or multi-variate xts time series
#' @import xts
#' @return an object of class "RegularTimeSeries"
#' @export
asInteropRegularTimeSeries <- function(xts_mts) {
  stopifnot(xts::is.xts(xts_mts))
  mts <- new("RegularTimeSeries", 
    TsGeom=getTsGeometry(xts_mts),
    EnsembleSize=ncol(xts_mts),
    NumericData=as.matrix(xts_mts)
  )
  return(mts)
}

#' Is the object a cinterop RegularTimeSeries object to be passed to a C API
#'
#' Is the object a cinterop RegularTimeSeries object to be passed to a C API
#'
#' @param tsInfo the object to test 
#' @export
isInteropRegularTimeSeries <- function(tsInfo) {
  return(is(tsInfo, "RegularTimeSeries"))
}

#' Convert an xts object to a cinterop RegularTimeSeries object to be passed to a C API
#'
#' Convert an xts object to a cinterop RegularTimeSeries object to be passed to a C API
#'
#' @param xts_mts the uni- or multi-variate xts time series
#' @import xts
#' @return an object of class "RegularTimeSeries"
#' @export
asXtsTimeSeries <- function(tsInfo) {
  stopifnot(isInteropRegularTimeSeries(tsInfo))
  if(tsInfo@EnsembleSize < 1) return(as.numeric(NA))
  xts::xts(tsInfo@NumericData, makeTimeAxis(tsInfo@TsGeom))
}


addMth <- function(n, d) {
  d %m+% lubridate::period(n, "month")
}

addMonths <- function(d, n) {
  stopifnot(is.POSIXct(d)) #brutal, but clear.
  if (length(n) == 1) {
    addMth(n, d)
  } else {
    dates <- sapply(n, addMth, d)
    tzattr <- tz(d)
    class(dates) <- c("POSIXct", "POSIXt")
    # do NOT use : tz(dates) <- tzattr
    attr(dates, "tzone") <- tzattr
    dates
  }
}

#' Creates a vector that can be used as a monthly time series index for an xts series
#'
#' Creates a vector that can be used as a monthly time series index for an xts series
#'
#' @param startDate a date object such as a POSIXct
#' @param n number of months
#' @import zoo
#' @import lubridate
#' @export
makeMonthlyTimeAxis <- function(startDate, n) {
  return(addMonths(startDate, 0:(n-1)))
}

#' Creates an R posixCT time axis for use in e.g. xts indexing
#'
#' Creates an R posixCT time axis for use in e.g. xts indexing
#'
#' @param tsGeom an S4 object of class 'RegularTimeSeriesGeometry'
#' @import xts
#' @import lubridate
#' @export
makeTimeAxis <- function(tsGeom) {
  stopifnot(is(tsGeom, "RegularTimeSeriesGeometry"))
  tStepCode <- tsGeom@TimeStepCode
  s <- tsGeom@Start
  if (tStepCode == 0L) {
    deltaT <- lubridate::seconds(tsGeom@TimeStepSeconds) 
    indices <- as.integer(0:(tsGeom@Length-1))
    return(s + indices * deltaT)
  } else if (tStepCode == 1L) { # monthly time step
    # NOTE: this is subject to change depending on requirements
    return(makeMonthlyTimeAxis(s, tsGeom@Length))
  }
}

#' Gets the time series geometry of an xts, to be passed to a C API
#'
#' Gets the time series geometry of an xts, to be passed to a C API
#'
#' @param xtseries the uni- or multi-variate xts time series
#' @import xts
#' @import stats
#' @import zoo
#' @import lubridate
#' @return an S4 object of class 'RegularTimeSeriesGeometry'
#' @export
getTsGeometry <- function(xtseries) {
  stopifnot(xts::is.xts(xtseries))
  tstamps <- zoo::index(xtseries[1:2,])
  a <- tstamps[1]
  b <- tstamps[2]
  firstDelta <- lubridate::as.duration(lubridate::as.interval(b-a, a))
  tStepCode <- 0L
  tStep <- as.integer(firstDelta)
  if (firstDelta > lubridate::ddays(27)){ # HACK: assume monthly
    tStepCode <- 1L
    tStep <- -1L
  }
  tsGeom <- createTsGeometry(startTime=a, size=nrow(xtseries), tStepSec=tStep, tStepCode=tStepCode)
  return(tsGeom)
}

