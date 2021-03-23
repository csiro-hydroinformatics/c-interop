cmake_minimum_required(VERSION 3.10)

## start setting
SET (this_target cinterop)
set(TARGET_LIB_NAME cinterop)
SET (this_target ${TARGET_LIB_NAME})

set(TARGET_MAJOR 1)
set(TARGET_MINOR 1)
set(TARGET_RELEASE 1)
set(TARGET_VERSION ${TARGET_MAJOR}.${TARGET_MINOR}.${TARGET_RELEASE})
SET (VERSION ${TARGET_VERSION})

PROJECT(${this_target} VERSION ${TARGET_VERSION} DESCRIPTION "Reusable functions for marshalling data between C, C++ and other programming languages")

include(GNUInstallDirs)

## section: include directory
INCLUDE_DIRECTORIES(
	./include
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
ADD_DEFINITIONS(
    # -DCMAKE_CXX_FLAGS:STRING=' -std=c++11 '    
    )

# JM needed to use this as of 2016-07, after an upgrade to latest Debian setup. The Add_definitions macro was not working, somehow.
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

## section: add target
add_library(${this_target} INTERFACE)

configure_file(${TARGET_LIB_NAME}.pc.in ${TARGET_LIB_NAME}.pc @ONLY)

# Files to be installed
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
else()
  install(FILES ${CMAKE_BINARY_DIR}/${TARGET_LIB_NAME}.pc
    # DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/pkgconfig) from examplar, but this appears not prevalent, most I see are under /usr/lib/x86_64-linux-gnu/pkgconfig, so:
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/pkgconfig)
    # The above also prevents a lintian error
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
