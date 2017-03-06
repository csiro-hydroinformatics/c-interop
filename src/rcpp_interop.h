#pragma once

#include <Rcpp.h>
using namespace Rcpp;

#include "common_c_interop.h"
#include "c_interop_forward_decl.h"

char** to_ansi_char_array(CharacterVector charVec);
void free_ansi_char_array(char ** values, int arrayLength);
double** as_double_ptr_array(NumericMatrix& mat);
double** to_double_ptr_array(const NumericMatrix& mat);
void free_double_ptr_array(double** values, int arrayLength);

CharacterVector to_r_character_vector(char** names, int size, bool cleanup = true);
NumericVector to_r_numeric_vector(double* values, int length, bool cleanup = false);

//MarshaledDateTime toDateTimeStruct(const Datetime& dt);
//Datetime toDateTime(const MarshaledDateTime& mdt);
//MarshaledTsGeometry* toMarshalledTsinfoPtr(const Rcpp::S4& rTsInfo);

//MarshaledTsGeometry toMarshalledTsinfo(const Rcpp::S4& rTsInfo);
//MultiTimeSeriesData toMultiTimeSeriesData(const Rcpp::S4& timeSeriesEnsemble);
//void PkgDisposeMultiTimeSeriesData(MultiTimeSeriesData& d);
//
//
//SceParameters toSceParameters(const NumericVector& sceParams);
//
