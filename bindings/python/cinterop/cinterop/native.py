
from cffi import FFI

class NativeHandle(object):
    ''' NativeHandle  A base class for wrappers around objects in native libraries for easier memory management. 

    Say you have a C API as follows:
    * `void* create_some_object();`
    * `dispose_of_some_object(void* obj);`
    and accessing it using Python and CFFI. Users would use the `calllib` function:
    aLibPointer = callib('mylib', 'create_some_object');
    but at some point when done need to dispose of it:
    callib('mylib', 'dispose_of_some_object', aLibPointer);
    In practice in real systems one quickly ends up with cases 
    where it is unclear when to dispose of the object. 
    If you call the `dispose_of_some_object` function more 
    than once of too soon, you could easily crash the program.
    NativeHandle is designed to alleviate this headache by 
    using Matlab native reference counting of `handle` classes to reliably dispose of objects. 

    This class is originally inspired from a class with a similar purpose in C#. See https://github.com/jmp75/dynamic-interop-dll

    '''

    """ a global function that can be called to release an external pointer """
    release_callback = None

    """ Thin wrapper around a native pointer (cffi object) """
    def __init__(self, ptr, type_id='', starting_ref_count = 0):
        # TODO checks on ptr
        self._type_id = type_id
        self._finalizing = False
        self._handle = None
        self._ref_count = 0
        # if release_callback is None:
        #     self._release_callback = NativeHandle.release_callback
        # else:
        #     self._release_callback = release_callback
        if ptr is None:
            return # defer setting handle to the inheritor.
        self._set_handle(ptr, starting_ref_count)

    def __is_valid_handle(self, h):
        # __is_valid_handle - Test whether an argument is a valid handle (lib.pointer) for this object.
        # Returns a logical.
        # Parameters:
        #   h:
        # The handle, value of the pointer to the native object
        return isinstance(h, FFI.CData)

    def __dispose_impl(self, decrement):
        # __dispose_impl - An implementation of the dispose method, to 
        # avoid cyclic method calls.
        # 
        # Parameters:
        # decrement - logical indicating whether the reference count should be decreased.
        if self.disposed:
            return
        if decrement:
            self._ref_count = self._ref_count - 1
        if self._ref_count <= 0:
            if self._release_handle():
                self._handle = None
                # if (!_finalizing)
                # GC.SuppressFinalize(this)

    # reference_count - The number of references to the underlying object (Not the wrapper).
    # In practice this would almost always be 0 or 1 and users should not need to take use this. 
    @property
    def reference_count(self):
        return self._ref_count
         
    # disposed - logical; has the native object and memory already been disposed of.        
    @property
    def disposed(self):
        return self._handle is None

    # is_invalid - logical; in practice synonym with disposed; 
    # has the native object and memory already been disposed of.        
    @property
    def is_invalid(self):
        return self._handle is None

    def _release_handle(self):
        # See also https://stackoverflow.com/questions/4714136/how-to-implement-virtual-methods-in-python
        # May want to make this abstract using ABC - we'll see.
        raise NotImplementedError()

    def _set_handle(self, pointer, currentRefCount=0):
        # _set_handle - Sets a handle.
        #
        # Parameters:
        #   pointer:
        # The handle (lib.pointer), value of the pointer to the native object
        #
        #   currentRefCount:
        # (Optional) Number of pre-existing references for 
        # the native object. Almost always 0 except in unusual, advanced situations.
        #
        # Exceptions:
        # error message when a pointer is a Zero pointer .
        #
        # Remarks:
        # If a native object was created prior to its use by Matlab, its lifetime may need
        # to extend beyong its use from Matlab, hence the provision for an initial reference 
        # count more than 0. In practice the scenario is very unusual.
        if not self.__is_valid_handle(pointer):
            raise Error('The lib.pointer argument is not a valid handle')
        self._handle = pointer
        self._ref_count = currentRefCount + 1

    @property
    def ptr(self):
        """ Return the pointer to a cffi object """
        return self._handle

    @property
    def type_id(self):
        """ Return the optional type identifier for the underlying native type """
        return self._type_id


    @ptr.setter
    def ptr(self, value):
        """ Set the pointer to the cffi object """
        self._handle = value

    @property
    def obj(self):
        """ Return the native object pointed to (cffi object) """
        return self._handle[0]

    def __str__(self):
        return 'Handle to a native pointer of type id "' + self.type_id + '"'

    def __repr__(self):
        return str(self)

    def __del__(self):
        if not self._handle is None:
            # if not self._release_callback is None:
            # Protect against accessing properties
            # of partially constructed objects (May not be an issue in Python?)
            self._finalizing = True
            self.release()

    def add_ref(self):
        # add_ref - Manually increments the reference counter.
        # This is very unusual you would need to call this method. 
        self._ref_count = self._ref_count + 1

    def dispose(self):
        # dispose - If the reference counts allows it, release the resource refered to by this handle.
        self.__dispose_impl(True)

    def get_handle(self):
        # get_handle = Returns the value of the handle.
        #
        # Returns:
        # The handle (lib.pointer)
        return self._handle

    def release(self):
        # release - Manually decrements the reference counter. Triggers disposal if count 
        # is down to zero.
        self.__dispose_impl(True)



