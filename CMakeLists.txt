cmake_minimum_required(VERSION 3.1)

## start setting
SET (this_target cinterop)
PROJECT(${this_target})

## section: include directory
INCLUDE_DIRECTORIES(
	./include
)

## section: library directories
LINK_DIRECTORIES(
)


## section: source files
# Add your source files here (one file per line), please SORT in alphabetical order for future maintenance
SET (${this_target}_SOURCE_FILES
)

## section: header files
# Add your header files here(one file per line), please SORT in alphabetical order for future maintenance!


SET(${this_target}_HEADER_FILES
  include/cinterop/c_boost_posix_time_interop.hpp
  include/cinterop/c_cpp_interop.hpp
  include/cinterop/c_interop_forward_decl.h
  include/cinterop/common_c_interop.h
  include/cinterop/object_lifetimes.hpp
  include/cinterop/rcpp_interop.hpp
  include/cinterop/rcpp_strict_r_headers.hpp
  include/cinterop/rcpp_timeseries_interop.hpp
  include/cinterop/timeseries_c_interop.h
  include/cinterop/timeseries_interop.hpp
)

IF (ENABLE_CODECOVERAGE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CMAKE_CXX_FLAGS_COVERAGE}")
ENDIF()

## section: precompiled header
#ADD_MSVC_PRECOMPILED_HEADER("precompiled.h" "precompiled.cpp" MySources)
#ADD_LIBRARY(MyLibrary ${MySources})

SET_SOURCE_FILES_PROPERTIES(${this_target}_HEADER_FILES
                            PROPERTIES HEADER_FILE_ONLY TRUE)
LIST(APPEND ${this_target}_SOURCE_FILES ${${this_target}_HEADER_FILES})

## section: add definitions
#   add prefix -D. example> -DSHP
#  - DO NOT add  the following definitions(already defined in ${OSP_DEFINITIONS}:
#   -DSHP, -DWIN32, -D_WINDOWS, -D_DEBUG, -D_USRDLL, -D_CRT_SECURE_NO_DEPRECATE
ADD_DEFINITIONS(
    # -DCMAKE_CXX_FLAGS:STRING=' -std=c++11 '    
    )

# JM needed to use this as of 2016-07, after an upgrade to latest Debian setup. The Add_definitions macro was not working, somehow.
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

## section: add target
# ADD_LIBRARY(${this_target} SHARED ${${this_target}_SOURCE_FILES} )
add_library(${this_target} INTERFACE)

## section: set link libraries
# TARGET_LINK_LIBRARIES( ${this_target}
# )


# Files to be installed - used by packaging stuff below
INSTALL(FILES ${${this_target}_HEADER_FILES} DESTINATION include/cinterop)


########### Add uninstall target ###############
# uninstall target
configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake_uninstall.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake"
    IMMEDIATE @ONLY)

add_custom_target(uninstall
    COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake)
########### End uninstall target ###############



if(WIN32)
  INSTALL(TARGETS ${this_target}
    RUNTIME DESTINATION bin
  )
else()
  INSTALL(TARGETS ${this_target}
    LIBRARY DESTINATION lib
  )
endif()

# Packages - currently just an RPM
set(CPACK_PACKAGE_VERSION ${VERSION})
set(CPACK_GENERATOR "RPM;TGZ")
set(CPACK_PACKAGE_NAME "cinterop")
set(CPACK_PACKAGE_RELEASE 1)
set(CPACK_RPM_PACKAGE_RELEASE ${CPACK_PACKAGE_RELEASE})
set(CPACK_PACKAGE_CONTACT "Jean-Michel Perraud")
set(CPACK_PACKAGE_VENDOR "CSIRO")
set(CPACK_PACKAGING_INSTALL_PREFIX ${CMAKE_INSTALL_PREFIX})
set(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}-${CPACK_PACKAGE_VERSION}-${CPACK_PACKAGE_RELEASE}.${CMAKE_SYSTEM_PROCESSOR}")
include(CPack)
