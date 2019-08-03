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
    TimeStepSeconds='integer')
)

createDefaultTsGeometry <- function() {
  return(new('RegularTimeSeriesGeometry',
    Start=lubridate::origin,
    Length=0L,
    TimeStepSeconds=3600L))
}

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
    NumericData='matrix')
)

# 2019-08 Had to move away from using the `prototype` argument in setClass. See 
# https://github.com/csiro-hydroinformatics/rcpp-interop-commons/issues/4
# for context.
# Very non-plussed by R reference classes.

setMethod("initialize", "RegularTimeSeriesGeometry", 
    function(.Object, ...) {
      .Object <- callNextMethod()
      .Object
    })

setMethod("initialize", "RegularTimeSeries",
          function(.Object, tsGeom = createDefaultTsGeometry(), ensSize = 0L, numericData = as.matrix(numeric()), ...) {
              .Object <- callNextMethod(.Object, ...)
              .Object@TsGeom <- tsGeom
              .Object@EnsembleSize <- ensSize
              .Object@NumericData <- numericData
              .Object
          })
