# library(roxygen2) ; roxygenize('F:/src/path/to/cinterop')

#' Reusable constructs for interop with opaque pointers in a C API
#' 
#' \tabular{ll}{
#' Package: \tab cinterop \cr
#' Type: \tab Package\cr
#' Version: \tab 1.0 \cr
#' Date: \tab 2020-06-10 \cr
#' Release Notes: \tab Adding C interop code for the definition of multi-objective multi-site optimisation\cr
#' License: \tab BSD-3 \cr
#' }
#'
#' \tabular{lll}{
#' Version \tab Date \tab Notes \cr
#' 0.3.0 \tab 2019-08-03 \tab Fixes to the R cinterop package, required by R 3.6+ which has likely broken the `prototype` argument in setClass. Issue #4: https://github.com/csiro-hydroinformatics/rcpp-interop-commons/issues/4 \cr
#' 0.2.5 \tab 2017-12-22 \tab Expand features relating to interop of time series includint xts in the R package cinterop \cr
#' 0.2.4 \tab 2017-08-09 \tab Add unit tests and additional time series conversions for dependent packages \cr
#' }
#'
#' @name cinterop-package
#' @aliases cinterop
#' @docType package
#' @title Reusable constructs for interop with opaque pointers in a C API
#' @author Jean-Michel Perraud \email{jean-michel.perraud_at_csiro.au}
#' @keywords C, external pointers
NULL
