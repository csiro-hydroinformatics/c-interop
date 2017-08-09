createTsGeometry <- function(startTime, size, tStepSec) {
  return(new('RegularTimeSeriesGeometry',
      Start=startTime, # POSIXct
      Length=size,
      TimeStepSeconds=tStepSec))
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
  xts::xts(tsInfo@NumericData, makeTimeAxis(tsInfo@TsGeom))
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
  deltaT <- lubridate::seconds(tsGeom@TimeStepSeconds) 
  indices <- as.integer(0:(tsGeom@Length-1))
  return(tsGeom@Start + indices * deltaT)
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
  tStep <- as.integer(lubridate::as.duration(lubridate::as.interval(b-a, a)))
  tsGeom <- createTsGeometry(startTime=stats::start(xtseries), size=nrow(xtseries), tStepSec=tStep)
  return(tsGeom)
}