#' Create a wrapper around an externalptr
#'
#' Create a wrapper around an externalptr
#'
#' @param obj the object to wrap, if this is an externalptr
#' @param type_id a string character that identifies the underlying type of this object.
#' @return an ExternalObjRef if the input is an externalptr, or 'obj' otherwise.
#' @export
def wrap_native_handle (obj, type_id='', release_callback = None, owner=True):
    if isinstance(obj, FFI.CData):
        return NativeHandle(obj, type_id=type_id, release_callback=release_callback, owner=owner) 
    else:
        return obj  


#' Gets an externalptr wrapped in an ExternalObjRef
#'
#' Gets an externalptr wrapped in an ExternalObjRef
#'
#' @param objRef the presumed ExternalObjRef to unwrap
#' @param stringent if TRUE, an error is raised if objRef is neither an  ExternalObjRef nor an externalptr.
#' @return an externalptr, or the input objRef unchanged if objRef is neither an  ExternalObjRef nor an externalptr and not in stringent mode
#' @import methods
#' @export
def unwrap_native_handle (objRef, stringent=False):
    # 2016-01-28 allowing null pointers, to unlock behavior of EstimateERRISParameters. 
    # Reassess approach, even if other C API function will still catch the issue of null ptrs.
    if objRef is None:
        return None  
    if isinstance(objRef, NativeHandle):
        return objRef.obj
    if isinstance(obj, FFI.CData):
        return obj
    else:
        if stringent:
            raise Error('argument is neither a NativeHandle nor a CFFI external pointer')
        else:
            return objRef


#' Update the PATH env var on windows, to locate an appropriate DLL dependency.
#' 
#' Update the PATH env var on windows. This is a function meant to be used by packages' '.onLoad' functions. 
#' Looks in another env var, then depending on whether the current process is 32 or 64 bits build a path and looks for a specified DLL. 
#' 
#' @param envVarName the environment variable to look for a root for architecture dependent libraries. 
#' @param libfilename name of the DLL sought and that should be present in the architecture (32/64) subfolder.
#' @import stringr
#' @return a character vector, the startup message string resulting from the update process.
#' @export
# updatePathWindows (envVarName='LIBRARY_PATH', libfilename='mylib.dll'):
#   startupMsg <- ''
#   if(Sys.info()['sysname'] == 'Windows') 
  
#     pathSep <- ';'
#     sharedLibPaths <- Sys.getenv(envVarName)
#     if(sharedLibPaths!=''):
#       startupMsg <- appendStartupMsg(paste0('Found env var ', envVarName, '=', sharedLibPaths), startupMsg)
#       rarch <- Sys.getenv('R_ARCH')
#       subfolder <- ifelse(rarch=='/x64', '64', '32')
#       sharedLibPathsVec <- stringr::str_split(sharedLibPaths, pathSep)
#       if(is.list(sharedLibPathsVec)) sharedLibPathsVec <- sharedLibPathsVec[[1]]
#       priorPathEnv <- Sys.getenv('PATH')
#       priorPaths <- stringr::str_split(priorPathEnv,pathSep)
#       if(is.list(priorPaths)) priorPaths <- priorPaths[[1]]
#       stopifnot(is.character(priorPaths))
#       priorPaths <- tolower(priorPaths)
#       newPaths <- priorPaths
#       for(sharedLibPath in sharedLibPathsVec):
#         if(file.exists(sharedLibPath)):
#           fullpath <- base::normalizePath(file.path(sharedLibPath, subfolder))
#           if(file.exists(fullpath)):
#             if(!(tolower(fullpath) %in% priorPaths)):
#               startupMsg <- appendStartupMsg(paste('Appending to the PATH env var:', fullpath), startupMsg)
#               newPaths <- c(newPaths, fullpath)
#              else 
#               startupMsg <- appendStartupMsg(paste('Path', fullpath, 'already found in PATH environment variable'), startupMsg)
            
          
        
      
#       Sys.setenv(PATH=paste(newPaths, sep=pathSep, collapse=pathSep))
    
#     libfullname <- base::normalizePath(Sys.which(libfilename))
#     if(libfullname=='')
#       startupMsg <- appendStartupMsg(paste0('WARNING: Sys.which("',libfilename,'") did not return a file path'), startupMsg)
#      else 
#       startupMsg <- appendStartupMsg(paste0('first ',libfilename,' shared library in PATH: ', libfullname), startupMsg)
    
  
#   return(startupMsg)


#' Is an object a cinterop wrapper
#'
#' Is an object a cinterop wrapper, and if so of a specified type_id
#'
#' @param x The object to check: is it an ExternalObjRef
#' @param type_id optional, the exact type of the ExternalObjRef to expect
#' @return a logical value
#' @export
def is_native_handle (x, type_id):
    if not isinstance(x, NativeHandle):
        return False
    if type_id is None or type_id == '':
        return True
    return (x.type_id == type_id)


#' Build an error message that an unexpected object is in lieu of an expected cinterop external ref object.
#'
#' Build an error message that an unexpected object is in lieu of an expected cinterop external ref object.
#'
#' @param x actual object that is not of the expected type or underlying type for the external pointer.
#' @param expectedType expected underlying type for the ExternalObj
#' @return a character, the error message
#' @export
# argErrorExternalObjType (x, expectedType):
#   if(!isExternalObjRef(x)):
#     return(paste0('Expected type "', expectedType, '" but got object of type "', typeof(x), '" and class "', class(x), '"' ))
#    else 
#     return(paste0('Expected ExternalObj type "', expectedType, '" but got ExternalObj type "', x@type))
  