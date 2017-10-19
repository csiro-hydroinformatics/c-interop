#pragma once

// At most as of R-3.3.3 the filse \include\R_ext\RS.h has a section that seems to be 
// for backward compat with S. It defines a macro named 'Free', which can derail compilation when using Visual CPP. 
// We need to define STRICT_R_HEADERS to prevent this, before we include Rcpp.h

#define STRICT_R_HEADERS
#include <Rcpp.h>
