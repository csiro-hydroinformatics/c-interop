
[PYPA on Packaging binary extensions](https://packaging.python.org/guides/packaging-binary-extensions)

Interesting read, fairly recent: [Writing cpython extension modules using C++](https://thomasnyberg.com/cpp_extension_modules.html)

[https://github.com/Kozea/cairocffi](https://github.com/Kozea/cairocffi) looks interesting to get architectural ideas from

Curiously there is no clarity as to how to include native code in python packages, as opposed to R packages. See [this SO thread](https://stackoverflow.com/questions/45121352/how-to-include-a-shared-c-library-in-a-python-package). The proposed solutions with manylinux and conda look overly convoluted for something this basic. Off.

Also re-discovered [pybindgen](https://github.com/gjcarneiro/pybindgen), as a reminder (no action required on this)

While I am reluctant to have both cffi and pybind11 as dependencies for the same package `cinterop`, it may make sense given the lightweight approach of pybind11 and well-established, rather than hand crafting native library compilation inside a package, especially the dearth of clarity around this in python packaging guidelines. Starting by learning a bit more following [this](https://pybind11.readthedocs.io/en/master/basics.html). One upward dependent package, which I think I already heard of somehow, is [starry](https://github.com/rodluger/starry)

```bat
conda activate uchronia
where cmake
cd c:\src\tmp
REM note to self: does not work need manual
REM curl -o pybind11_master.zip https://github.com/pybind/pybind11/archive/master.zip
unzip pybind11-master.zip

cd pybind11-master
mkdir build
cd build
cmake ..
```

```txt
CMake Error at tools/FindPythonLibsNew.cmake:125 (message):
Python config failure: Python is 64-bit, chosen compiler is 32-bit
```

```bat
cd c:\src\tmp\pybind11-master\build
rm -rf *
cmake -A x64 ..
```

Decided to try to test uchronia_pd with pybind11, no cinterop at this stage. Starting from python_example for pybind11 as a springboard.
Updrating to use the latest toolchain rather than remaining with 2013. However:

```
Unknown compiler version - please run the configure tests and report the results
```

This appears to be a boost related thing: I need to update boost. OK. Getting nervous about unexpected issues with Boost libraries actross several msvc runtimes though. Then agsin, had forgotten to turn on opaque pointers. Phew. Case in point why you gotta love `void*` in spite of preconceptions.

