# Declares the S4 class that is used to hold references to external objects accessed via opaque, external pointers.
setClass('ExternalObjRef', slots = c(obj='externalptr', type='character'), prototype=list(obj=NULL, type=''))

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


