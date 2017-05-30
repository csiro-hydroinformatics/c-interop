#' Class ExternalObjRef.
#'
#' Class \code{ExternalObjRef} defines a class that is used to hold references to external objects accessed via opaque, external pointers.
#'
#' @name ExternalObjRef-class
#' @rdname ExternalObjRef-class
#' @exportClass ExternalObjRef
setClass('ExternalObjRef', slots = c(obj='externalptr', type='character'), prototype=list(obj=NULL, type=''))

#' Class RegularTimeSeriesGeometry.
#'
#' Class \code{RegularTimeSeriesGeometry} defines a class defining the geometry of time series with a time step identical for every step.
#'
#' @name RegularTimeSeriesGeometry-class
#' @rdname RegularTimeSeriesGeometry-class
#' @exportClass RegularTimeSeriesGeometry
setClass('RegularTimeSeriesGeometry', 
  slots = c(
    Start='POSIXct',
    Length='integer',
    TimeStepSeconds='integer'), 
  prototype=c(
    Start=lubridate::origin,
    Length=0,
    TimeStepSeconds=3600)
)
  
#' Class RegularTimeSeries.
#'
#' Class \code{RegularTimeSeries} is a simplified structure for multivariate regular series, readier for interop with a C API.
#'
#' @name RegularTimeSeries-class
#' @rdname RegularTimeSeries-class
#' @exportClass RegularTimeSeries
setClass('RegularTimeSeries', 
  slots = c(
    TsGeom='RegularTimeSeriesGeometry',
    EnsembleSize='integer',
    NumericData='matrix'), 
  prototype=c(
    TsGeom=new('RegularTimeSeriesGeometry'),
    EnsembleSize=0,
    NumericData=as.matrix(numeric()))
)


