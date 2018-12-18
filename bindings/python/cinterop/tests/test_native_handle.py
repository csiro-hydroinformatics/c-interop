import os
import numpy as np
import datetime as dt
import sys
from datetime import datetime

pkg_dir = os.path.join(os.path.dirname(__file__),'..')
sys.path.append(pkg_dir)
from cinterop.native import *

dir_path = 'C:/src/github_jm/rcpp-interop-commons/bindings/python/cinterop/tests/test_native_library/x64/Debug'
native_lib_path = os.path.join(dir_path, 'test_native_library.dll')

ut_ffi = FFI()

ut_ffi.cdef('''
typedef struct _date_time_interop
{
	int year;
	int month;
	int day;
	int hour;
	int minute;
	int second;
} date_time_interop;

typedef struct _interval_interop
{
	date_time_interop start;
	date_time_interop end;
} interval_interop;
''')

ut_ffi.cdef('extern void create_date(date_time_interop* start, int year, int month, int day, int hour, int min, int sec);')
ut_ffi.cdef('extern int test_date(date_time_interop* start, int year, int month, int day, int hour, int min, int sec);')
ut_ffi.cdef('extern  void* create_dog();')
ut_ffi.cdef('extern int get_dog_refcount( void* obj);')
ut_ffi.cdef('extern int remove_dog_reference( void* obj);')
ut_ffi.cdef('extern int add_dog_reference( void* obj);')
ut_ffi.cdef('extern  void* create_owner( void* d);')
ut_ffi.cdef('extern int get_owner_refcount( void* obj);')
ut_ffi.cdef('extern int remove_owner_reference( void* obj);')
ut_ffi.cdef('extern int add_owner_reference( void* obj);')
ut_ffi.cdef('extern int num_dogs();')
ut_ffi.cdef('extern int num_owners();')
ut_ffi.cdef('extern void say_walk( void* owner);')
ut_ffi.cdef('extern void release( void* obj);')

ut_dll = ut_ffi.dlopen(native_lib_path, 1) # Lazy loading


class CustomNativeHandle(NativeHandle):
    def __init__(self, pointer, currentRefCount = 0):
        super(CustomNativeHandle, self).__init__(pointer, type_id='', starting_ref_count = currentRefCount)

    def _release_handle(self):
        ut_dll.release(self.get_handle());
        return True

class Dog(CustomNativeHandle):
    def __init__(self, pointer = None):
        if pointer is None:
            pointer = ut_dll.create_dog()
        super(Dog, self).__init__(pointer)

    @property
    def native_reference_count(self):
        return ut_dll.get_dog_refcount(self.get_handle())

    @staticmethod
    def NumNativeInstances():
        return ut_dll.num_dogs()


class DogOwner(CustomNativeHandle):

    def __init__(self, dog):
        super(DogOwner, self).__init__(None)
        self._set_handle(ut_dll.create_owner(dog.get_handle()))
        self.dog = dog
        self.dog.add_ref()
        
    @property
    def native_reference_count(self):
        return ut_dll.get_owner_refcount(self.get_handle())

    @staticmethod
    def NumNativeInstances():
        return ut_dll.num_owners()

    def say_walk(self):
        ut_dll.say_walk(self.get_handle())

    def _release_handle(self):
        super()._release_handle()
        # super(DogOwner, self)._release_handle()
        self.dog.release()
        return True


# def test_NativeObjectReferenceCounting():

dog = Dog()
assert 1 == dog.reference_count
assert 1 == dog.native_reference_count
dog.add_ref()
assert 2 == dog.reference_count
assert 1 == dog.native_reference_count
owner = DogOwner(dog)
assert 1 == owner.reference_count
assert 3 == dog.reference_count
assert 1 == dog.native_reference_count
dog.release()
assert 1 == owner.reference_count
assert 2 == dog.reference_count
assert 1 == dog.native_reference_count
dog.release()
assert 1 == owner.reference_count
assert 1 == owner.native_reference_count
assert 1 == dog.reference_count
assert 1 == dog.native_reference_count
assert not dog.is_invalid
owner.say_walk()
owner.release()
assert 0 == owner.reference_count
assert 0 == dog.reference_count
# Cannot check on the native ref count - deleted objects. 
# TODO think of a simple way to test these
#assert 0, owner.native_reference_count)
#assert 0, dog.native_reference_count)
assert dog.is_invalid
assert owner.is_invalid

#     /*
#     # Try as i might i cannot seem to force 
#     # garbage collection on this unit test.
#     # If I change the execution point back in debug mode I can get 
#     # an expected finalization, but otherwise, nope. 
#     # This is puzzling. I have to give up on unit testing this. I do not see in 
#     # any way how there could possibly be a mem leak with these.
#     # 2017-10-24 On windows, I cannot get setting dog to null to trigger GC, somehow. 
#     # At least not in debug mode from VS via the test explorer. Using netstandard2.0 as a target platform. i.e. what runtime??
#     # A Watchpoint but the other tests suggest this is a false flag.
#     # 2018-01- Same issue on linux
#     [Fact]
#     public void TestNativeHandleFinalizers()
#     {
#         NativeTestLib lib = new NativeTestLib();
#         int initDogCount = Dog.NumNativeInstances;

#         Dog dog = new Dog();
#         assert initDogCount + 1, Dog.NumNativeInstances);
#         assert 1, dog.reference_count);
#         assert 1, dog.native_reference_count);
#         # if dog reference a new instance and we force garbage GC:
#         CallGC();
#         dog = new Dog();
#         var gen = System.GC.GetGeneration(dog);
#         CallGC();
#         gen = System.GC.GetGeneration(dog);
#         CallGC();
#         assert 1, dog.reference_count);
#         assert 1, dog.native_reference_count);
#         assert initDogCount + 2, Dog.NumNativeInstances);
#         # if dog reference a new instance and we force garbage GC:
#         dog = new Dog();
#         CallGC();
#         CallGC();
#         assert 1, dog.reference_count);
#         assert 1, dog.native_reference_count);
#         assert initDogCount + 2, Dog.NumNativeInstances);

#         dog = null;
#         CallGC();
#         assert initDogCount, Dog.NumNativeInstances);
#     }
# */
#     [Fact]
#     public void TestNativeHandleDisposal()
#     {
#         NativeTestLib lib = new NativeTestLib();
#         int initDogCount = Dog.NumNativeInstances;

#         Dog dog = new Dog();
#         assert initDogCount + 1, Dog.NumNativeInstances);
#         assert 1, dog.reference_count);
#         assert 1, dog.native_reference_count);
#         dog.Dispose();
#         assert initDogCount, Dog.NumNativeInstances);
#     }

#     #/ <summary>
#     #/ Use intended only for unit tests.
#     #/ </summary>
#     public static long CallGC()
#     {
#         for (int i = 0; i < GC.MaxGeneration * 2; i++)
#         {
#             GC.Collect();
#             GC.WaitForPendingFinalizers();
#         }
#         GC.Collect(GC.MaxGeneration, GCCollectionMode.Forced, true, true);
#         GC.WaitForPendingFinalizers();
#         return GC.GetTotalMemory(true);
#     }

# }
# }


