import os
import sys
from datetime import datetime
import gc
import cinterop
from cinterop.cffi.marshal import * 

pkg_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, pkg_dir)

from refcount.interop import *
from refcount.putils import library_short_filename

fname = library_short_filename("test_native_library")

if sys.platform == "win32":
    dir_path = os.path.join(pkg_dir, "tests/test_native_library/x64/Debug")
else:
    dir_path = os.path.join(pkg_dir, "tests/test_native_library/build")
    cdefs_dir = os.path.join(pkg_dir, 'tests/test_native_library')

native_lib_path = os.path.join(dir_path, fname)

assert os.path.exists(native_lib_path)


# test_native_obj_ref_counting()
# test_cffi_native_handle_finalizers()
# test_cffi_native_handle_dispose()

ut_ffi = FFI()

with open(os.path.join(cdefs_dir, 'structs_cdef.h')) as f_headers:
    ut_ffi.cdef(f_headers.read())

with open(os.path.join(cdefs_dir, 'funcs_cdef.h')) as f_headers:
    ut_ffi.cdef(f_headers.read())

ut_dll = ut_ffi.dlopen(native_lib_path, 1)  # Lazy loading

marshal = CffiMarshal(ut_ffi)

def test_date_time_interop():
    ptr = ut_dll.create_date(2019, 12, 1, 2, 3, 4)
    dt = marshal.as_datetime(ptr)
    ut_dll.dispose_date(ptr)
    assert dt.year == 2019
    # Pass in a datetime into a native lib function
    dt = datetime(2001, 1, 2, 3, 4, 5)
    dt_ptr = marshal.datetime_to_dtts(dt)
    assert ut_dll.get_year(dt_ptr.obj) == 2001

if __name__ == "__main__":
    test_date_time_interop()
