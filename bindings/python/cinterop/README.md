# cinterop

<!-- [![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/csiro-hydroinformatics/rcpp-interop-commons/blob/master/bindings/python/cinterop/LICENSE.txt) ![status](https://img.shields.io/badge/status-beta-blue.svg) [![Documentation Status](https://readthedocs.org/projects/pycinterop/badge/?version=latest)](https://pycinterop.readthedocs.io/en/latest/?badge=latest) master: [![Build status - master](https://ci.appveyor.com/api/projects/status/vmwq7xarxxj8s564/branch/master?svg=true)](https://ci.appveyor.com/project/jmp75/pycinterop/branch/master) testing: [![Build status - devel](https://ci.appveyor.com/api/projects/status/vmwq7xarxxj8s564/branch/testing?svg=true)](https://ci.appveyor.com/project/jmp75/pycinterop/branch/testing)
 -->

<!-- ![Reference counted native handles](./docs/img/cinterop-principles.png "Reference counted native handles") -->

[Marshalling data between C, C++ and other programming languages](https://github.com/csiro-hydroinformatics/rcpp-interop-commons)

This package is primarily for managing and marshalling resources in native libraries, written for instance in C++, from Python. 

## License

MIT (see [License.txt](https://github.com/csiro-hydroinformatics/rcpp-interop-commons/blob/master/bindings/python/cinterop/LICENSE.txt))

## Documentation

Placeholder 

<!-- Hosted at [pycinterop.readthedocs.io](https://pycinterop.readthedocs.io/en/latest/?badge=latest) -->

## Source code

The code repository is on [GitHub](https://github.com/csiro-hydroinformatics/rcpp-interop-commons).

## Installation

```sh
pip install cinterop
```

From source:

```sh
pip install -r requirements.txt
python setup.py install
```

## Sample use

Placeholder section

## Related work

Placeholder section

### Ancestry, acknowledgements

This python package `cinterop` relates loosely to prior work for interoperability between C++, R and .NET ([R.NET](https://github.com/rdotnet/rdotnet))

`cinterop` features using `cffi` were also significantly informed by Kevin Plastow's [work](https://search.informit.com.au/documentSummary;dn=823898220073899;res=IELENG) while he was at the Australian Bureau of Meteorology; this contribution is gratefully acknowledged.

In you have native interop needs you may also want to look at:

* the nuget package [dynamic-interop-dll](https://github.com/rdotnet/dynamic-interop-dll) for .NET/native interop.
* Reference counting package [refcount](https://github.com/csiro-hydroinformatics/pyrefcount)
* a C# library for [generating interop glue code on top of C API glue code](https://github.com/csiro-hydroinformatics/c-api-wrapper-generation).

### Other python packages

Placeholder
