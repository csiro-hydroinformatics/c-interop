#' Create a wrapper around an externalptr
#'
#' Create a wrapper around an externalptr
#'
#' @param obj the object to wrap, if this is an externalptr
#' @param type a string character that identifies the underlying type of this object.
#' @return an ExternalObjRef if the input is an externalptr, or 'obj' otherwise.
#' @export
mkExternalObjRef <- function(obj, type='') {
  if(!is(obj, 'externalptr')) {
    return(obj)
  } else {
    return(new('ExternalObjRef', obj=obj, type=type))
  }
}

#' Gets an externalptr wrapped in an ExternalObjRef
#'
#' Gets an externalptr wrapped in an ExternalObjRef
#'
#' @param objRef the presumed ExternalObjRef to unwrap
#' @param stringent if TRUE, an error is raised if objRef is neither an  ExternalObjRef nor an externalptr.
#' @return an externalptr, or the input objRef unchanged if objRef is neither an  ExternalObjRef nor an externalptr and not in stringent mode
#' @export
getExternalXptr <- function(objRef, stringent=FALSE) {
  # 2016-01-28 allowing null pointers, to unlock behavior of EstimateERRISParameters. 
  # Reassess approach, even if other C API function will still catch the issue of null ptrs.
  if(is.null(objRef)) {
    return(NULL)
  }
  if (is(objRef, 'ExternalObjRef')) {
    return(objRef@obj)
  } else if (is(objRef, 'externalptr')) {
    return(objRef)
  } else {
    if(stringent) {
      stop('argument is neither a ExternalObjRef nor an external pointer')
    } else {
      return(objRef)
    }
  }
}

appendStartupMsg <- function(msg, prior) {
  return(paste0(prior, msg, '\n'))
}

#' @export
updatePathWindows <- function(envVarName='LIBRARY_PATH', libfilename='swift.dll') {
  startupMsg <- ''
  if(Sys.info()['sysname'] == 'Windows') 
  {
    pathSep <- ';'
    sharedLibPaths <- Sys.getenv(envVarName)
    if(sharedLibPaths!='') {
      startupMsg <- appendStartupMsg(paste0('Found env var ', envVarName, '=', sharedLibPaths), startupMsg)
      rarch <- Sys.getenv('R_ARCH')
      subfolder <- ifelse(rarch=='/x64', '64', '32')
      sharedLibPathsVec <- stringr::str_split(sharedLibPaths, pathSep)
      if(is.list(sharedLibPathsVec)) sharedLibPathsVec <- sharedLibPathsVec[[1]]
      priorPathEnv <- Sys.getenv('PATH')
      priorPaths <- stringr::str_split(priorPathEnv,pathSep)
      if(is.list(priorPaths)) priorPaths <- priorPaths[[1]]
      stopifnot(is.character(priorPaths))
      priorPaths <- tolower(priorPaths)
      newPaths <- priorPaths
      for(sharedLibPath in sharedLibPathsVec) {
        if(file.exists(sharedLibPath)) {
          fullpath <- base::normalizePath(file.path(sharedLibPath, subfolder))
          if(file.exists(fullpath)) {
            if(!(tolower(fullpath) %in% priorPaths)) {
              startupMsg <- appendStartupMsg(paste('Appending to the PATH env var:', fullpath), startupMsg)
              newPaths <- c(newPaths, fullpath)
            } else {
              startupMsg <- appendStartupMsg(paste('Path', fullpath, 'already found in PATH environment variable'), startupMsg)
            }
          }
        }
      }
      Sys.setenv(PATH=paste(newPaths, sep=pathSep, collapse=pathSep))
    }
    libfullname <- base::normalizePath(Sys.which(libfilename))
    if(libfullname==''){
      startupMsg <- appendStartupMsg(paste0('WARNING: Sys.which("',libfilename,'") did not return a file path'), startupMsg)
    } else {
      startupMsg <- appendStartupMsg(paste0('first ',libfilename,' shared library in PATH: ', libfullname), startupMsg)
    }
  }
  return(startupMsg)
}

#' @export
isExternalObjRef <- function(x, type) {
  result <- is(x, 'ExternalObjRef')
  if(result) {
    if(!missing(type)) {
      result <- (result && x@type == type)
    }
  }
  return(result)
}

#' @export
argErrorExternalObjType <- function(x, expectedType) {
  if(!isExternalObjRef(x)) {
    return(paste0('Expected type "', expectedType, '" but got object of type "', typeof(x), '" and class "', class(x), '"' ))
  } else {
    return(paste0('Expected ExternalObj type "', expectedType, '" but got ExternalObj type "', x@type))
  }
}

